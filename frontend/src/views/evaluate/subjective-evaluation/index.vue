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
          <div id="selectModel" style="margin-bottom: 20px; margin-left: 21vw; transition: margin-left 0.5s ease-out">
            <a-form layout="inline" >
              <a-form-item>
                <a-select  v-model="modelSelector" :options="ModelSelectOptions" style="width: 15vw; margin-right: 10px"
                           :placeholder="$t('evaluation.select.models')" />
              </a-form-item>
              <a-form-item>
                <a-select  v-model="datasetSelector" :options="DatasetSelectOptions" style="width: 15vw"
                           :placeholder="$t('evaluation.select.datasets')" />
              </a-form-item>
              <a-form-item>
                <a-button html-type="submit" type="primary" style="margin-left: 10px;" @click="handleSelect">
                  <template #icon>
                    <icon-check/>
                  </template>
                  {{ $t('evaluation.select.models.confirm') }}
                </a-button>
              </a-form-item>
            </a-form>
          </div>
          <a-row :gutter="16">
            <a-col id='selectPanel' :span="12" style="margin-left: 22vw; transition: margin-left 0.5s ease-out;">
              <div class="text-box">
                <a-space direction="vertical" :size="10" class="QAShower">
                  <div class="box-header" v-if="currentLLMID!==undefined && currentDatasetID!==undefined">
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
            <transition name="fade" @before-enter="beforeEnter" @enter="enter">
              <a-col :span="12" v-if="currentLLMID!==undefined && subjectiveInfo!==undefined" key="subPanel">
                  <div style="font-size: 2vh; font-weight: bolder;">
                    {{$t('evaluation.question.type')}}
                  </div>
                  <div style="display: flex; align-items: center; justify-content: center">
                    <a-tag v-for="(item, index) in subjectiveInfo[currentIndex].subjects" :key="index"
                           style="margin: 6.5vh 0.5vw" color="arcoblue" size="large">
                      {{ item }}
                    </a-tag>
                  </div>
                  <div style="font-size: 2vh; font-weight: bolder; margin-top: 3vh">
                    {{ $t('evaluation.credit') }}
                  </div>
                  <a-rate :count="10" style="display: flex; align-items: center; justify-content: center; margin-top: 8vh"
                          :model-value="currentScore" @change="handleRate"/>
                  <div style="display: flex; align-items: center; justify-content: center; margin-top: 9vh;
                            color: #1c61ff; font-size: 1.5vh; font-weight: bold"
                       v-if="subjectiveInfo!==undefined">
                    {{`${currentIndex + 1} / ${subjectiveInfo.length}`}}
                  </div>
                  <div style="display: flex; flex-direction: row; align-items: center; justify-content: center;
                              margin-top: 2vh" v-if="subjectiveInfo!==undefined">
                    <a-button type="outline" style="margin: auto 0.5vw" @click="handleGenerate"
                              :disabled="subjectiveInfo[currentIndex].getAnswerGenerated()">
                      <div v-if="subjectiveInfo[currentIndex].getAnswerGenerated()">
                        {{ $t('evaluation.answer.generated') }}
                      </div>
                      <div v-else>
                        {{ $t('evaluation.answer.generate') }}
                      </div>
                    </a-button>
                    <a-button type="outline" style="margin: auto 0.5vw"
                              :disabled="currentIndex===0" @click="handlePrev">
                      {{ $t('evaluation.question.last') }}
                    </a-button>
                    <a-button type="outline" style="margin: auto 0.5vw"
                              :disabled="currentIndex===subjectiveInfo.length - 1" @click="handleNext">
                      {{ $t('evaluation.question.next') }}
                    </a-button>
                    <a-button type="outline" style="margin: auto 0.5vw"
                              :disabled="!subjectiveInfo.every(element => element.getScored())" @click="handleSubmit">
                      {{ $t('evaluation.credit.submit') }}
                    </a-button>
                  </div>
              </a-col>
            </transition>
          </a-row>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script lang="ts" setup>
  import { computed, ref, reactive, watch, nextTick } from 'vue';
  import { Modal } from '@arco-design/web-vue';
  import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
  import {queryLLMevaluateList, queryDatasetEvaluateList, SelectedModel, getStreamResponse, updateSubjetiveRecord} from "@/api/evaluate";
  import {SubjectiveEvaluationData, generateSubEvalData} from "@/api/dataset";
  import {getLLMName} from "@/api/evaluate";
  import {getToken} from "@/utils/auth";
  import element from "zrender/src/Element";
  import {useI18n} from "vue-i18n";

  const { t } = useI18n();
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
    if(modelSelector.value === undefined || datasetSelector.value === undefined){
      Modal.error({
        title: t('evaluation.select.error.title'),
        content: t('evaluation.select.error.content')
      });
      return;
    }
    document.getElementById('selectPanel')!.style.marginLeft = '0';
    document.getElementById('selectModel')!.style.marginLeft = '0';
    currentLLMID.value = modelSelector.value;
    currentDatasetID.value = datasetSelector.value;
    setTimeout(()=>{
      generateSubEvalData(currentDatasetID.value!).then(returnValue => {
        subjectiveInfo.value = returnValue;
      });
      getLLMName(currentLLMID.value!.toString()).then(returnValue => {
        currentLLMName.value = returnValue;
      });
    }, 500);
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

  const beforeEnter = (el: any) => {
    el.style.opacity = 0;
  };

  const enter = (el: any, done: any) => {
    requestAnimationFrame(() => {
      el.style.transition = 'opacity 0.5s ease';
      el.style.opacity = 1;
      done();
    });
  };
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
    width: 140px;
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
