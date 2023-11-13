<template>
  <a-form-item
      field="mobile"
      :rules="phoneRules"
      :validate-trigger="['change', 'blur']"
      hide-label
  >
    <a-input
        v-model="model.mobile"
        :placeholder="$t('login.form.phone.placeholder')"
    >
      <template #prefix>
        <icon-phone />
      </template>
    </a-input>
  </a-form-item>
  <a-form-item field="code" :rules="codeRules" hide-label>
    <a-input
        v-model="model.code"
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
</template>

<script lang="ts" setup>
import {getCurrentInstance, reactive} from "vue";
  import { useI18n } from 'vue-i18n';
  import useLoading from "@/hooks/loading";
  import {useUserStore} from "@/store";

  const props = defineProps(['mobile', 'code', 'error_message']);
  const { loading, setLoading } = useLoading();
  const { t } = useI18n();
  const userStore = useUserStore();
  const { proxy } = getCurrentInstance()!;
  const emits = defineEmits(['update:mobile', 'update:code', 'update:error_message']);

  const model = reactive({
    mobile: props.mobile,
    code: props.code
  });

  const modelListeners = {
    updateMobile: (value: string) => emits('update:mobile', value),
    updateCode: (value: string) => emits('update:code', value)
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
      const res = await userStore.verifyPhone(props.mobile);
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

  const codeRules = [
    {
      required: true,
      validator: (value, callback) => {
        return new Promise((resolve) => {
          window.setTimeout(() => {
            if (value === '') {
              callback(t('register.form.code.errMsg1'));
            } else if (!/\d{6}/.test(value)) {
              callback(t('login.form.code.errMsg2'));
            }
            resolve();
          }, 1000);
        });
      },
      trigger: ['change', 'blur'],
    },
  ];
</script>

<style scoped>

</style>
