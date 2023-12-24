<script setup lang="ts">
  import { reactive } from 'vue';
  import {downloadDataset, getDatasetFile, getModelDetails, previewDataset} from "@/api/dataset";
  import {useI18n} from "vue-i18n";

  const props = defineProps(['datasetID']);
  const { t } = useI18n();
  let columns;
  let data;

  await previewDataset(props.datasetID)
      .then(result => {
        if (result.data.subjective) {
          columns = [
            {
              title: t('dataset.details.prompt'),
              dataIndex: 'prompt',
              align: 'center',
            },
          ];
          data = [];
          for (let i = 0; i < result.data.items.length; i+=1) {
            data.push({
              key: '1',
              prompt: result.data.items[i],
            });
          }
        }
        else {
          columns = [
            {
              title: t('dataset.details.question'),
              dataIndex: 'question',
              align: 'center',
            },
            {
              title: 'A',
              dataIndex: 'A',
              align: 'center',
            },
            {
              title: 'B',
              dataIndex: 'B',
              align: 'center',
            },
            {
              title: 'C',
              dataIndex: 'C',
              align: 'center',
            },
            {
              title: 'D',
              dataIndex: 'D',
              align: 'center',
            },
            {
              title: t('dataset.details.answer'),
              dataIndex: 'answer',
              align: 'center',
            },
          ];
          data = [];
          for (let i = 0; i < result.data.items.length; i+=1) {
            data.push({
              key: '1',
              question: result.data.items[i].question,
              A: result.data.items[i].A,
              B: result.data.items[i].B,
              C: result.data.items[i].C,
              D: result.data.items[i].D,
              answer: result.data.items[i].answer,
            });
          }
        }
      })
      .catch(error => {});
</script>

<template>
  <div id="container">
    <a-table :columns="columns" :data="data" :pagination="false" :scroll="{y: 460}"/>
  </div>
</template>

<style scoped lang="less">
  #container {
    height: 460px;
    margin-left: 20px;
    margin-right: 20px;
  }
</style>