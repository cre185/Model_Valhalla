<template>
  <div class="register-form-type-selector" v-if="userType === ''">
    <a-space direction="vertical" :size="60" :align="'center'">
      <div class="register-form-type-selector-title">
        {{$t('register.form.typeSelector.title')}}
      </div>
      <a-space :size="'large'">
        <a-button type="primary" shape="round" class="register-form-type-selector-user-btn" @click="userType= 'user'">
          <template #icon>
            <icon-user />
          </template>
          {{$t('register.form.user.buttonText')}}
        </a-button>
        <a-button type="primary" shape="round" class="register-form-type-selector-admin-btn" @click="userType = 'administrator'">
          <template #icon>
            <icon-customer-service />
          </template>
          {{$t('register.form.administrator.buttonText')}}
        </a-button>
      </a-space>
    </a-space>
  </div>
  <div class="register-form-wrapper" v-if="userType !== ''">
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
        :rules="usernameRules"
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
        :rules="passwordRules"
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
          :rules="passwordValidationRules"
          :validate-trigger="['change', 'blur']"
          hide-label
      >
        <a-input-password
            v-model="passwordValidation.passwordValidation"
            :placeholder="$t('register.form.passwordValidation.placeholder')"
            allow-clear
        >
          <template #prefix>
            <icon-check-square />
          </template>
        </a-input-password>
      </a-form-item>
      <a-form-item
          field="mobile"
          :rules="phoneRules"
          hide-label
      >
        <a-input
            v-model="registerInfo.mobile"
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
                @click="handleSendCode"
            >
              {{$t('register.form.code.buttonText1')}}
            </a-button>
            <a-button
                v-if="codeInterval.codeInterval >= 0"
            >
              {{codeInterval.codeInterval + $t('register.form.code.buttonText2')}}
            </a-button>
          </template>
        </a-input>
      </a-form-item>
      <a-form-item
          field="code"
          :rules="codeRules"
          hide-label
      >
        <a-input
            v-model="phoneValidation.code"
            :placeholder="$t('register.form.code.placeholder')"
            allow-clear
        >
          <template #prefix>
            <icon-message />
          </template>
        </a-input>
      </a-form-item>
      <a-form-item
          field="adminCode"
          :rules="adminCodeRules"
          hide-label
          v-if="userType === 'administrator'"
      >
        <a-input
            v-model="adminCode"
            :placeholder="$t('register.form.adminCode.placeholder')"
            allow-clear
        >
          <template #prefix>
            <icon-bookmark />
          </template>
        </a-input>
      </a-form-item>
      <a-form-item
          field="email"
          :rules="emailRules"
          hide-label
      >
        <a-input
            v-model="registerInfo.email"
            :placeholder="$t('register.form.email.placeholder')"
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
        <a-button type="primary" html-type="submit" long :loading="loading">
          {{ $t('register.form.register') }}
        </a-button>
        <a-button type="text" long class="login-form-register-btn" @click="userType=''">
          {{ $t('register.form.return.btn') }}
        </a-button>
      </a-space>
    </a-form>
  </div>
</template>

<script lang="ts" setup>
import {ref, reactive, onMounted, onBeforeUnmount, getCurrentInstance} from 'vue';
  import { useRouter } from 'vue-router';
  import { ValidatedError } from '@arco-design/web-vue/es/form/interface';
  import { useStorage } from '@vueuse/core';
  import { useUserStore } from '@/store';
  import useLoading from '@/hooks/loading';
  import type { LoginData, phoneVerifyData , registerData} from '@/api/user';
import error from "@/views/result/error/index.vue";

  const router = useRouter();
  const errorMessage = ref('');
  const { loading, setLoading } = useLoading();
  const userStore = useUserStore();
  const { proxy } = getCurrentInstance()

  const registerConfig = useStorage('register-config', {
    username: '',
    password: '',
    mobile: '',
    email: '',
  });
  const registerInfo = reactive({
    username: registerConfig.value.username,
    password: registerConfig.value.password,
    mobile: registerConfig.value.mobile,
    email: registerConfig.value.email,
  });
  const acceptAgreementInfo = reactive({
    acceptAgreement: false,
  });

  const passwordValidation = reactive({
    passwordValidation: '',
  });

  const phoneValidation = reactive({
    code: '',
  });

  const codeInterval = reactive({
    codeTimer: null as null | ReturnType<typeof setInterval>,
    codeInterval: -1,
  })

  const userType = ref('');
  const adminCode = ref('');
  const invitationCode = new Set(['TXNKvJ#1', '&I&IKZO7', 'u&%ONBea',
                                        'KF0jhFN0', 't1NNob8!', 'QNyKOY$w',
                                        '&%o^YOt#', '4PGX33aX', 'rc@$t#Of', 'L!hf_TIk'])

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
        if(!acceptAgreementInfo.acceptAgreement)
          throw new Error(proxy.$t('register.form.agreement.errMsg'))
        if(userType.value === 'administrator')
          values.is_admin = 1;
        const phoneVerification = {mobile: registerInfo.mobile, code: phoneValidation.code}
        await userStore.verifyCode(phoneVerification as phoneVerifyData);
        await userStore.register(values as registerData);
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
  // 发送验证码函数
  const handleSendCode = async () => {
    try {
      codeInterval.codeInterval = 60
      codeInterval.codeTimer = setInterval(() => {
        if(codeInterval.codeInterval >= 0){
          codeInterval.codeInterval -= 1;
        }
        else{
          clearInterval(codeInterval.codeTimer);
        }
      }, 1000);
    const res = await userStore.verifyPhone(registerInfo.mobile);
    } catch (err) {
      errorMessage.value = (err as Error).message;
    } finally {
      setLoading(false);
    }
  };

  const setAcceptAgreement = (value: boolean) => {
    acceptAgreementInfo.acceptAgreement = value;
  };

  // 表单信息验证
  const usernameRules = [{
    validator: (value, callback) => {
      return new Promise(resolve => {
        window.setTimeout(() => {
          if(value === ''){
            callback(proxy.$t('register.form.userName.errMsg1'))
          }
          else if (value.length < 6) {
            callback(proxy.$t('register.form.userName.errMsg2'))
          }
          resolve()
        }, 1000)
      })
    },
  }];

  const passwordRules = [{
    validator: (value, callback) => {
      return new Promise(resolve => {
        window.setTimeout(() => {
          if(value === ''){
            callback(proxy.$t('register.form.password.errMsg1'))
          }
          else if (value.length < 8) {
            callback(proxy.$t('register.form.password.errMsg2'))
          }
          resolve()
        }, 1000)
      })
    },
  }];

  const passwordValidationRules = [{
    validator: (value, callback) => {
      return new Promise(resolve => {
        window.setTimeout(() => {
          value = passwordValidation.passwordValidation
          if(value === ''){
            callback(proxy.$t('register.form.passwordValidation.errMsg1'))
          }
          else if (value !== registerInfo.password) {
            callback(proxy.$t('register.form.passwordValidation.errMsg2'))
          }
          resolve()
        }, 1000)
      })
    },
  }];

  const phoneRules = [{
    validator: (value, callback) => {
      return new Promise(resolve => {
        window.setTimeout(() => {
          if(value === ''){
            callback(proxy.$t('register.form.phone.errMsg1'))
          }
          else if (!/1[3,4,5,7,8][0-9]{9}/.test(value)) {
            callback(proxy.$t('register.form.phone.errMsg2'))
          }
          resolve()
        }, 1000)
      })
    },
  }];

  const codeRules = [{
    required: true,
    validator: (value, callback) => {
      return new Promise(resolve => {
        window.setTimeout(() => {
          value = phoneValidation.code
          if(value === ''){
            callback(proxy.$t('register.form.code.errMsg1'))
          }
          else if (!/\d{6}/.test(value)) {
            callback(proxy.$t('register.form.code.errMsg2'))
          }
          resolve()
        }, 1000)
      })
    },
    trigger: ['change', 'blur'],
  }];

  const adminCodeRules = [{
    required: true,
    validator: (value, callback) => {
      return new Promise(resolve => {
        window.setTimeout(() => {
          value = adminCode.value
          if(value === ''){
            callback(proxy.$t('register.form.adminCode.errMsg1'))
          }
          else if (!invitationCode.has(value)) {
            callback(proxy.$t('register.form.adminCode.errMsg2'))
          }
          resolve()
        }, 1000)
      })
    },
    trigger: ['change', 'blur'],
  }];

  const emailRules = [{
    required: false,
    validator: (value, callback) => {
      return new Promise(resolve => {
        value = registerInfo.email
        window.setTimeout(() => {
          if (!/.+@.+\..+/.test(value) && value !== '') {
            callback(proxy.$t('register.form.email.invalid'))
          }
          resolve()
        }, 1000)
      })
    },
  }];
</script>

<style lang="less" scoped>
  .register-form {
    &-wrapper {
      width: 320px;
    }

    &-title, &-type-selector-title{
      color: var(--color-text-1);
      font-weight: 500;
      font-size: 24px;
      line-height: 32px;
    }

    &-type-selector-title{
      display: flex;
      justify-content: center;
      align-items: center;
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
