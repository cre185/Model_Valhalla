<template>
  <div class="change-phone-form-wrapper">
    <div class="change-phone-form-title">{{ $t('change.phone.form.title') }}</div>
    <div class="change-phone-form-sub-title" v-if="!verifiedPhone">{{ $t('change.phone.form.subtitle1') }}</div>
    <div class="change-phone-form-sub-title" v-else>{{ $t('change.phone.form.subtitle2') }}</div>
    <div class="change-phone-form-error-msg">{{ errorMessage }}</div>
    <a-form
        :model="phoneVerification"
        layout="vertical"
        v-if="!verifiedPhone"
    >
      <PhoneInputForm :input_type="'mobile'"
                      v-model:mobile="phoneVerification.phone"
                      :mobile_read_only="true"
                      :email_read_only="false"
                      v-model:code="phoneVerification.code"
                      v-model:error_message="errorMessage"
                      @update:code="(value: string) => { phoneVerification.code = value;}"
                      @update:error_message="(value: string) => { errorMessage = value;}"
      />
      <a-space :size="16" direction="vertical">
        <a-button type="primary" @click="handleVerifyCode" long :loading="loading">
          {{ $t('change.phone.form.verify') }}
        </a-button>
        <a-button type="text"
                  @click="router.push({ name: 'Setting'});"
                  long class="change-phone-form-back-btn">
          {{ $t('change.phone.form.back') }}
        </a-button>
      </a-space>
    </a-form>
    <a-form
        :model="changedSecurityPhoneVerification"
        layout="vertical"
        v-else
    >
      <PhoneInputForm :input_type="'mobile'"
                      v-model:mobile="changedSecurityPhoneVerification.phone"
                      :mobile_read_only="false"
                      :email_read_only="false"
                      v-model:code="changedSecurityPhoneVerification.code"
                      v-model:error_message="errorMessage"
                      @update:mobile="(value: string) => { changedSecurityPhoneVerification.mobile = value;}"
                      @update:code="(value: string) => { changedSecurityPhoneVerification.code = value;}"
                      @update:error_message="(value: string) => { errorMessage = value;}"
      />
      <a-space :size="16" direction="vertical">
        <a-button type="primary" @click="handleChangeSecurityPhone" long :loading="loading">
          {{ $t('change.phone.form.change') }}
        </a-button>
        <a-button type="text"
                  @click="router.push({ name: 'Setting'});"
                  long class="change-phone-form-back-btn">
          {{ $t('change.phone.form.back') }}
        </a-button>
      </a-space>
    </a-form>
  </div>
</template>

<script lang="ts" setup>
  import PhoneInputForm from "@/views/changeInfo/components/verification-input-form.vue";
  import { ref, reactive, getCurrentInstance } from 'vue';
  import { useRouter } from 'vue-router';
  import { ValidatedError } from '@arco-design/web-vue/es/form/interface';
  import { useI18n } from 'vue-i18n';
  import { useUserStore } from '@/store';
  import useLoading from '@/hooks/loading';
  import {phoneVerifyData, verifyCode} from '@/api/user';
  import { updateInfo } from "@/api/user-info";
  import {getToken} from "@/utils/auth";
  import { Modal } from '@arco-design/web-vue';

  const router = useRouter();
  const { t } = useI18n();
  const { loading, setLoading } = useLoading();
  const userStore = useUserStore();
  const errorMessage = ref('');
  const verifiedPhone = ref(false);
  userStore.setInfo(JSON.parse(localStorage.getItem('userStore')!));
  const phoneVerification = reactive({
    phone: userStore.phone,
    code:'',
  })
  const changedSecurityPhoneVerification = reactive({
    phone: '',
    code: '',
  })
  const handleVerifyCode = async ({
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
        await verifyCode({mobile: phoneVerification.phone, code: phoneVerification.code} as phoneVerifyData);
        verifiedPhone.value = true;
        errorMessage.value = '';
      } catch (err) {
        errorMessage.value = (err as Error).message;
        verifiedPhone.value = false;
      } finally {
        setLoading(false);
      }
    }
  }
  const handleChangeSecurityPhone = async ({
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
        await verifyCode({mobile: changedSecurityPhoneVerification.phone, code: changedSecurityPhoneVerification.code} as phoneVerifyData);
        await updateInfo(userStore.accountId!, getToken()!, {key: changedSecurityPhoneVerification.phone}, 'mobile');
        userStore.phone = changedSecurityPhoneVerification.phone;
        localStorage.setItem('userStore', JSON.stringify(userStore.$state));
        let returnInterval = 3;
        let returnTimer: ReturnType<typeof setInterval> | undefined;
        const modal = Modal.success({
          title: ' ',
          content: t('change.phone.form.success'),
          okText: t('change.phone.form.back'),
          onOpen: () => {
            returnTimer = setInterval(() => {
            if (returnInterval >= 0) {
              console.log(returnInterval);
              returnInterval -= 1;
            } else {
              clearInterval(returnTimer);
              router.push({ name: 'Setting'});
              modal.close();
            }
          }, 1000);},
          onOk: () => {
            clearInterval(returnTimer);
            router.push({ name: 'Setting'});
            modal.close();
          },
          bodyStyle: 'display: flex; align-items: center; justify-content: center; font-size: 24px;',
        });
      } catch (err) {
        errorMessage.value = (err as Error).message;
      } finally {
        setLoading(false);
      }
    }
  }
</script>

<style scoped lang="less">
.change-phone-form{
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

  &-error-msg {
    height: 32px;
    color: rgb(var(--red-6));
    line-height: 32px;
  }

  &-register-btn {
    color: var(--color-text-3) !important;
  }
}
</style>
