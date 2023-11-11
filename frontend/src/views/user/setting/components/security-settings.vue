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
              v-if="changeUsername"
              id="input"
              v-model="username"
              :placeholder="username"
              @press-enter="saveUsername"
            />
            <a-typography-paragraph v-else>
              {{ username }}
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
            <a-link>
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
            <a-link>
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
          <div v-if="email != null" class="content">
            <a-typography-paragraph v-model="email">
              已绑定：{{ email }}
            </a-typography-paragraph>
          </div>
          <div v-else class="content">
            <a-typography-paragraph>
              未绑定邮箱
            </a-typography-paragraph>
          </div>
          <div v-if="email != null" class="operation">
            <a-link>
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
  import { ref, onBeforeMount, defineEmits } from 'vue';
  import axios from 'axios';
  import { useUserStore } from '@/store';
  import { FileItem } from '@arco-design/web-vue/es/upload/interfaces';

  const username = ref('');
  const phone = ref('');
  const maskedPhone = ref('');
  const email = ref('');
  const userId = 1;
  const changeUsername = ref(false);
  const emit = defineEmits<{
    (event: 'changeName', payload: string): void;
  }>();

  const fetchData = () => {
    axios
      .get(`http://localhost:8000/user/retrieve/${userId}`)
      .then((response) => {
        const responseJson = response.data;
        // 请求成功，处理响应数据
        username.value = responseJson.username;
        phone.value = responseJson.mobile;
        email.value = responseJson.email;
        const start = phone.value.slice(0, 3); // 前三位
        const middle = '*'.repeat(6); // 中间六位替换成星号
        const end = phone.value.slice(-2); // 后两位

        maskedPhone.value = `${start}${middle}${end}`;
      })
      .catch((error) => {
        // 请求失败，处理错误
        console.error(error);
      });
  };
  const changeUsernameFunc = () => {
    changeUsername.value = true;
  };
  const saveUsername = () => {
    changeUsername.value = false;
    // 定义要更新的数据
    const newUsername = username;
    emit('changeName', newUsername.value);
    const updatedData = {
      username: newUsername.value,
    };
    // 发送 PATCH 请求
    axios
      .patch(`http://localhost:8000/user/update/${userId}`, updatedData)
      .then((response) => {})
      .catch((error) => {
        console.error(error);
      });
  };
  onBeforeMount(() => {
    fetchData();
  });
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
