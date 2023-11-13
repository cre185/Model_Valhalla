<template>
  <div class="change-email-form-wrapper">
    <div class="change-email-form-title">{{ $t('change.email.form.title') }}</div>
    <div class="change-email-form-sub-title" v-if="!verifiedPhone">{{ $t('change.email.form.subtitle1') }}</div>
    <div class="change-email-form-sub-title" v-else>{{ $t('change.email.form.subtitle2') }}</div>
    <div class="change-email-form-error-msg">{{ errorMessage }}</div>
    <a-form
        ref="loginForm"
        :model="phoneVerification"
        class="login-form"
        layout="vertical"
        @submit="handleVerifyCode"
    >
      <PhoneInputForm v-model:mobile="phoneVerification.phone"
                      v-model:code.sync="phoneVerification.code"
                      v-model:error_message.sync="errorMessage"/>
      <a-space :size="16" direction="vertical">
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
  </div>
</template>

<script lang="ts" setup>
  import PhoneInputForm from "@/views/changeInfo/components/phone-input-form.vue";
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
  const verifiedPhone = ref(false);
  const phoneVerification = reactive({
    phone: '',
    code:'',
  })

  const handleVerifyCode = async ({
    errors,
    values,
  }: {
    errors: Record<string, ValidatedError> | undefined;
    values: Record<string, any>;
  }) => {

  };
</script>

<style scoped lang="less">
  .change-email-form{
    &-wrapper{
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
      line-height: 50px;
    }
  }
</style>
