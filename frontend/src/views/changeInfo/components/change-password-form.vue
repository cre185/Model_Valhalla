<template>
  <div class="login-form-wrapper">
    <div class="login-form-title">{{ $t('change.form.title') }}</div>
    <div class="login-form-error-msg">{{ errorMessage }}</div>
    <a-form
      ref="changeForm"
      :model="userChangeInfo"
      class="login-form"
      layout="vertical"
      @submit="handleSubmit"
    >
      <PhoneInputForm :input_type="'mobile'"
                      v-model:mobile="userChangeInfo.mobile"
                      :mobile_read_only="$route.params.mobileReadOnly === '1'"
                      :email_read_only="false"
                      v-model:code="userChangeInfo.code"
                      v-model:error_message="errorMessage"
                      @update:mobile="(value: string) => { userChangeInfo.mobile = value;}"
                      @update:code="(value: string) => { userChangeInfo.code = value;}"
                      @update:error_message="(value: string) => { errorMessage = value;}"
      />
      <a-form-item
        field="firstPassword"
        :rules="firstPasswordRules"
        :validate-trigger="['change', 'blur']"
        hide-label
      >
        <a-input-password
          v-model="userChangeInfo.firstPassword"
          :placeholder="$t('change.form.password.placeholder')"
        >
          <template #prefix>
            <icon-lock />
          </template>
        </a-input-password>
      </a-form-item>
      <a-form-item
        field="secondPassword"
        :rules="secondPasswordRules"
        :validate-trigger="['change', 'blur']"
        hide-label
      >
        <a-input-password
          v-model="userChangeInfo.secondPassword"
          type="password"
          :placeholder="$t('change.form.password_again.placeholder')"
        >
          <template #prefix>
            <icon-safe />
          </template>
        </a-input-password>
      </a-form-item>
      <a-space :size="5" direction="vertical">
        <a-row class="row">
          <a-col :span="2">
            <icon-check-circle-fill />
          </a-col>
          <a-col :span="22">
            <span> {{ $t('login.form.rule') }} </span>
          </a-col>
        </a-row>
        <a-row class="row">
          <a-col :span="2">
            <icon-check-circle-fill />
          </a-col>
          <a-col :span="22">
            <span> {{ $t('login.form.hint') }} </span>
          </a-col>
        </a-row>
      </a-space>
      <a-space :size="16" direction="vertical">
        <div id="codeMargin"></div>
        <a-button type="primary" html-type="submit" long :loading="loading">
          {{ $t('change.form.acknowledge') }}
        </a-button>
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
  import { ref, reactive, getCurrentInstance, onMounted } from 'vue';
  import PhoneInputForm from "@/views/changeInfo/components/verification-input-form.vue";
  import { useRouter } from 'vue-router';
  import { Modal } from '@arco-design/web-vue';
  import { ValidatedError } from '@arco-design/web-vue/es/form/interface';
  import { useI18n } from 'vue-i18n';
  import { useUserStore } from '@/store';
  import useLoading from '@/hooks/loading';
  import { getPassword, updateInfo } from '@/api/user-info';
  import { getToken } from '@/utils/auth';
  import { phoneVerifyData } from '@/api/user';

  const router = useRouter();
  const { t } = useI18n();
  const errorMessage = ref('');
  const { loading, setLoading } = useLoading();
  const userStore = useUserStore();
  userStore.setInfo(JSON.parse(localStorage.getItem('userStore')!));
  const { proxy } = getCurrentInstance();

  const userChangeInfo = reactive({
    mobile: userStore.phone,
    code: '',
    firstPassword: '',
    secondPassword: '',
  });

  const oldPassword = ref('');
  const changeForm = ref();
  const codeInterval = reactive({
    codeTimer: null as null | ReturnType<typeof setInterval>,
    codeInterval: -1,
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
        const phoneVerification = {
          mobile: userChangeInfo.mobile,
          code: userChangeInfo.code,
        };
        await userStore.verifyCode(phoneVerification as phoneVerifyData);
        await updateInfo(
          userStore.accountId!,
          getToken()!,
          {
            key: userChangeInfo.firstPassword,
          },
          'password'
        );
        let returnInterval = 3;
        let returnTimer: ReturnType<typeof setInterval> | undefined;
        const modal = Modal.success({
          title: '',
          content: t('change.form.change.success'),
          okText: t('change.form.return'),
          onOpen: () => {
            returnTimer = setInterval(() => {
              if (returnInterval >= 0) {
                console.log(returnInterval);
                returnInterval -= 1;
              } else {
                clearInterval(returnTimer);
                router.back();
                modal.close();
              }
            }, 1000);
          },
          onOk: () => {
            clearInterval(returnTimer);
            router.back();
            modal.close();
          },
        });
      } catch (err) {
        errorMessage.value = t('change.form.change.error');
        setTimeout(() => {
          errorMessage.value = '';
        }, 5000);
      } finally {
        setLoading(false);
      }
    }
  };

  const firstPasswordRules = [
    {
      validator: (
        value: string | undefined,
        callback: (argument: string) => void
      ) => {
        return new Promise((resolve) => {
          window.setTimeout(() => {
            if (value === undefined) {
              callback(proxy.$t('change.form.password.errMsg1'));
            } else if (!/^[a-zA-Z0-9_-]{6,32}$/.test(value)) {
              callback(proxy.$t('change.form.password.errMsg2'));
            } else if (oldPassword.value !== '' && value === oldPassword.value) {
              callback(proxy.$t('change.form.password.errMsg3'));
            }
            resolve(undefined);
          }, 1000);
        });
      },
    },
  ];

  const secondPasswordRules = [
    {
      validator: (
        value: string | undefined,
        callback: (argument: string) => void
      ) => {
        return new Promise((resolve) => {
          window.setTimeout(() => {
            if (value === undefined) {
              callback(proxy.$t('change.form.password_again.errMsg1'));
            } else if (value !== userChangeInfo.firstPassword) {
              callback(proxy.$t('change.form.password_again.errMsg2'));
            }
            resolve(undefined);
          }, 1000);
        });
      },
    },
  ];

  const goBack = () => {
    router.back();
  };

  onMounted(async () => {
    if (userStore.accountId !== undefined)
    {
      oldPassword.value = await getPassword(userStore.accountId, getToken()!);
    }
  });
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
