<template>
  <a-card class="general-card" :title="$t('userInfo.title.subscribedModels')">
    <template #extra>
      <a-link>{{ $t('userInfo.viewAll') }}</a-link>
    </template>
    <a-list :bordered="false">
      <a-list-item
          v-for="model in subscribedModelsList"
          :key="model.id"
          action-layout="horizontal"
      >
        <a-skeleton
            v-if="loading"
            :loading="loading"
            :animation="true"
            class="skeleton-item"
        >
          <a-col :span="24">
            <a-skeleton-line :widths="['40%', '100%']" :rows="2" />
          </a-col>
        </a-skeleton>
        <a-list-item-meta
            v-else
            :title="model.name"
            :description="`${$t('userInfo.subscribedModel.ranking')} ${model.ranking}
            ${$t('userInfo.subscribedModel.ranking.suffix')}`"
        >
        </a-list-item-meta>
      </a-list-item>
    </a-list>
  </a-card>
</template>

<script setup lang="ts">
  import useLoading from "@/hooks/loading";
  import {ref} from "vue";
  import {SubscribedModelRecord, querySubscribedModels} from "@/api/user-center";

  const props = defineProps(['userID']);
  const { loading, setLoading } = useLoading(true);
  const subscribedModelsList = ref<SubscribedModelRecord[]>([]);
  const fetchData = async () => {
    try {
      const data  = await querySubscribedModels(props.userID);
      subscribedModelsList.value = data;
    } catch (err) {
      // you can report use errorHandler or other
    } finally {
      setLoading(false);
    }
  };
  fetchData();
</script>

<style scoped>

</style>
