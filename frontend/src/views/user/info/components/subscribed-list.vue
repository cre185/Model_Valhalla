<template>
  <a-card class="general-card">
    <template #title>
      <span style="font-weight: 900">
        {{ subscriptionType==='llm' ? $t('userInfo.title.subscribedModels')
          : $t('userInfo.title.subscribedDatasets') }}
      </span>
    </template>
    <template #extra>
      <a-link @click="handleShow">{{ $t('userInfo.viewAll') }}</a-link>
    </template>
    <a-row :gutter="[16, 16]">
      <a-col
          v-for="(data, index) in subscribedDataList"
          :key="index"
          :xs="12"
          :sm="12"
          :md="12"
          :lg="12"
          :xl="8"
          :xxl="8"
          class="my-project-item"
      >
        <a-card :style="{visibility: data.name !== undefined ? 'visible' : 'hidden'}">
          <a-skeleton v-if="loading" :loading="loading" :animation="true">
            <a-skeleton-line :rows="3" />
          </a-skeleton>
          <a-space v-else size="medium" direction="vertical">
            <a-typography-text v-if="data.name !== undefined" bold>{{ data.name }}</a-typography-text>
            <a-typography-text v-else>{{ 'placeholder' }}</a-typography-text>
            <a-typography-text v-if="subscriptionType==='llm' && data.ranking !== undefined" type="secondary">
              {{ `${$t('userInfo.subscribedModel.ranking')} ${data.ranking}
            ${$t('userInfo.subscribedModel.ranking.suffix')}` }}
            </a-typography-text>
            <a-typography-text v-else-if="data.domain !== undefined" type="secondary">
              {{ data.domain }}
            </a-typography-text>
            <a-typography-text v-else style="visibility: hidden">{{ 'placeholder' }}</a-typography-text>
          </a-space>
        </a-card>
      </a-col>
    </a-row>
  </a-card>
</template>

<script setup lang="ts">
  import useLoading from "@/hooks/loading";
  import {ref} from "vue";
  import {
    SubscribedModelRecord,
    querySubscribedModels,
    SubscribedDatasetRecord,
    querySubscribedDatasets
  } from "@/api/user-center";
  import {defineEmits} from "vue/dist/vue";

  const props = defineProps(['userID', 'subscriptionType']);
  const emit = defineEmits<{
    (event: 'showMore', arg1: number): void;
  }>();
  const { loading, setLoading } = useLoading(true);
  const subscribedDataList = ref<SubscribedModelRecord[] | SubscribedDatasetRecord[]>(new Array(6).fill({}));
  const fetchData = async () => {
    try {
      let data: any;
      if(props.subscriptionType === 'llm'){
        data = await querySubscribedModels(props.userID);
      }
      else {
        data = await querySubscribedDatasets(props.userID);
      }
      if(data.length > 6){
        data = data.slice(0, 6);
      }
      else {
        while(data.length < 6){
          data.push({});
        }
      }
      subscribedDataList.value = data;
    } catch (err) {
      // you can report use errorHandler or other
    } finally {
      setLoading(false);
    }
  };

  const handleShow = () => {
    emit("showMore", props.subscriptionType==='llm' ? 1 : 2);
  }

  fetchData();
</script>

<style scoped>

</style>
