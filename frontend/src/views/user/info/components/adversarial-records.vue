<template>
  <a-card class="general-card" style="height: 100%" :key="toRepaint">
    <template #title>
      <span style="font-weight: 900">
        {{ $t('userInfo.title.adversarialRecords') }}
      </span>
    </template>
    <template #extra>
      <a-link @click="handleShowMore">{{ $t('userInfo.viewAll') }}</a-link>
    </template>
    <a-list :bordered="false"
    >
      <a-skeleton v-if="loading" :loading="loading" :animation="true">
        <a-skeleton-line :rows="8" />
      </a-skeleton>
      <a-list-item v-else v-for="(data, index) in battleRecordsData" :key="index">
        <a-list-item-meta
            :title="`${$t('userInfo.adversarial.models')}${data.model} & ${data.adversarialModel}`"
            :description="data.battleTime"
            :style="{visibility: data.id !== undefined ? 'visible' : 'hidden'}"
        >
        </a-list-item-meta>
      </a-list-item>
    </a-list>
  </a-card>
</template>

<script setup lang="ts">

import {defineEmits, onMounted, ref, watch} from "vue";
  import {BattleRecordsData, queryBattleRecordsData} from "@/api/user-center";
  import useLoading from "@/hooks/loading";
  import {useUserStore} from "@/store";

  const { loading, setLoading } = useLoading(true);
  const userInfo = useUserStore();
  const emit = defineEmits<{
    (event: 'showMore', arg1: number): void;
  }>();

  const battleRecordsData = ref<BattleRecordsData[] | any[]>([]);
  const toRepaint = ref(false);

  const fetchData = () => {
    try {
      queryBattleRecordsData(parseInt(userInfo.accountId!, 10)).then(returnValue => {
        battleRecordsData.value = returnValue;
        if(battleRecordsData.value.length > 3){
          battleRecordsData.value = battleRecordsData.value.slice(0 ,3);
        }
        else if(battleRecordsData.value.length === 0){
          battleRecordsData.value = [{}];
        }
      });
    } catch (err) {
      // you can report use errorHandler or other
    } finally {
      setLoading(false);
    }
  };

  const handleShowMore = () => {
    emit("showMore", 3);
  }

  onMounted(() => {
    fetchData();
  });
</script>

<style scoped>
  :deep(.arco-card-header) {
    height: 20%;
  }

  :deep(.arco-card-body) {
    height: 80%;
  }

  :deep(.arco-list-item-meta-title){
    font-weight: 700;
  }
</style>
