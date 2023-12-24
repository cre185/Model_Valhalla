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
        <a-button style="background-color: white;" @click="showMiniMsgBox">
          <template #icon>
            <icon-notification />
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
                  <a-button type="text" @click="emptyList">
                    {{ $t('messageBox.tab.button') }}
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
} from '@/api/message';
import useLoading from '@/hooks/loading';
import List from './list.vue';

const router = useRouter();
const myAvatar = ref();
const Login = () => {
  router.push({
    name: 'Login',
  });
};
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
const avatar = computed(() => {
  return userStore.avatar;
});
const theme = computed(() => {
  return appStore.theme;
});
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
const handleLogout = () => {
  logout();
};
const setDropDownVisible = () => {
  const event = new MouseEvent('click', {
    view: window,
    bubbles: true,
    cancelable: true,
  });
  triggerBtn.value.dispatchEvent(event);
};
const switchRoles = async () => {
  const res = await userStore.switchRoles();
  Message.success(res as string);
};
const toggleDrawerMenu = inject('toggleDrawerMenu') as () => void;

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
const messageType = ref('message');
const { t } = useI18n();
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
    key: 'message',
    title: "666",
  },
  {
    key: 'notice',
    title: "777",
  },
  {
    key: 'todo',
    title: "888",
  },
];
async function fetchSourceData() {
  setLoading(true);
  try {
    const { data } = await queryMessageList(getToken()!);
    // messageData.messageList = data;
    data.msgs.forEach(item => {
      const newUserToDataset: userToDataset = {
        msg_id: item.id,
        msg_type: item.msg_type,
        src_UserID: item.author,
        dst_DatasetID: "2",
        msg_title: item.msg,
        msg_content: "666",
        add_time: item.add_time,
        read: item.read,
        avatar: "666",
        messageType: "0",
      };
      messageData.messageList.push(newUserToDataset);
    });
  } catch (err) {
    // you can report use errorHandler or other
  } finally {
    setLoading(false);
  }
}
async function readMessage(data: MessageListType) {
  const ids = data.map((item) => item.msg_id);
  await setMessageStatus({ ids });
}
fetchSourceData();
const renderList = computed(() => {
  return messageData.messageList.filter(
    (item) => messageType.value === "message"
  );
});
console.log("computed", messageData.messageList[0]);
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
  if (renderList.value.length) readMessage([...items]);
};
const emptyList = () => {
  messageData.messageList = [];
};
const showMiniMsgBox = () => {
  msgVisible.value = true;
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
</style>
