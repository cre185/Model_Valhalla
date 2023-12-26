<template>
  <div class="navbar">
    <div class="left-side">
      <a-space>
        <img alt="logo" src="../../assets/trophy.png" width="25" height="25" />
        <a-typography-title
          :style="{ margin: 0, fontSize: '18px' }"
          :heading="5"
        >
          模型竞技场 Model Valhalla
        </a-typography-title>
      </a-space>
    </div>

    <ul :key="update" class="right-side">
      <a-dropdown trigger="click" @select="changeLocale as any">
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
      <li v-if="isLogin()">
        <a-space :size="16">
          <span>{{ $t('navbar.welcome') }}{{ userStore.username }}</span>
          <a-popover @mouseenter="resizeBigAvatar" @mouseleave="resizeSmallAvatar">
            <a-avatar ref="myAvatar" id="userInfoPanelAvatar">
              <img alt="用户头像" :src="userStore.avatar"/>
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
              <a-divider margin="5px"/>
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
  import { LOCALE_OPTIONS } from '@/locale';
  import useLocale from '@/hooks/locale';
  import useUser from '@/hooks/user';
  import { useRouter } from 'vue-router';
  import { getToken, isLogin } from '@/utils/auth';
  import {useI18n} from "vue-i18n";

  const router = useRouter();
  const myAvatar = ref();
  const Login = () => {
    router.push({
      name: 'Login',
    });
  };
  const jwt = getToken();
  const update = ref(false);

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
</style>

<style lang="less">
  .message-popover {
    .arco-popover-content {
      margin-top: 0;
    }
  }
</style>
