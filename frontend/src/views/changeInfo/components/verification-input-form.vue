<template>
  <a-form-item
      field="mobile"
      :rules="phoneRules"
      :validate-trigger="['change', 'blur']"
      hide-label
      v-if="props.input_type === 'mobile'"
  >
    <a-input
        v-model="model.mobile"
        :placeholder="$t('login.form.phone.placeholder')"
        :style="{ 'pointer-events': props.mobile_read_only ? 'none' : 'auto' }"
        @update:modelValue="modelListeners.updateMobile"
    >
      <template #prefix>
        <icon-phone />
      </template>
    </a-input>
  </a-form-item>
  <a-form-item
      field="email"
      :rules="emailRules"
      :validate-trigger="['change', 'blur']"
      hide-label
      v-if="props.input_type === 'email'"
  >
    <a-input
        v-model="model.email"
        :placeholder="$t('register.form.email.placeholder')"
        :style="{ 'pointer-events': props.email_read_only ? 'none' : 'auto' }"
        @update:modelValue="modelListeners.updateEmail"
    >
      <template #prefix>
        <icon-email />
      </template>
    </a-input>
  </a-form-item>
  <a-form-item field="code" :rules="codeRules" hide-label>
    <a-input
        v-model="model.code"
        :placeholder="$t('login.form.code.placeholder')"
        allow-clear
        @update:modelValue="modelListeners.updateCode"
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
</template>

<script lang="ts" setup>
import { getCurrentInstance, reactive } from "vue";
  import { useI18n } from 'vue-i18n';
  import useLoading from "@/hooks/loading";
  import { useUserStore } from "@/store";

  const props = defineProps(['input_type', 'mobile', 'email', 'mobile_read_only',
                                    'email_read_only', 'code', 'error_message']);
  const { loading, setLoading } = useLoading();
  const { t } = useI18n();
  const userStore = useUserStore();
  const { proxy } = getCurrentInstance()!;

  const model = reactive({
    mobile: props.mobile_read_only ? `${props.mobile.slice(0, 3)}${'*'.repeat(6)}${props.mobile.slice(-2)}` : props.mobile,
    email: props.email_read_only ? `${props.mobile.slice(0, 3)}${'*'.repeat(props.email.length)}` : props.email,
    code: props.code
  });

  const modelListeners = {
    updateMobile (value: string) {
      model.mobile = value;
      proxy!.$emit('update:mobile', value);
    },
    updateEmail (value: string) {
      model.email = value;
      proxy!.$emit('update:email', value);
    },
    updateCode (value: string) {
      model.code = value;
      proxy!.$emit('update:code', value);
    }
  };

  const codeInterval = reactive({
    codeTimer: null as null | ReturnType<typeof setInterval>,
    codeInterval: -1,
  });

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
      if(props.input_type === 'mobile'){
        await userStore.verifyPhone(props.mobile);
      }
      else if(props.input_type === 'email'){
        await userStore.verifyEmail(props.email);
      }
    } catch (err) {
      proxy!.$emit('update:error_message.value', '(err as Error).message');
    } finally {
      setLoading(false);
    }
  };

  const phoneRules = [
    {
      validator: (value, callback) => {
        return new Promise((resolve) => {
          if(props.mobile_read_only)
            return;
          window.setTimeout(() => {
            if (value === '') {
              callback(t('login.form.phone.errMsg1'));
            } else if (!/1[3,4578][0-9]{9}/.test(value)) {
              callback(t('login.form.phone.errMsg2'));
            }
            resolve();
          }, 1000);
        });
      },
    },
  ];

  const emailRules = [
    {
      required: false,
      validator: (value, callback) => {
        return new Promise((resolve) => {
          value = model.email;
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

  const codeRules = [
    {
      required: true,
      validator: (value, callback) => {
        return new Promise((resolve) => {
          window.setTimeout(() => {
            value = model.code;
            if (value === '') {
              callback(t('register.form.code.errMsg1'));
            } else if (!/\d{6}/.test(value)) {
              callback(t('register.form.code.errMsg2'));
            }
            resolve();
          }, 1000);
        });
      },
    },
  ];
</script>

<style scoped>
  ::v-deep(.arco-input-append) {
    padding: 0;
  }
</style>
