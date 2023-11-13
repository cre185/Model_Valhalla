<template>
  <div class="login-form-wrapper">
    <div class="login-form-title">{{ $t('login.form.title') }}</div>
    <a-tabs v-model:active-key="loginWay">
      <a-tab-pane key="1">
        <template #title>
          {{ $t('login.form.loginWay.password') }}
        </template>
        <div class="login-form-error-msg">{{ errorMessage }}</div>
        <a-form
          ref="loginForm"
          :model="userPassInfo"
          class="login-form"
          layout="vertical"
          @submit="handleSubmit"
        >
          <a-form-item
            field="username"
            :rules="[
              { required: true, message: $t('login.form.userName.errMsg') },
            ]"
            :validate-trigger="['change', 'blur']"
            hide-label
          >
            <a-input
              v-model="userPassInfo.username"
              :placeholder="$t('login.form.userName.placeholder')"
            >
              <template #prefix>
                <icon-user />
              </template>
            </a-input>
          </a-form-item>
          <a-form-item
            field="password"
            :rules="[
              { required: true, message: $t('login.form.password.errMsg') },
            ]"
            :validate-trigger="['change', 'blur']"
            hide-label
          >
            <a-input-password
              v-model="userPassInfo.password"
              :placeholder="$t('login.form.password.placeholder')"
              allow-clear
            >
              <template #prefix>
                <icon-lock />
              </template>
            </a-input-password>
          </a-form-item>
          <a-space :size="16" direction="vertical">
            <div class="login-form-password-actions">
              <a-checkbox
                checked="rememberPassword"
                :model-value="loginByPasswordConfig.rememberPassword"
                @change="setRememberPassword as any"
              >
                {{ $t('login.form.rememberPassword') }}
              </a-checkbox>
              <a-link>{{ $t('login.form.forgetPassword') }}</a-link>
            </div>
            <a-button type="primary" html-type="submit" long :loading="loading">
              {{ $t('login.form.login') }}
            </a-button>
            <router-link to="/register">
              <a-button type="text" long class="login-form-register-btn">
                {{ $t('login.form.register') }}
              </a-button>
            </router-link>
          </a-space>
        </a-form>
      </a-tab-pane>
      <a-tab-pane key="2">
        <template #title>
          {{ $t('login.form.loginWay.code') }}
        </template>
        <div class="login-form-error-msg">{{ errorMessage }}</div>
        <a-form
          ref="loginForm"
          :model="userCodeInfo"
          class="login-form"
          layout="vertical"
          @submit="handleSubmit"
        >
          <a-form-item
            field="mobile"
            :rules="phoneRules"
            :validate-trigger="['change', 'blur']"
            hide-label
          >
            <a-input
              v-model="userCodeInfo.mobile"
              :placeholder="$t('login.form.phone.placeholder')"
            >
              <template #prefix>
                <icon-phone />
              </template>
            </a-input>
          </a-form-item>
          <a-form-item field="code" :rules="codeRules" hide-label>
            <a-input
              v-model="userCodeInfo.code"
              :placeholder="$t('login.form.code.placeholder')"
              allow-clear
            >
              <template #prefix>
                <icon-message />
              </template>
              <template #append>
                <a-button
                  v-if="codeInterval.codeInterval < 0"
                  type="primary"
                  @click="handleSendCode"
                >
                  {{ $t('login.form.code.buttonText1') }}
                </a-button>
                <a-button v-if="codeInterval.codeInterval >= 0">
                  {{
                    codeInterval.codeInterval +
                    $t('register.form.code.buttonText2')
                  }}
                </a-button>
              </template>
            </a-input>
          </a-form-item>
          <a-space :size="16" direction="vertical">
            <div id="codeMargin"></div>
            <a-button type="primary" html-type="submit" long :loading="loading">
              {{ $t('login.form.login') }}
            </a-button>
            <router-link to="../register">
              <a-button type="text" long class="login-form-register-btn">
                {{ $t('login.form.register') }}
              </a-button>
            </router-link>
          </a-space>
        </a-form>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script lang="ts" setup>
  import { ref, reactive, getCurrentInstance } from 'vue';
  import { useRouter } from 'vue-router';
  import { Message } from '@arco-design/web-vue';
  import { ValidatedError } from '@arco-design/web-vue/es/form/interface';
  import { useI18n } from 'vue-i18n';
  import { useStorage } from '@vueuse/core';
  import { useUserStore } from '@/store';
  import useLoading from '@/hooks/loading';
  import type { LoginData, phoneVerifyData } from '@/api/user';
  import {
    getUsername,
    getRegisterTime,
    getPhone,
    getAvatar,
    getEmail,
  } from '@/api/user-info';
  import { getToken } from '@/utils/auth';

  const router = useRouter();
  const { t } = useI18n();
  const errorMessage = ref('');
  const { loading, setLoading } = useLoading();
  const userStore = useUserStore();
  const { proxy } = getCurrentInstance();

  const loginByPasswordConfig = useStorage('login-by-password-config', {
    rememberPassword: true,
    username: 'admin', // 演示默认值
    password: 'admin', // demo default value
  });
  const userPassInfo = reactive({
    username: loginByPasswordConfig.value.username,
    password: loginByPasswordConfig.value.password,
  });
  const userCodeInfo = reactive({
    mobile: '',
    code: '',
  });

  const codeInterval = reactive({
    codeTimer: null as null | ReturnType<typeof setInterval>,
    codeInterval: -1,
  });

  const loginWay = ref('1');
  const handleSubmit = async ({
    errors,
    values,
  }: {
    errors: Record<string, ValidatedError> | undefined;
    values: Record<string, any>;
  }) => {
    if (loading.value) return;
    if (!errors) {
      setLoading(true);
      try {
        if (loginWay.value === '1') {
          await userStore.login(values as LoginData);
        } else {
          await userStore.loginByPhone(values as phoneVerifyData);
        }
        const { redirect, ...othersQuery } = router.currentRoute.value.query;
        const jwt = getToken();
        const userID = userStore.$state.accountId;
        let name;
        let registrationDate;
        let avatar;
        let phone;
        let email;
        await getUsername(userID!, jwt!).then((returnValue) => {
          name = returnValue;
        });
        await getRegisterTime(userID!, jwt!).then((returnValue) => {
          registrationDate = returnValue;
        });
        await getAvatar(userID!, jwt!).then((returnValue) => {
          avatar = returnValue;
        });
        await getPhone(userID!, jwt!).then((returnValue) => {
          phone = returnValue;
        });
        await getEmail(userID!, jwt!).then((returnValue) => {
          email = returnValue;
        });
        userStore.setInfo({
          username: name,
          avatar,
          registrationDate,
          phone,
          email,
        });
        localStorage.setItem('userStore', JSON.stringify(userStore.$state));
        router.push({
          name: (redirect as string) || 'Index',
          query: {
            ...othersQuery,
          },
        });
        Message.success(t('login.form.login.success'));
        if (loginWay.value === '1') {
          const { rememberPassword } = loginByPasswordConfig.value;
          const { username, password } = values;
          // 实际生产环境需要进行加密存储。
          loginByPasswordConfig.value.username = rememberPassword
            ? username
            : '';
          loginByPasswordConfig.value.password = rememberPassword
            ? password
            : '';
        }
      } catch (err) {
        errorMessage.value = (err as Error).message;
      } finally {
        setLoading(false);
      }
    }
  };

  const handleSendCode = async () => {
    try {
      codeInterval.codeInterval = 60;
      codeInterval.codeTimer = setInterval(() => {
        if (codeInterval.codeInterval >= 0) {
          codeInterval.codeInterval -= 1;
        } else {
          clearInterval(codeInterval.codeTimer);
        }
      }, 1000);
      const res = await userStore.verifyPhone(userCodeInfo.mobile);
    } catch (err) {
      errorMessage.value = (err as Error).message;
    } finally {
      setLoading(false);
    }
  };

  const setRememberPassword = (value: boolean) => {
    loginByPasswordConfig.value.rememberPassword = value;
  };

  const phoneRules = [
    {
      validator: (value, callback) => {
        return new Promise((resolve) => {
          window.setTimeout(() => {
            if (value === '') {
              callback(proxy.$t('login.form.phone.errMsg1'));
            } else if (!/1[3,4578][0-9]{9}/.test(value)) {
              callback(proxy.$t('login.form.phone.errMsg2'));
            }
            resolve();
          }, 1000);
        });
      },
    },
  ];

  const codeRules = [
    {
      required: true,
      validator: (value, callback) => {
        return new Promise((resolve) => {
          window.setTimeout(() => {
            value = userCodeInfo.code;
            if (value === '') {
              callback(proxy.$t('register.form.code.errMsg1'));
            } else if (!/\d{6}/.test(value)) {
              callback(proxy.$t('login.form.code.errMsg2'));
            }
            resolve();
          }, 1000);
        });
      },
      trigger: ['change', 'blur'],
    },
  ];

  const emailRules = [
    {
      required: false,
      validator: (value, callback) => {
        return new Promise((resolve) => {
          value = registerInfo.email;
          window.setTimeout(() => {
            if (!/.+@.+\..+/.test(value) && value !== '') {
              callback(proxy.$t('register.form.email.invalid'));
            }
            resolve();
          }, 1000);
        });
      },
    },
  ];
</script>
<style lang="less" scoped>
  .login-form {
    &-wrapper {
      width: 320px;
    }

    &-title {
      color: var(--color-text-1);
      font-weight: 500;
      font-size: 24px;
      line-height: 32px;
    }

    &-sub-title {
      color: var(--color-text-3);
      font-size: 16px;
      line-height: 24px;
    }

    &-error-msg {
      height: 32px;
      color: rgb(var(--red-6));
      line-height: 32px;
    }

    &-password-actions {
      display: flex;
      justify-content: space-between;
    }

    &-register-btn {
      color: var(--color-text-3) !important;
    }
  }
  #codeMargin {
    height: 24px;
  }
  ::v-deep(.arco-input-append) {
    padding: 0;
  }
</style>
