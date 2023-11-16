<script setup lang="ts">
  const props = defineProps(['modelDescription', 'website', 'paper', 'license',
    'date', 'img', 'maxHeight']);
</script>

<template>
  <a-space direction="vertical" fill size="small">
    <!-- 模型的logo -->
    <a-image
        width="200"
        :src="props.img"
    />
    <!-- 模型的发布时间 -->
    <span>Released {{props.date}}</span>
    <!-- 模型的详细信息 -->
    <a-list :max-height="props.maxHeight" :scrollbar="true">
      <a-list-item>
        <a-list-item-meta
            :title="$t('ranking.profile.info.description')"
            :description="props.modelDescription"
        >
        </a-list-item-meta>
      </a-list-item>
      <a-list-item>
        <a-list-item-meta
            :title="$t('ranking.profile.info.index')"
        >
        </a-list-item-meta>
        <a-link :href="props.website">{{ props.website }}</a-link>
      </a-list-item>
      <a-list-item>
        <a-list-item-meta
            :title="$t('ranking.profile.info.paper')"
        >
        </a-list-item-meta>
        <a-list :bordered="false">
          <a-list-item v-for="(value, key) in props.paper" :key="key">
            <a-link :href="key as string">{{ value }}</a-link>
          </a-list-item>
        </a-list>
      </a-list-item>
      <a-list-item>
        <a-list-item-meta
            :title="$t('ranking.profile.info.license')"
            :description="props.license"
        >
        </a-list-item-meta>
      </a-list-item>
    </a-list>
  </a-space>
</template>

<style scoped lang="less">

</style>