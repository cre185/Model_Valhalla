<template>
  <a-list :bordered="false">
    <a-list-item>
      <a-list-item-meta>
        <template #avatar>
          <a-typography-paragraph>
            {{ $t('userSetting.SecuritySettings.form.label.username') }}
          </a-typography-paragraph>
        </template>
        <template #description>
          <div class="content">
            <a-input
              v-show="changeUsername"
              id="input"
              ref="inputRef"
              v-model="userStore.username"
              :placeholder="userStore.username"
              @press-enter="saveUsername"
              @blur="saveUsername"
            />
            <a-typography-paragraph v-show="!changeUsername">
              {{ userStore.username }}
            </a-typography-paragraph>
          </div>
          <div class="operation">
            <a-link @click="changeUsernameFunc">
              {{ $t('userSetting.SecuritySettings.button.update') }}
            </a-link>
          </div>
        </template>
      </a-list-item-meta>
    </a-list-item>
    <a-list-item>
      <a-list-item-meta>
        <template #avatar>
          <a-typography-paragraph>
            {{ $t('userSetting.SecuritySettings.form.label.password') }}
          </a-typography-paragraph>
        </template>
        <template #description>
          <div class="content">
            <a-typography-paragraph>
              {{ $t('userSetting.SecuritySettings.placeholder.password') }}
            </a-typography-paragraph>
          </div>
          <div class="operation">
            <a-link @click="changePasswordFunc">
              {{ $t('userSetting.SecuritySettings.button.update') }}
            </a-link>
          </div>
        </template>
      </a-list-item-meta>
    </a-list-item>
    <a-list-item>
      <a-list-item-meta>
        <template #avatar>
          <a-typography-paragraph>
            {{ $t('userSetting.SecuritySettings.form.label.phone') }}
          </a-typography-paragraph>
        </template>
        <template #description>
          <div class="content">
            <a-typography-paragraph v-model="maskedPhone">
              已绑定：{{ maskedPhone }}
            </a-typography-paragraph>
          </div>
          <div class="operation">
            <a-link @click="changePhoneFunc">
              {{ $t('userSetting.SecuritySettings.button.update') }}
            </a-link>
          </div>
        </template>
      </a-list-item-meta>
    </a-list-item>
    <a-list-item>
      <a-list-item-meta>
        <template #avatar>
          <a-typography-paragraph>
            {{ $t('userSetting.SecuritySettings.form.label.email') }}
          </a-typography-paragraph>
        </template>
        <template #description>
          <div v-if="userStore.email" class="content">
            <a-typography-paragraph v-model="userStore.email">
              已绑定：{{ userStore.email }}
            </a-typography-paragraph>
          </div>
          <div v-else class="content">
            <a-typography-paragraph> 未绑定邮箱 </a-typography-paragraph>
          </div>
          <div v-if="userStore.email" class="operation">
            <a-link @click="changeEmailFunc">
              {{ $t('userSetting.SecuritySettings.button.update') }}
            </a-link>
          </div>
          <div v-else class="operation">
            <a-link> 绑定 </a-link>
          </div>
        </template>
      </a-list-item-meta>
    </a-list-item>
  </a-list>
</template>

<script lang="ts" setup>
  import { ref, defineEmits, nextTick } from 'vue';
  import axios from 'axios';
  import { useUserStore } from '@/store';
  import { getToken } from '@/utils/auth';
  import { useRouter } from 'vue-router';

  const userStore = useUserStore();
  userStore.setInfo(JSON.parse(localStorage.getItem('userStore')!));
  let oldUsername = userStore.username;
  const maskedPhone = ref('');
  const start = userStore.phone!.slice(0, 3); // 前三位
  const middle = '*'.repeat(6); // 中间六位替换成星号
  const end = userStore.phone!.slice(-2); // 后两位
  maskedPhone.value = `${start}${middle}${end}`;
  const jwt = getToken();
  const changeUsername = ref(false);
  const emit = defineEmits<{
    (event: 'changeName', payload: string): void;
  }>();
  const inputRef = ref();
  const router = useRouter();

  const changeUsernameFunc = () => {
    changeUsername.value = true;
    nextTick(() => {
      inputRef.value.focus();
    });
  };
  const saveUsername = () => {
    changeUsername.value = false;
    // 定义要更新的数据
    const newUsername = userStore.username;
    if (newUsername !== oldUsername) {
      emit('changeName', newUsername!);
      const updatedData = {
        username: newUsername,
      };
      userStore.setInfo({ username: newUsername });
      localStorage.setItem('userStore', JSON.stringify(userStore.$state));
      oldUsername = newUsername;
      // 发送 PATCH 请求
      axios
        .patch(
          `http://localhost:8000/user/update/${userStore.accountId}`,
          updatedData
        )
        .then((response) => {})
        .catch((error) => {
          console.error(error);
        });
    }
  };
  const changePasswordFunc = () => {
    router.push({ name: 'ChangeInfo', params: { toChange: 'password'}});
  };
  const changePhoneFunc = () => {
    router.push({ name: 'ChangeInfo', params: { toChange: 'phone'}});
  };
  const changeEmailFunc = () => {
    router.push({ name: 'ChangeInfo', params: { toChange: 'email'}});
  };
</script>

<style scoped lang="less">
  #input {
    margin-bottom: 20px;
  }
  :deep(.arco-list-item) {
    border-bottom: none !important;
    .arco-typography {
      margin-bottom: 20px;
    }
    .arco-list-item-meta-avatar {
      margin-bottom: 1px;
    }
    .arco-list-item-meta {
      padding: 0;
    }
  }
  :deep(.arco-list-item-meta-content) {
    flex: 1;
    border-bottom: 1px solid var(--color-neutral-3);

    .arco-list-item-meta-description {
      display: flex;
      flex-flow: row;
      justify-content: space-between;

      .tip {
        color: rgb(var(--gray-6));
      }
      .operation {
        margin-right: 6px;
      }
    }
  }
</style>
