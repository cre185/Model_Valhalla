<template>
  <div class="container">
    <Breadcrumb :items="['menu.dataset', 'menu.dataset.details']" />
    <a-button
    type="primary"
    @click="feedbackClick"
    >Show Dataset Feedback</a-button>
    <DatasetFeedback
    v-model:visible="showDatasetFeedback"/>
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue';
import DatasetFeedback from "./components/datasetfeedback.vue";

const showDatasetFeedback = ref(false);
const feedbackClick = () => {
  showDatasetFeedback.value = true;
}
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }
</style>
