<template>
  <div class="container">
    <Breadcrumb :items="['menu.evaluate', 'menu.evaluate.subjective']" />
    <a-row :gutter="20" align="stretch">
      <a-col :span="24">
        <a-card class="general-card" >
          <template #title>
            <div class="custom-title"><b>{{ $t('evaluation.subjective.rules.title') }}</b></div>
          </template>
          <a-space direction="vertical" size="large">
            <div class="boxTest">
              <div class="contentTest">
                <h3>
                  {{ $t('evaluation.subjective.rules.1') }}
                </h3>
              </div>
            </div>
            <div class="boxTest">
              <div class="contentTest">
                <h3>
                  {{ $t('evaluation.subjective.rules.2') }}
                </h3>
              </div>
            </div>
            <div class="boxTest">
              <div class="contentTest">
                <h3>
                  {{ $t('evaluation.subjective.rules.3') }}
                </h3>
              </div>
            </div>
          </a-space>
        </a-card>
        <br>
        <a-card class="resultShow">
          <div id="selectModel">
            <a-select  v-model="modelSelector" :options="ModelSelectOptions" style="width: 320px"
                      :placeholder="$t('evaluation.select.models')" />
            <a-select  v-model="datasetSelector" :options="DatasetSelectOptions" style="width: 320px"
                       :placeholder="$t('evaluation.select.datasets')" />
            <a-button type="primary" style="margin: auto 20px auto 20px;" @click="handleSelect">
              <template #icon>
                <icon-check></icon-check>
              </template>
              {{ $t('evaluation.select.models.confirm') }}
            </a-button>
          </div>
          <a-row :gutter="16">
            <a-col :span="12">
              <div class="text-box">
                <a-space direction="vertical" :size="10" class="QAShower">
                  <div class="box-header" v-if="currentLLMID!==undefined">
                    <a-space>
                      <icon-message/>
                      <span style="font-size: 13px;">{{ currentLLMName }}</span>
                    </a-space>
                  </div>
                  <div class="QA" v-if="currentLLMID!==undefined">
                    <a-space direction="vertical" :size="15" class="added-div">
                      <div class="userQuestion" v-if="subjectiveInfo!==undefined">
                        {{subjectiveInfo[currentIndex].getPrompt()}}
                      </div>
                      <div v-if="subjectiveInfo!==undefined">
                        <div v-if="subjectiveInfo[currentIndex].getAnswerGenerated()" ref="modelResponse" class="modelResponse">
                          {{subjectiveInfo[currentIndex].getAnswer()}}
                        </div>
                      </div>
                    </a-space>
                  </div>
                </a-space>
              </div>
            </a-col>
            <a-col span="12" v-if="currentLLMID!==undefined && subjectiveInfo!==undefined">
                <div>
                  问题类型:
                </div>
                <div style="display: flex; align-items: center; justify-content: center">
                  <a-tag v-for="(item, index) in subjectiveInfo[currentIndex].subjects" :key="index">
                    {{item}}
                  </a-tag>
                </div>
                <div>
                  评分:
                </div>
                <a-rate :count="10" style="display: flex; align-items: center; justify-content: center"
                        :model-value="currentScore" @change="handleRate"/>
                <div style="display: flex; align-items: center; justify-content: center" v-if="subjectiveInfo!==undefined">
                  {{`${currentIndex + 1} / ${subjectiveInfo.length}`}}
                </div>
                <div style="display: flex; flex-direction: row; align-items: center; justify-content: center" v-if="subjectiveInfo!==undefined">
                  <a-button @click="handleGenerate">
                    <div v-if="subjectiveInfo[currentIndex].answerGenerated">
                      已生成
                    </div>
                    <div v-else>
                      生成答案
                    </div>
                  </a-button>
                  <a-button @click="handlePrev">
                    上一题
                  </a-button>
                  <a-button @click="handleNext">
                    下一题
                  </a-button>
                  <a-button :disabled="!subjectiveInfo.every(element => element.getScored())" @click="handleSubmit">
                    提交结果
                  </a-button>
                </div>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script lang="ts" setup>
  import { computed, ref, reactive, watch, nextTick } from 'vue';
  import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
  import {queryLLMevaluateList, queryDatasetEvaluateList, SelectedModel, getStreamResponse, updateSubjetiveRecord} from "@/api/evaluate";
  import {SubjectiveEvaluationData, generateSubEvalData} from "@/api/dataset";
  import {getLLMName} from "@/api/evaluate";
  import {getToken} from "@/utils/auth";
  import element from "zrender/src/Element";

  const SelectedModelInfo = ref<SelectedModel[]>();
  const SelectedDatasetInfo = ref<SelectedModel[]>();
  const subjectiveInfo = ref<SubjectiveEvaluationData[]>();
  const modelSelector = ref<number>();
  const datasetSelector = ref<number>();
  const currentLLMID = ref<number>();
  const currentDatasetID = ref<number>();
  const currentLLMName = ref<string>();
  const currentIndex = ref(0);
  const modelResponse = ref();
  const currentScore = ref<number>(0);
  SelectedModelInfo.value = (await queryLLMevaluateList()).data;
  SelectedDatasetInfo.value = (await queryDatasetEvaluateList()).data;
  const ModelSelectOptions = computed<SelectOptionData[]>(() => {
    return (SelectedModelInfo.value || []).map((model) => ({
      label: model.name,
      value: model.id,
    }));
  });
  const DatasetSelectOptions = computed<SelectOptionData[]>(() => {
    return (SelectedDatasetInfo.value || []).map((dataset) => ({
      label: dataset.name,
      value: dataset.id,
    }));
  });

  const handleSelect = () => {
    currentLLMID.value = modelSelector.value;
    currentDatasetID.value = datasetSelector.value;
    generateSubEvalData(currentDatasetID.value!).then(returnValue => {
      subjectiveInfo.value = returnValue;
    });
    getLLMName(currentLLMID.value!.toString()).then(returnValue => {
      currentLLMName.value = returnValue;
    });
  };

  const handlePrev = () => {
    currentIndex.value = currentIndex.value ? currentIndex.value - 1 : currentIndex.value;
    currentScore.value = subjectiveInfo.value![currentIndex.value].getScore()!;
  }

  const handleNext = () => {
    currentIndex.value = currentIndex.value < subjectiveInfo.value!.length ? currentIndex.value + 1 : currentIndex.value;
    currentScore.value = subjectiveInfo.value![currentIndex.value].getScore()!;
  }

  const handleGenerate = async () => {
    subjectiveInfo.value![currentIndex.value].setAnswerGenerated();
    subjectiveInfo.value![currentIndex.value].setAnswer('...');
    await getStreamResponse(getToken()!, subjectiveInfo.value![currentIndex.value].getPrompt(), subjectiveInfo.value![currentIndex.value],
    currentLLMID.value!, modelResponse);
  }

  const handleRate = (score: number)=>{
    if(subjectiveInfo.value![currentIndex.value].getAnswerGenerated()){
      subjectiveInfo.value![currentIndex.value].setScore(score);
      currentScore.value = score;
      subjectiveInfo.value![currentIndex.value].setScored();
    }
  }

  const handleSubmit = ()=>{
    let score = 0;
    for(let i = 0; i < subjectiveInfo.value!.length; i += 1){
      score += subjectiveInfo.value![i].getScore()!;
    }
    score /= subjectiveInfo.value!.length;
    updateSubjetiveRecord({llmId: currentLLMID.value, datasetId: currentDatasetID.value, credit: score});
  }
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }

  .custom-title {
    font-size: 27px;
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

  .text-box {
    border: 1px solid #ccc;
    border-radius: 10px;
    height: 500px;
    padding-bottom: 2%;
  }

  .text-box {
    border: 1px solid #ccc;
    border-radius: 10px;
    height: 500px;
    padding-bottom: 2%;
  }

  #selectModel {
    display: flex;
    align-items: center;
    gap: 30px;
    width: 45%;
    height: 50px;
    margin-bottom: 20px;
  }

  .QAShower
  {
    width: 100%;
  }

  .box-header {
    display: flex;
    justify-content: center;
    align-items: center;
    border-bottom: 1px solid #ccc;
    border-right: 1px solid #ccc;
    border-radius: 10px 0 10px 0;
    width: 100px;
    height: 30px;
  }

  .QA {
    display: flex;
    flex-direction: column;
    gap: 15px;
    height: 450px;
    overflow: auto;
  }

  .added-div {
    width: 100%;
  }

  .userQuestion {
    background-color: #fff7ed;
    margin: 10% auto 5% 7%;
    padding: 15px;
    width: 91%;
    border: 1px solid #fee6ca;
    border-radius: 20px 20px 0 20px;
    font-size: 20px;
  }

  .modelResponse {
    background-color: #f9fafb;
    margin: 5% auto 10% 2%;
    padding: 15px;
    width: 91%;
    border: 1px solid #e5e7eb;
    border-radius: 20px 20px 20px 0;
    font-size: 20px;
  }
</style>
