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
            <a-typography-paragraph>
              已绑定：150******50
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
          <div class="content">
            <a-typography-paragraph>
              {{ $t('userSetting.SecuritySettings.placeholder.email') }}
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
  </a-list>
</template>

<script lang="ts" setup>
  import { ref, onBeforeMount, defineEmits } from 'vue';
  import axios from 'axios';
  import { useUserStore } from '@/store';
  import { FileItem } from '@arco-design/web-vue/es/upload/interfaces';

  const username = ref('');
  const addTime = ref('');
  const userId = 1;
  const changeUsername = ref(false);
  const emit = defineEmits<{
    (event: 'changeName', payload: string): void;
  }>();

  const fetchData = () => {
    axios
      .get(`user/retrieve/${userId}`)
      .then((response) => {
        const responseJson = response.data;
        // 请求成功，处理响应数据
        username.value = responseJson.username;
        addTime.value = responseJson.add_time;
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
      .patch(`user/update/${userId}`, updatedData)
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
