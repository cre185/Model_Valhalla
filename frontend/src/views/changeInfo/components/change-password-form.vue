<template>
  <div class="login-form-wrapper">
    <div class="login-form-title">{{ $t('change.form.title') }}</div>
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
          :placeholder="$t('change.form.phone.placeholder')"
        >
          <template #prefix>
            <icon-phone />
          </template>
        </a-input>
      </a-form-item>
      <a-form-item
        field="code"
        :rules="codeRules"
        :validate-trigger="['change', 'blur']"
        hide-label
      >
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
                codeInterval.codeInterval + $t('register.form.code.buttonText2')
              }}
            </a-button>
          </template>
        </a-input>
      </a-form-item>
      <a-form-item
        field="mobile"
        :rules="phoneRules"
        :validate-trigger="['change', 'blur']"
        hide-label
      >
        <a-input
          v-model="userCodeInfo.mobile"
          :placeholder="$t('change.form.password.placeholder')"
        >
          <template #prefix>
            <icon-lock />
          </template>
        </a-input>
      </a-form-item>
      <a-form-item
        field="mobile"
        :rules="phoneRules"
        :validate-trigger="['change', 'blur']"
        hide-label
      >
        <a-input
          v-model="userCodeInfo.mobile"
          :placeholder="$t('change.form.password_again.placeholder')"
        >
          <template #prefix>
            <icon-safe />
          </template>
        </a-input>
      </a-form-item>
      <a-space :size="5" direction="vertical">
        <a-row class="row">
          <a-col :span="2">
            <icon-check-circle-fill />
          </a-col>
          <a-col :span="22">
            <span> 密码由6-32位数字、字母或符号(_和-)组成 </span>
          </a-col>
        </a-row>
        <a-row class="row">
          <a-col :span="2">
            <icon-check-circle-fill />
          </a-col>
          <a-col :span="22">
            <span> 安全提示：新密码请勿与旧密码过于相似 </span>
          </a-col>
        </a-row>
      </a-space>
      <a-space :size="16" direction="vertical">
        <div id="codeMargin"></div>
        <router-link to="../login">
          <a-button type="primary" html-type="submit" long :loading="loading">
            {{ $t('change.form.acknowledge') }}
          </a-button>
        </router-link>
        <a-button
          type="text"
          long
          class="login-form-register-btn"
          @click="goBack"
        >
          {{ $t('change.form.return') }}
        </a-button>
      </a-space>
    </a-form>
  </div>
</template>

<script lang="ts" setup>
  import { ref, reactive, getCurrentInstance, inject } from 'vue';
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
  const loginByCodeConfig = useStorage('login-by-code-config', {
    mobile: '18678901234',
    code: '',
  });
  const userPassInfo = reactive({
    username: loginByPasswordConfig.value.username,
    password: loginByPasswordConfig.value.password,
  });
  const userCodeInfo = reactive({
    mobile: loginByCodeConfig.value.mobile,
    code: loginByCodeConfig.value.code,
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
      validator: (
        value: string | undefined,
        callback: (argument: string) => void
      ) => {
        return new Promise((resolve) => {
          window.setTimeout(() => {
            if (value === undefined) {
              callback(proxy.$t('change.form.phone.errMsg1'));
            } else if (!/^1[3-9]\d{9}$/.test(value)) {
              callback(proxy.$t('login.form.phone.errMsg2'));
            }
            resolve(undefined);
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

  const goBack = () => {
    router.go(-1);
  };
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

  .row {
    color: grey;
    align-items: baseline;
  }
</style>
