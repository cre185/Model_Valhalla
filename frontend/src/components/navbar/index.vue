<template>
  <div class="navbar">
    <div class="left-side">
      <a-space>
        <img alt="logo" src="../../assets/trophy.png" width="25" height="25" />
        <a-typography-title :style="{ margin: 0, fontSize: '18px' }" :heading="5">
          模型竞技场 Model Valhalla
        </a-typography-title>
      </a-space>
    </div>

    <ul key="update" class="right-side" id="parentNode">
      <a-trigger trigger="click" :unmount-on-close="false">
        <a-button id="msgButton" style="background-color: white;" @click="showMiniMsgBox" shape="circle">
          <template #icon>
            <icon-email />
          </template>
        </a-button>
        <template #content>
          <div class="demo-basic" style="background-color: white; width: 400px;">
            <a-spin style="display: block" :loading="loading">
              <a-tabs v-model:activeKey="messageType" type="rounded" destroy-on-hide>
                <a-tab-pane v-for="item in tabList" :key="item.key">
                  <template #title>
                    <span> {{ item.title }}{{ formatUnreadLength(item.key) }} </span>
                  </template>
                  <a-result v-if="!renderList.length" status="404">
                    <template #subtitle> {{ $t('messageBox.noContent') }} </template>
                  </a-result>
                  <List :render-list="renderList" :unread-count="unreadCount" @item-click="handleItemClick" />
                </a-tab-pane>
                <template #extra>
                  <a-button type="text" @click="checkMore">
                    {{ $t('messageBox.viewMore') }}
                  </a-button>
                </template>
              </a-tabs>
            </a-spin>
          </div>
        </template>
      </a-trigger>
      <li v-if="isLogin()">
        <a-space :size="16">
          <span>{{ $t('navbar.welcome') }}{{ userStore.username }}</span>
          <a-popover @mouseenter="resizeBigAvatar" @mouseleave="resizeSmallAvatar">
            <a-avatar ref="myAvatar" id="userInfoPanelAvatar">
              <img alt="用户头像" :src="userStore.avatar" />
            </a-avatar>
            <template #content>
              <a-space direction="vertical">
                <a-button type="primary" class="hoverButton">
                  <template #icon>
                    <icon-user />
                  </template>
                  <template #default>{{ $t('menu.user.info') }}</template>
                </a-button>
                <a-button type="primary" class="hoverButton">
                  <template #icon>
                    <icon-settings />
                  </template>
                  <template #default>{{ $t('menu.user.setting') }}</template>
                </a-button>
              </a-space>
              <a-divider margin="5px" />
              <a-button type="primary" class="hoverButton" @click="myLogout">
                <template #icon>
                  <icon-export />
                </template>
                <template #default>{{ $t('navbar.quit') }}</template>
              </a-button>
            </template>
          </a-popover>
        </a-space>
      </li>
      <li v-else @click="Login" id="userInfoPanel">
        <a-space size="medium">
          <span>您好，请先登录</span>
          <a-avatar :size="32" :style="{ backgroundColor: '#FFC72E' }">
            <IconUser />
          </a-avatar>
        </a-space>
      </li>
    </ul>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, inject, onMounted, nextTick, reactive, toRefs } from 'vue';
import { Message } from '@arco-design/web-vue';
import { useDark, useToggle, useFullscreen } from '@vueuse/core';
import { useAppStore, useUserStore } from '@/store';
import { LOCALE_OPTIONS } from '@/locale';
import useLocale from '@/hooks/locale';
import useUser from '@/hooks/user';
import { useRouter } from 'vue-router';
import { getToken, isLogin } from '@/utils/auth';
import { useI18n } from "vue-i18n";
import {
  queryMessageList,
  setMessageStatus,
  userToDataset,
  MessageListType,
  getUserAvatar,
} from '@/api/message';
import useLoading from '@/hooks/loading';
import axios from 'axios';
import apiCat from '@/api/main';
import { Comment } from 'vue';
import List from './list.vue';

const router = useRouter();
const myAvatar = ref();
const Login = () => {
  router.push({
    name: 'Login',
  });
};
const { t } = useI18n();
const jwt = getToken();
const update = ref(false);
const msgVisible = ref(false);
const appStore = useAppStore();
const userStore = useUserStore();
userStore.setInfo(JSON.parse(localStorage.getItem('userStore')!));
const { logout } = useUser();
const { changeLocale, currentLocale } = useLocale();
const { isFullscreen, toggle: toggleFullScreen } = useFullscreen();
const locales = [...LOCALE_OPTIONS];
const topMenu = computed(() => appStore.topMenu && appStore.menu);
const isDark = useDark({
  selector: 'body',
  attribute: 'arco-theme',
  valueDark: 'dark',
  valueLight: 'light',
  storageKey: 'arco-theme',
  onChanged(dark: boolean) {
    // overridden default behavior
    appStore.toggleTheme(dark);
  },
});
const toggleTheme = useToggle(isDark);
const handleToggleTheme = () => {
  toggleTheme();
};
const setVisible = () => {
  appStore.updateSettings({ globalSettings: true });
};
const refBtn = ref();
const triggerBtn = ref();
const setPopoverVisible = () => {
  const event = new MouseEvent('click', {
    view: window,
    bubbles: true,
    cancelable: true,
  });
  refBtn.value.dispatchEvent(event);
};

const resizeBigAvatar = () => {
  myAvatar.value.$el.style.width = '64px';
  myAvatar.value.$el.style.height = '64px';
  myAvatar.value.$el.style.marginLeft = '16px';
  myAvatar.value.$el.style.transform = 'translate(-10px, 10px)';
}

const resizeSmallAvatar = () => {
  myAvatar.value.$el.style.width = '32px';
  myAvatar.value.$el.style.height = '32px';
  myAvatar.value.$el.style.marginLeft = '0px';
  myAvatar.value.$el.style.transform = 'translate(0, 0)';
}

const myLogout = async () => {
  await logout();
  update.value = !update.value;
}
interface TabItem {
  key: string;
  title: string;
  avatar?: string;
}
const { loading, setLoading } = useLoading(true);
const messageType = ref('like');
const messageData = reactive<{
  renderList: userToDataset[];
  messageList: userToDataset[];
}>({
  renderList: [],
  messageList: [],
});
toRefs(messageData);
const tabList: TabItem[] = [
  {
    key: 'like',
    title: t('messageBox.tab.title.one'),
  },
  {
    key: 'comment',
    title: t('messageBox.tab.title.two'),
  },
  {
    key: 'system',
    title: t('messageBox.tab.title.three'),
  },
];
async function fetchSourceData() {
  setLoading(true);
  messageData.messageList = [];
  try {
    const { data } = await queryMessageList(getToken()!);
    // messageData.messageList = data;
    data.msgs.forEach(async (item) => {
      const newUserToDataset: userToDataset = {
        msg_id: item.id,
        msg_type: item.msg_type,
        src_UserID: item.author,
        msg_text: "Unknown",
        msg_content: item.msg_content,
        msg_title: "Unknown",
        add_time: item.add_time,
        read: item.read,
        avatar: "Unknown",
        messageType: "0",
      };
      const responseUser = await axios.get(apiCat(`/user/retrieve/${item.author}`), {
        headers: {
          Authorization: getToken()!,
        },
      });
      if (item.msg_type === "Upload") { // 上传数据集
        newUserToDataset.msg_title = t('messageBox.upload.title');
        if (currentLocale.value === "zh-CN") {
          newUserToDataset.msg_text = `${responseUser.data.username}上传了数据集:${item.msg_content.datasetName}`;
        }
        else {
          newUserToDataset.msg_text = `${responseUser.data.username} uploaded the dataset ${item.msg_content.datasetName}`;
        }
      }
      else if (item.msg_type === "Reply") { // 回复了评论
        if (currentLocale.value === "zh-CN") {
          newUserToDataset.msg_title = `${responseUser.data.username}回复了你的评论`;
        }
        else {
          newUserToDataset.msg_title = `${responseUser.data.username} replied to your comment`;
        }
        newUserToDataset.msg_text = item.msg_content.childContent;
      }
      else if (item.msg_type === "Like") { // 点赞消息
        newUserToDataset.msg_title = t('messageBox.like.title');
        if (currentLocale.value === "zh-CN") {
          newUserToDataset.msg_text = `${responseUser.data.username}点赞了你的评论“${item.msg_content.likeContent}”`;
        }
        else {
          newUserToDataset.msg_text = `${responseUser.data.username} liked your comment "${item.msg_content.likeContent}"`;
        }
      }
      else if (item.msg_type === "Feedback") { // 数据集反馈意见
        newUserToDataset.msg_title = t('messageBox.feedback.title');
        const responseDataset = await axios.get(apiCat(`/dataset/retrieve/${item.msg_content.datasetID}`), {
          headers: {
            Authorization: getToken()!,
          },
        });
        if (currentLocale.value === "zh-CN") {
          newUserToDataset.msg_text = `原因:${item.msg_content.feedbackType}，具体描述:${item.msg_content.feedbackContent}`;
        }
        else {
          newUserToDataset.msg_text = `Reason: ${item.msg_content.feedbackType}, Detailed description: ${item.msg_content.feedbackContent}`;
        }
      }
      else if (item.msg_type === "Report") { // 数据集举报
        newUserToDataset.msg_title = t('messageBox.report.title');
        const responseDataset = await axios.get(apiCat(`/dataset/retrieve/${item.msg_content.datasetID}`), {
          headers: {
            Authorization: getToken()!,
          },
        });
        if (currentLocale.value === "zh-CN") {
          newUserToDataset.msg_text = `原因:${item.msg_content.reportReason}，具体描述:${item.msg_content.reportContent}`;
        }
        else {
          newUserToDataset.msg_text = `Reason: ${item.msg_content.reportReason}, Detailed description: ${item.msg_content.reportContent}`;
        }
      }
      else if (item.msg_type === "Advice") { // 对抗评测意见
        if (currentLocale.value === "zh-CN") {
          newUserToDataset.msg_title = `${responseUser.data.username}提出评测建议`;
          newUserToDataset.msg_text = `具体内容:${item.msg_content.adviceContent}`;
        }
        else {
          newUserToDataset.msg_title = `${responseUser.data.username} proposed suggestions`
          newUserToDataset.msg_text = `Detailed content: ${item.msg_content.adviceContent}`;
        }
      }
      newUserToDataset.avatar = await getUserAvatar(getToken()!, item.author);
      messageData.messageList.push(newUserToDataset);
    });
  } catch (err) {
    // you can report use errorHandler or other
  } finally {
    setLoading(false);
  }
}
async function readMessage(data: MessageListType) { // 提前msg_id设置为已读
  const ids = data.map((item) => item.msg_id);
  await setMessageStatus({ ids });
}
const renderList = computed(() => { // 创建一个过滤属性，只包含未读的消息列表，并设置显示四条
  if (messageType.value === 'like') {
    return messageData.messageList.filter(
      (item) => !item.read && item.msg_type === 'Like'
    ).slice(0, 4);
  }
  if (messageType.value === 'comment') {
    return messageData.messageList.filter(
      (item) => !item.read && item.msg_type === 'Reply'
    ).slice(0, 4);
  }
  return messageData.messageList.filter(
    (item) => !item.read && item.msg_type !== 'Reply' && item.msg_type !== 'Like'
  ).slice(0, 4);
});
const unreadCount = computed(() => {
  return renderList.value.filter((item) => !item.read).length;
});
const getUnreadList = (type: string) => {
  const list = messageData.messageList.filter(
    (item) => item.msg_type === type && !item.read
  );
  return list;
};
const formatUnreadLength = (type: string) => {
  const list = getUnreadList(type);
  return list.length ? `(${list.length})` : ``;
};
const handleItemClick = (items: MessageListType) => {
  if (renderList.value.length) {
    readMessage([...items]);
  }
  axios.post(apiCat('/user/check_message'), { id: items[0].msg_id }, { // 点击后先设置消息已读
    headers: {
      Authorization: getToken()!,
    }
  })
  msgVisible.value = false;
  const routerType = items[0].msg_type;
  if (routerType === "Upload") // 设置反馈路由，目前仅调转页面，后续具体参数要沟通
  {
    let target;
    if ('targetID' in items[0].msg_content) {
      target = items[0].msg_content.targetID as string;
    }
    router.push({
      path: '/dataset/details',
      params: { toShowDetailsID: target, toShowPanelIndex: 1 },
    });
  }
  else if (routerType === "Reply") // 设置回复评论路由
  {
    let target;
    if ('targetID' in items[0].msg_content) {
      target = items[0].msg_content.targetID as string;
    }
    if ('contentFlag' in items[0].msg_content && !items[0].msg_content.contentFlag) {
      router.push({
        path: '/dataset/details',
        params: { toShowDetailsID: target, toShowPanelIndex: 4 },
      });
    }
    else {
      router.push({
        path: '/leaderboard/details',
        params: { toShowDetailsID: target, toShowPanelIndex: 4 },
      });
    }
  }
  else if (routerType === "Like") {
    let target;
    if ('targetID' in items[0].msg_content) {
      target = items[0].msg_content.targetID as string;
    }
    if ('likeFlag' in items[0].msg_content && !items[0].msg_content.likeFlag) // 设置点赞信息路由
    {
      router.push({
        path: '/dataset/details',
        params: { toShowDetailsID: target, toShowPanelIndex: 4 },
      });
    }
    else {
      router.push({
        path: '/leaderboard/details',
        params: { toShowDetailsID: target, toShowPanelIndex: 4 },
      });
    }
  }
  else if (routerType === "Feedback") { // 设置反馈的路由
    if ('datasetID' in items[0].msg_content) {
      const datasetID = items[0].msg_content.datasetID as string;
      console.log(datasetID);
      router.push({
        name: '/dataset/details',
        params: { toShowDetailsID: datasetID, toShowPanelIndex: 1 },
      });
    }
  }
  else if (routerType === "Report") {
    if ('datasetID' in items[0].msg_content) {
      const datasetID = items[0].msg_content.datasetID as string;
      console.log(datasetID);
      router.push({
        name: '/dataset/details',
        params: { toShowDetailsID: datasetID, toShowPanelIndex: 1 },
      });
    }
  }
};
const emptyList = () => {
  messageData.messageList = [];
};
const showMiniMsgBox = () => { // 点击后再获得消息
  fetchSourceData();
  msgVisible.value = true;
}
const checkMore = () => {
  router.push({
    path: '/user/info',
  });
}
</script>

<style scoped lang="less">
.navbar {
  display: flex;
  justify-content: space-between;
  height: 100%;
  background-color: var(--color-bg-2);
  border-bottom: 1px solid var(--color-border);
}

.left-side {
  display: flex;
  align-items: center;
  padding-left: 20px;
}

.center-side {
  flex: 1;
}

.right-side {
  display: flex;
  padding-right: 20px;
  list-style: none;

  :deep(.locale-select) {
    border-radius: 20px;
  }

  li {
    display: flex;
    align-items: center;
    padding: 0 10px;
  }

  a {
    color: var(--color-text-1);
    text-decoration: none;
  }

  .nav-btn {
    border-color: rgb(var(--gray-2));
    color: rgb(var(--gray-8));
    font-size: 16px;
  }

  .trigger-btn,
  .ref-btn {
    position: absolute;
    bottom: 14px;
  }

  .trigger-btn {
    margin-left: 14px;
  }
}

#userInfoPanel {
  cursor: pointer;
}

#userInfoPanelAvatar {
  position: relative;
  width: 32px;
  height: 32px;
  cursor: pointer;
  transition: all 0.5s ease-in-out;
}

.hoverButton {
  background: white;
  color: #6b6f76;
}

.hoverButton:hover {
  background: #e3e5e7;
  color: #6b6f76;
}

.message-popover {
  .arco-popover-content {
    margin-top: 0;
  }
}

:deep(.arco-popover-popup-content) {
  padding: 0;
}

:deep(.arco-list-item-meta) {
  align-items: flex-start;
}

:deep(.arco-tabs-nav) {
  padding: 14px 0 12px 16px;
  border-bottom: 1px solid var(--color-neutral-3);
}

:deep(.arco-tabs-content) {
  padding-top: 0;

  .arco-result-subtitle {
    color: rgb(var(--gray-6));
  }
}

#msgButton :hover {
  background-color: aliceblue
}
</style>
