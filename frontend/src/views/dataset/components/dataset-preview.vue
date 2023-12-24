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
        console.log(result.data)
        if (result.data.subjective) {
          columns = [
            {
              title: t('dataset.details.prompt'),
              dataIndex: 'prompt',
              align: 'center',
            },
          ];
          data = [];
          for (let i = 0; i < result.data.data.length; i+=1) {
            data.push({
              key: i,
              prompt: result.data.data[i],
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
          for (let i = 0; i < result.data.data.length; i+=1) {
            data.push({
              key: i,
              question: result.data.data[i][0],
              A: result.data.data[i][1],
              B: result.data.data[i][2],
              C: result.data.data[i][3],
              D: result.data.data[i][4],
              answer: result.data.data[i][5],
            });
          }
        }
      })
      .catch(error => {});
</script>

<template>
  <div id="container">
    <a-table :columns="columns" :data="data" :pagination="false" :scroll="{y: 410}"/>
  </div>
</template>

<style scoped lang="less">
  #container {
    height: 460px;
    margin-left: 20px;
    margin-right: 20px;
  }
</style>