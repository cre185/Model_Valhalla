<template>
  <div class="login-form-wrapper">
    <div class="login-form-title">{{ $t('login.form.title') }}</div>
    <a-tabs :justify="true">
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
            field="phone"
            :rules="[
              { required: true, message: $t('login.form.phone.errMsg') },
            ]"
            :validate-trigger="['change', 'blur']"
            hide-label
          >
            <a-input
              v-model="userCodeInfo.phone"
              :placeholder="$t('login.form.phone.placeholder')"
            >
              <template #prefix>
                <icon-phone />
              </template>
            </a-input>
          </a-form-item>
          <a-form-item
            field="code"
            :rules="[{ required: true, message: $t('register.form.code.errMsg') }]"
            :validate-trigger="['change', 'blur']"
            hide-label
          >
            <a-input-search
              v-model="userCodeInfo.code"
              :placeholder="$t('register.form.code.placeholder')"
              allow-clear
              button-text="发送验证码"
              search-button
            >
              <template #prefix>
                <icon-message />
              </template>
            </a-input-search>
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
  import { ref, reactive } from 'vue';
  import { useRouter } from 'vue-router';
  import { Message } from '@arco-design/web-vue';
  import { ValidatedError } from '@arco-design/web-vue/es/form/interface';
  import { useI18n } from 'vue-i18n';
  import { useStorage } from '@vueuse/core';
  import { useUserStore } from '@/store';
  import useLoading from '@/hooks/loading';
  import type { LoginData } from '@/api/user';

  const router = useRouter();
  const { t } = useI18n();
  const errorMessage = ref('');
  const { loading, setLoading } = useLoading();
  const userStore = useUserStore();

  const loginByPasswordConfig = useStorage('login-by-password-config', {
    rememberPassword: true,
    username: 'admin', // 演示默认值
    password: 'admin', // demo default value
  });
  const loginByCodeConfig = useStorage('login-by-code-config', {
    phone: '18678901234',
    code: '',
  });
  const userPassInfo = reactive({
    username: loginByPasswordConfig.value.username,
    password: loginByPasswordConfig.value.password,
  });
  const userCodeInfo = reactive({
    phone: loginByCodeConfig.value.phone,
    code: loginByCodeConfig.value.code,
  });

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
        await userStore.login(values as LoginData);
        const { redirect, ...othersQuery } = router.currentRoute.value.query;
        router.push({
          name: (redirect as string) || 'Index',
          query: {
            ...othersQuery,
          },
        });
        Message.success(t('login.form.login.success'));
        const { rememberPassword } = loginByPasswordConfig.value;
        const { username, password } = values;
        // 实际生产环境需要进行加密存储。
        // The actual production environment requires encrypted storage.
        loginByPasswordConfig.value.username = rememberPassword ? username : '';
        loginByPasswordConfig.value.password = rememberPassword ? password : '';
      } catch (err) {
        errorMessage.value = (err as Error).message;
      } finally {
        setLoading(false);
      }
    }
  };
  const setRememberPassword = (value: boolean) => {
    loginByPasswordConfig.value.rememberPassword = value;
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
  #codeMargin{
    height: 24px;
  }
</style>
