<script setup lang="ts">
  import axios from "axios";
  import apiCat from "@/api/main";
  import {onMounted, reactive, ref} from "vue";
  import {useI18n} from "vue-i18n";
  import {getModelDetails, getModelScore} from "@/api/dataset";

  const props = defineProps(['datasetID']);
  const { t } = useI18n();
  const columns = [
    {
      title: t('dataset.LLMName'),
      dataIndex: 'name',
    },
    {
      title: t('dataset.score'),
      dataIndex: 'score',
    },
  ];
  const data = reactive([{
    key: '1',
    name: 'Jane Doe',
    salary: 23000,
    address: '32 Park Road, London',
    email: 'jane.doe@example.com'
  }, {
    key: '2',
    name: 'Alisa Ross',
    salary: 25000,
    address: '35 Park Road, London',
    email: 'alisa.ross@example.com'
  }, {
    key: '3',
    name: 'Kevin Sandra',
    salary: 22000,
    address: '31 Park Road, London',
    email: 'kevin.sandra@example.com'
  }, {
    key: '4',
    name: 'Ed Hellen',
    salary: 17000,
    address: '42 Park Road, London',
    email: 'ed.hellen@example.com'
  }, {
    key: '5',
    name: 'William Smith',
    salary: 27000,
    address: '62 Park Road, London',
    email: 'william.smith@example.com'
  }]);

  let modelDetails:any;
  getModelDetails()
      .then(result => {
        modelDetails = result;
      })
      .catch(error => {});

  let modelScore:any;
  getModelScore(1)
      .then(result => {
        console.log(result);
      })
      .catch(error => {});
</script>

<template>
  <div id="container">
    <a-table :columns="columns" :data="data" id="scoreTable"/>
    <div id="separator"></div>
    <div id="visualization">
      <h1>测试结果可视化</h1>
      <div class="boxTest">
        <div class="contentTest">
          <h3>
            {{ $t('dataset.visualization.rule') }}
          </h3>
        </div>
      </div>
      <a-divider />
      <a-select :default-value="[]" :style="{width:'360px'}" :placeholder="$t('dataset.select')" multiple
                :scrollbar="true">
        <a-option v-for="model in modelDetails" :key="model">{{ model.name }}</a-option>
      </a-select>
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
    border-left: 1px dashed #ccc; /* 1px 宽度的垂直虚线，颜色为黑色 */
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
</style>