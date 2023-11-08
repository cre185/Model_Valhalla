<template>
  <div class="register-form-wrapper">
    <div class="register-form-title">{{ $t('register.form.title') }}</div>
    <div class="register-form-error-msg">{{ errorMessage }}</div>
    <a-form
      ref="registerForm"
      :model="registerInfo"
      class="register-form"
      layout="vertical"
      @submit="handleSubmit"
    >
      <a-form-item
        field="username"
        :rules="[{ required: true, message: $t('login.form.userName.errMsg') }]"
        :validate-trigger="['change', 'blur']"
        hide-label
      >
        <a-input
          v-model="registerInfo.username"
          :placeholder="$t('register.form.userName.placeholder')"
        >
          <template #prefix>
            <icon-user />
          </template>
        </a-input>
      </a-form-item>
      <a-form-item
        field="password"
        :rules="[{ required: true, message: $t('login.form.password.errMsg') }]"
        :validate-trigger="['change', 'blur']"
        hide-label
      >
        <a-input-password
          v-model="registerInfo.password"
          :placeholder="$t('register.form.password.placeholder')"
          allow-clear
        >
          <template #prefix>
            <icon-lock />
          </template>
        </a-input-password>
      </a-form-item>
      <a-form-item
          field="check-password"
          :rules="[{ required: true, message: $t('login.form.password.errMsg') }]"
          :validate-trigger="['change', 'blur']"
          hide-label
      >
        <a-input-password
            v-model="passwordValidation.passwordValidation"
            :placeholder="$t('register.form.checkPassword.placeholder')"
            allow-clear
        >
          <template #prefix>
            <icon-check-square />
          </template>
        </a-input-password>
      </a-form-item>
      <a-form-item
          field="phone"
          :rules="[{ required: true, message: $t('register.form.phone.errMsg') }]"
          :validate-trigger="['change', 'blur']"
          hide-label
      >
        <a-input
            v-model="registerInfo.phone"
            :placeholder="$t('register.form.phoneNumber.placeholder')"
            allow-clear
        >
          <template #prefix>
            <icon-phone />
          </template>
          <template #append>
            <a-button
                type="primary"
                v-if="codeInterval.codeInterval < 0"
                @click="codeInterval.codeInterval=60"
            >
              发送验证码
            </a-button>
            <a-button
                v-if="codeInterval.codeInterval >= 0"
            >
              {{codeInterval.codeInterval + 's 后重试'}}
            </a-button>
          </template>
        </a-input>
      </a-form-item>
      <a-form-item
          field="code"
          :rules="[{ required: true, message: $t('register.form.code.errMsg')}]"
          :validate-trigger="['change', 'blur']"
          hide-label
      >
        <a-input
            v-model="phoneValidation.phoneValidationCode"
            :placeholder="$t('register.form.code.placeholder')"
            allow-clear
        >
          <template #prefix>
            <icon-message />
          </template>
        </a-input>
      </a-form-item>
      <a-form-item
          field="email"
          hide-label
      >
        <a-input
            v-model="registerInfo.email"
            :placeholder="$t('register.form.email.placeholder')"
            :rules="rules"
            allow-clear
        >
          <template #prefix>
            <icon-email />
          </template>
        </a-input>
      </a-form-item>
      <a-space :size="16" direction="vertical">
        <div class="register-form-password-actions">
          <a-checkbox
            checked="acceptAgreement"
            :model-value="acceptAgreementInfo.acceptAgreement"
            @change="setAcceptAgreement"
          >
            {{ $t('register.form.agreement') }}
            <a-link>{{ $t('register.form.agreementName') }}</a-link>
            <a-link>{{ $t('register.form.privacy') }}</a-link>
          </a-checkbox>
        </div>
      </a-space>
      <a-button type="primary" html-type="submit" long :loading="loading">
        {{ $t('register.form.register') }}
      </a-button>
    </a-form>
  </div>
</template>

<script lang="ts" setup>
import {ref, reactive, onMounted, onBeforeUnmount} from 'vue';
  import { useRouter } from 'vue-router';
  import { ValidatedError } from '@arco-design/web-vue/es/form/interface';
  import { useI18n } from 'vue-i18n';
  import { useStorage } from '@vueuse/core';
  import { useUserStore } from '@/store';
  import useLoading from '@/hooks/loading';
  import type { LoginData } from '@/api/user';

  const router = useRouter();
  const errorMessage = ref('');
  const { loading, setLoading } = useLoading();
  const userStore = useUserStore();

  const registerConfig = useStorage('register-config', {
    username: '',
    password: '',
    phone: '',
    email: '',
  });
  const registerInfo = reactive({
    username: registerConfig.value.username,
    password: registerConfig.value.password,
    phone: registerConfig.value.phone,
    email: registerConfig.value.email,
  });
  const acceptAgreementInfo = reactive({
    acceptAgreement: false,
  });

  const passwordValidation = reactive({
    passwordValidation: '',
  });

  const phoneValidation = reactive({
    phoneValidationCode: '',
  });

  const codeInterval = reactive({
    codeTimer: null as null | ReturnType<typeof setInterval>,
    codeInterval: -1,
  })

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
          name: (redirect as string) || 'Login',
          query: {
            ...othersQuery,
          },
        });
      } catch (err) {
        errorMessage.value = (err as Error).message;
      } finally {
        setLoading(false);
      }
    }
  };
  const setAcceptAgreement = (value: boolean) => {
    acceptAgreementInfo.acceptAgreement = value;
  };

  // 设置验证码计时器
  onMounted(() => {
    codeInterval.codeTimer = setInterval(() => {
      if(codeInterval.codeInterval >= 0){
        codeInterval.codeInterval -= 1;
      }
    }, 1000);
  });

  onBeforeUnmount(() => {
    if(codeInterval.codeTimer)
      clearInterval(codeInterval.codeTimer);
  });

  const rules = [{
    validator: (value: any, cb: (arg: string) => void) => {
      return new Promise<void>(resolve => {
        window.setTimeout(() => {
          if (!/.+@.+\..+/.test(value)) {
            cb('Email is not valid')
          }
          resolve()
        }, 2000)
      })
    }
  }];

</script>

<style lang="less" scoped>
  .register-form {
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
  ::v-deep(.arco-input-append) {
    padding: 0;
  }
</style>
