<script setup lang="ts">
  import axios from "axios";
  import apiCat from "@/api/main";
  import {onMounted, reactive, ref} from "vue";
  import {useI18n} from "vue-i18n";
  import {getModelDetails, getModelScore} from "@/api/dataset";
  import Chart from 'chart.js/auto';
  import {min} from "lodash";

  const props = defineProps(['datasetID']);
  const { t } = useI18n();
  const columns = [
    {
      title: t('dataset.LLMName'),
      dataIndex: 'name',
      align: 'center',
    },
    {
      title: t('dataset.score'),
      dataIndex: 'score',
      align: 'center',
    },
  ];

  let modelDetails:any;
  await getModelDetails()
      .then(result => {
        modelDetails = result;
      })
      .catch(error => {});

  let modelScore:any;
  await getModelScore(1)
      .then(result => {
        modelScore = result;
      })
      .catch(error => {});

  const array: Array<any> = [];
  for (let i = 0; i < modelScore.length; i+=1) {
    array.push({name: modelScore[i].LLM_name, score: modelScore[i].credit});
  }
  const data = reactive(array);

  const buttonDisabled = ref(true);

  const visChart = ref();

  const selectedModels = ref<string[]>([]);

  const handleThreeSelect = (value:any) => {
    selectedModels.value = value;
    buttonDisabled.value = value.length !== 3;
  }

  const paint = () => {
    const snap = selectedModels.value;
    const existingChart = Chart.getChart(visChart.value);
    if (existingChart) {
      existingChart.destroy();
    }
    const sets = [
      {
        label: 'first',
        data: [
          { x: 10, y: 1 },
          { x: 15, y: 1 },
          { x: 20, y: 1 },
        ],
        backgroundColor: 'rgba(255, 159, 64, 0.2)',
        pointRadius: 4,
        showLine: true,
        borderColor: 'rgba(255, 159, 64, 0.2)',
        borderWidth: 2
      },
      {
        label: 'second',
        data: [
          { x: 10, y: 2 },
          { x: 15, y: 2 },
          { x: 20, y: 2 },
        ],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        pointRadius: 4,
        showLine: true,
        borderColor: 'rgba(75, 192, 192, 0.2)',
        borderWidth: 2
      },
      {
        label: 'third',
        data: [
          { x: 10, y: 3 },
          { x: 15, y: 3 },
          { x: 20, y: 3 },
        ],
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        pointRadius: 4,
        showLine: true,
        borderColor: 'rgba(153, 102, 255, 0.2)',
        borderWidth: 2
      },
    ];
    const minXValue = sets
        .map(dataset => dataset.data.map(point => point.x))
        .reduce((acc, curr) => acc.concat(curr), [])
        .reduce((mini, current) => Math.min(mini, current), Infinity);
    const maxXValue = sets
        .map(dataset => dataset.data.map(point => point.x))
        .reduce((acc, curr) => acc.concat(curr), [])
        .reduce((maxi, current) => Math.max(maxi, current), -Infinity);
    const visualChart = new Chart(visChart.value, {
     type: 'scatter',
     data: {
       datasets: sets
     },
     options: {
       scales: {
         x: {
           type: 'linear',
           position: 'bottom',
           min: minXValue-5,
           max: maxXValue+5,
           ticks: {
             stepSize: 5
           }
         },
         y: {
           type: 'linear',
           position: 'left',
           min: 0,
           ticks: {
             stepSize: 1,
             color: 'rgb(22,93,255)',
             callback(value, index, values) {
               if (value === 0) {
                 return '';
               }
               return snap[index-1];
             }
           }
         }
       },
       plugins: {
         legend: {
           display: false,
         },
       }
     },
    });
  }
</script>

<template>
  <div id="container">
    <a-table :columns="columns" :data="data" id="scoreTable"/>
    <div id="separator"></div>
    <div id="visualization">
      <h1>{{ $t('dataset.visualization') }}</h1>
      <div class="boxTest">
        <div class="contentTest">
          <h3>
            {{ $t('dataset.visualization.rule') }}
          </h3>
        </div>
      </div>
      <a-divider />
      <div id="select">
        <a-select :default-value="[]" :style="{width:'360px'}" :placeholder="$t('dataset.select')" multiple
                  :scrollbar="true" :limit="3" @change="handleThreeSelect">
          <a-option v-for="model in modelDetails" :key="model">{{ model.name }}</a-option>
        </a-select>
        <a-button type="primary" :disabled="buttonDisabled" @click="paint">
          <template #icon>
            <icon-check />
          </template>
          <template #default>{{ $t('dataset.confirm') }}</template>
        </a-button>
      </div>
      <canvas ref="visChart" :style="{width:'400px'}" id="myChart"></canvas>
    </div>
  </div>
</template>

<style scoped lang="less">
 #container {
   height: 500px;
   display: flex;
   justify-content: space-between;
   align-items: center;
 }

 #scoreTable {
   flex: 14;
 }

  #separator {
    flex: 1;
    width: 1px;
    border-left: 1px dashed #ccc;
    height: 500px;
    margin-left: 10px;
    margin-right: 10px;
  }

  #visualization {
    flex: 9;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

 .boxTest {
   height: 30px;
 }

 .boxTest::before {
   content: '';
   position: absolute;
   width: 6px;
   height: 30px;
   background: rgb(45, 92, 246);
 }

 .contentTest {
   position: relative;
   display: flex;
   align-items: center;
   height: 100%;
   padding-left: 20px;
 }

 #select {
   display: flex;
   justify-content: space-between;
 }
</style>