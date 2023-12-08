<template>
  <div class="container">
    <Breadcrumb :items="['menu.dataset', 'menu.dataset.details']" />
    <a-button
    type="primary"
    @click="UploadClick"
    >Show Dataset Upload</a-button>
    <DatasetUpload
    v-model:visible="showDatasetUpload"/>
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue';
import DatasetUpload from "./components/datasetupload.vue";

const showDatasetUpload = ref(false);
const UploadClick = () => {
  showDatasetUpload.value = true;
}
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }
</style>