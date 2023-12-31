<template>
  <a-card :bordered="false">
    <a-space :size="54">
      <a-upload
        :custom-request="customRequest"
        list-type="picture-card"
        :file-list="fileList"
        :show-upload-button="true"
        :show-file-list="false"
        @change="uploadChange"
      >
        <template #upload-button>
          <a-avatar :size="100" class="info-avatar">
            <template #trigger-icon>
              <icon-camera />
            </template>
            <img
              v-if="fileList.length"
              alt="用户头像"
              :src="userStore.avatar"
            />
          </a-avatar>
        </template>
      </a-upload>
      <a-descriptions
        id="infoBar"
        :column="2"
        align="right"
        layout="inline-horizontal"
        :label-style="{
          width: '100px',
          fontWeight: 'normal',
          color: 'rgb(var(--gray-8))',
        }"
        :value-style="{
          width: '300px',
          paddingLeft: '8px',
          textAlign: 'left',
        }"
      >
        <span
          >{{ $t('userSetting.label.name') }}：{{ userStore.username }}</span
        >
        <span>{{ $t('userSetting.label.accountId') }}：{{ userStore.accountId }}</span>
        <span
          >{{ $t('userSetting.label.registrationDate') }}：{{ userStore.registrationDate }}</span
        >
      </a-descriptions>
    </a-space>
  </a-card>
</template>

<script lang="ts" setup>
  import { ref, onBeforeMount, watch } from 'vue';
  import type {
    FileItem,
    RequestOption,
  } from '@arco-design/web-vue/es/upload/interfaces';
  import { useUserStore } from '@/store';
  import { userUploadApi } from '@/api/user-center';
  import type { DescData } from '@arco-design/web-vue/es/descriptions/interface';
  import { getToken } from '@/utils/auth';

  const userStore = useUserStore();
  userStore.setInfo(JSON.parse(localStorage.getItem('userStore')!));
  const props = defineProps(['name']);
  const jwt = getToken();

  const file = {
    uid: '-2',
    name: 'avatar.png',
    url: userStore.avatar,
  };
  const renderData = ref([
    {
      label: 'userSetting.label.name',
      value: userStore.username,
    },
    {
      label: 'userSetting.label.accountId',
      value: userStore.accountId,
    },
    {
      label: 'userSetting.label.registrationDate',
      value: userStore.registrationDate,
    },
  ]) as unknown as DescData[];
  const fileList = ref<FileItem[]>([file]);
  const uploadChange = (fileItemList: FileItem[], fileItem: FileItem) => {
    fileList.value = [fileItem];
    userStore.setInfo({ avatar: fileItem.url });
    localStorage.setItem('userStore', JSON.stringify(userStore.$state));
  };
  const customRequest = (options: RequestOption) => {
    // docs: https://axios-http.com/docs/cancellation
    const controller = new AbortController();

    (async function requestWrap() {
      const {
        onProgress,
        onError,
        onSuccess,
        fileItem,
        name = 'file',
      } = options;
      onProgress(20);
      const formData = new FormData();
      formData.append(name as string, fileItem.file as Blob);
      const onUploadProgress = (event: ProgressEvent) => {
        let percent;
        if (event.total > 0) {
          percent = (event.loaded / event.total) * 100;
        }
        onProgress(parseInt(String(percent), 10), event);
      };

      try {
        // https://github.com/axios/axios/issues/1630
        // https://github.com/nuysoft/Mock/issues/127
        // const jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTk3MTYwODIsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoidGVzdHVzZXIyIn0.cLylHhCqtP2xuMu90OlWEeunZ5vpVKMGcXzxAlxVp9U';
        const res = await userUploadApi(formData, jwt!);
        onSuccess(res);
      } catch (error) {
        onError(error);
      }
    })();
    return {
      abort() {
        controller.abort();
      },
    };
  };
  watch(
    () => props.name,
    (newVal, oldVal) => {
      // 更新组件内部的响应式变量
      userStore.setInfo({ username: newVal });
      localStorage.setItem('userStore', JSON.stringify(userStore.$state));
    }
  );
</script>

<style scoped lang="less">
  .arco-card {
    padding: 14px 0 4px 4px;
    border-radius: 4px;
  }
  :deep(.arco-avatar-trigger-icon-button) {
    width: 32px;
    height: 32px;
    line-height: 32px;
    background-color: #e8f3ff;
    .arco-icon-camera {
      margin-top: 8px;
      color: rgb(var(--arcoblue-6));
      font-size: 14px;
    }
  }
</style>
