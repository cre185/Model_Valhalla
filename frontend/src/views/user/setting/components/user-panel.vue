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
              :src="fileList[0].url"
              :alt="fileList[0].name"
            />
          </a-avatar>
        </template>
      </a-upload>
      <a-descriptions
        :data="renderData"
        :column="2"
        align="right"
        layout="inline-horizontal"
        :label-style="{
          width: '140px',
          fontWeight: 'normal',
          color: 'rgb(var(--gray-8))',
        }"
        :value-style="{
          width: '200px',
          paddingLeft: '8px',
          textAlign: 'left',
        }"
      >
        <template #label="{ label }">{{ $t(label) }} :</template>
        <template #value="{ value }">
          <span>{{ value }}</span>
        </template>
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
  import axios from 'axios';

  // const username = ref('');
  const addTime = ref('');
  const userId = 1;
  const props = defineProps(['name']);
  const username = ref(props.name);

  const userStore = useUserStore();
  const file = {
    uid: '-2',
    name: 'avatar.png',
    url: userStore.avatar,
  };
  const renderData = ref([
    {
      label: 'userSetting.label.name',
      value: username,
    },
    {
      label: 'userSetting.label.accountId',
      value: userId,
    },
    {
      label: 'userSetting.label.registrationDate',
      value: addTime,
    },
  ]) as unknown as DescData[];
  const fileList = ref<FileItem[]>([file]);
  const uploadChange = (fileItemList: FileItem[], fileItem: FileItem) => {
    fileList.value = [fileItem];
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

        const res = await userUploadApi(formData, {
          controller,
          onUploadProgress,
        });
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
  onBeforeMount(() => {
    fetchData();
  });
  watch(
    () => props.name,
    (newVal, oldVal) => {
      // 更新组件内部的响应式变量
      username.value = newVal;
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
