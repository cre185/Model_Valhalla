<template>
  <div class="container">
    <Breadcrumb :items="['menu.dataset', 'menu.dataset.details']" />
    <dataset-profile />
  </div>
</template>

<script lang="ts" setup>

import DatasetProfile from "@/views/dataset/components/dataset-profile.vue";
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }
</style>
