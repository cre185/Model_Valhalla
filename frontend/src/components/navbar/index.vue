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
      <a-space>
        <a-dropdown trigger="click" @select="handleChangeLocale">
          <a-button
              class="nav-btn"
              type="outline"
              :shape="'circle'"
          >
            <template #icon>
              <icon-language />
            </template>
          </a-button>
          <template #content>
            <a-doption
                v-for="item in locales"
                :key="item.value"
                :value="item.value"
            >
              <template #icon>
                <icon-check v-show="item.value === currentLocale" />
              </template>
              {{ item.label }}
            </a-doption>
          </template>
        </a-dropdown>
        <a-popover :popup-visible="msgVisible"
                   :content-style="{width: '21vw', height: '50vh', padding: '0'}"
        >
          <a-badge :count="unreadCount">
            <a-button
                class="nav-btn"
                type="outline"
                :shape="'circle'"
                @click="showMiniMsgBox"
            >
              <template #icon>
                <icon-notification />
              </template>
            </a-button>
          </a-badge>
          <template #content >
            <MessageBox v-if="currentLocale1==='zh-CN'"
                        :currentLocale="'zh-CN'"
                        @changeShowingStatus="showMiniMsgBox"
                        :size="'small'"
            />
            <MessageBox v-else
                        :currentLocale="'en-US'"
                        @changeShowingStatus="showMiniMsgBox"
                        :size="'small'"
            />
          </template>
        </a-popover>
      </a-space>
      <li v-if="isLogin()">
        <a-space :size="16">
          <span>{{ $t('navbar.welcome') }}{{ userStore.username }}</span>
          <a-popover @mouseenter="resizeBigAvatar" @mouseleave="resizeSmallAvatar">
            <a-avatar ref="myAvatar" id="userInfoPanelAvatar">
              <img alt="用户头像" :src="userStore.avatar" />
            </a-avatar>
            <template #content>
              <a-space direction="vertical">
                <a-button type="primary" class="hoverButton" @click="handleInfo">
                  <template #icon>
                    <icon-user />
                  </template>
                  <template #default>{{ $t('menu.user.info') }}</template>
                </a-button>
                <a-button type="primary" class="hoverButton" @click="handleSetting">
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
  import {computed, ref, inject, onMounted, nextTick} from 'vue';
  import { Message } from '@arco-design/web-vue';
  import { useDark, useToggle, useFullscreen } from '@vueuse/core';
  import { useAppStore, useUserStore } from '@/store';
  import useUser from '@/hooks/user';
  import { useRouter } from 'vue-router';
  import { getToken, isLogin } from '@/utils/auth';
  import { LOCALE_OPTIONS } from '@/locale';
  import useLocale from '@/hooks/locale';
  import eventBus from '@/api/event-bus';
  import { useI18n } from "vue-i18n";
  import {
    getMessageData,
    setMessageStatus,
    userToDataset,
    MessageListType,
    getUserAvatar,
  } from '@/api/message';
  import useLoading from '@/hooks/loading';
  import {getLocale} from "@arco-design/web-vue";
  import MessageBox from './components/message-box.vue';

  const router = useRouter();
  const myAvatar = ref();
  const msgVisible = ref(false);
  const Login = () => {
    router.push({
      name: 'Login',
    });
  };
  const { t } = useI18n();
  const jwt = getToken();
  const update = ref(false);
  const appStore = useAppStore();
  const userStore = useUserStore();
  userStore.setInfo(JSON.parse(localStorage.getItem('userStore')!));
  const { logout } = useUser();
  const currentLocale1 = ref(getLocale());
  const { changeLocale, currentLocale } = useLocale();
  const locales = [...LOCALE_OPTIONS];

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

  const handleInfo = async () => {
    await router.push({
      name: 'Info',
    });
  }

  const handleSetting = async () => {
    await router.push({
      name: 'Setting',
    });
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
  const messageData = ref<userToDataset[]>([]);
  const unreadCount = ref(0);

  const showMiniMsgBox = () => { // 点击后再获得消息
    msgVisible.value = !msgVisible.value;
  }

  const handleChangeLocale = (value: string) => {
    console.log(value);
    changeLocale(value);
    currentLocale1.value = value;
  }

  onMounted(() => {
    getMessageData(getLocale(), t).then(data => {
      messageData.value = data;
      unreadCount.value = data.filter(item => !item.read).length;
    });
    document.addEventListener('scroll', ()=>{
      msgVisible.value = false;
    });
    eventBus.on('updateNavbar', () => {
      update.value = !update.value;
    });
  });
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
