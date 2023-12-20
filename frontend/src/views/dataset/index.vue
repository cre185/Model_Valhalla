<template>
  <div class="container">
    <!--<Breadcrumb :items="['menu.dataset', 'menu.dataset.details']" />-->
    <!--<dataset-profile />-->
    <!--<dataset-discussion-area :commentDetails="commentDetails" :datasetId=ModelID
                         @change-comment="handleChangeComment" />-->
  </div>
</template>

<script lang="ts" setup>
import DatasetProfile from "@/views/dataset/components/dataset-profile.vue";
import DatasetDiscussionArea from "@/views/dataset/components/dataset-discussion-area.vue";
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }
</style>
