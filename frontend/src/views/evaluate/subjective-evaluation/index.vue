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
            <a-select  :options="ModelSelectOptions" style="width: 320px"
                      :placeholder="$t('evaluation.select.models')" />
            <a-select  :options="DatasetSelectOptions" style="width: 320px"
                       :placeholder="$t('evaluation.select.datasets')" />
            <a-button type="primary" style="margin: auto 20px auto 20px;" >
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
                  <div class="box-header">
                    <a-space>
                      <icon-message/>
                      <span style="font-size: 13px;">Model A</span>
                    </a-space>
                  </div>
                  <div class="QA" ref="QAModelA">
                    <a-space direction="vertical" :size="15" class="added-div">
                      <div class="userQuestion">
                        TODO
                      </div>
                      <div class="modelResponse">
                        TODO
                      </div>
                    </a-space>
                  </div>
                </a-space>
              </div>
            </a-col>
            <a-col span="12">
                <div>
                  问题类型:
                </div>
                <div style="display: flex; align-items: center; justify-content: center">
                  人称转换
                </div>
                <div>
                  评分:
                </div>
                <a-rate :count="10" style="display: flex; align-items: center; justify-content: center"/>
                <div style="display: flex; flex-direction: row; align-items: center; justify-content: center">
                  <button>
                    生成答案
                  </button>
                  <button>
                    上一题
                  </button>
                  <button>
                    下一题
                  </button>
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
  import { useI18n } from 'vue-i18n';
  import useLoading from '@/hooks/loading';
  import { queryPolicyList, PolicyRecord, PolicyParams } from '@/api/list';
  import { Pagination } from '@/types/global';
  import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import cloneDeep from 'lodash/cloneDeep';
  import Sortable from 'sortablejs';
  import {queryLLMevaluateList, queryDatasetEvaluateList, SelectedModel} from "@/api/evaluate";
  import {SubjectiveEvaluationData, generateSubEvalData} from "@/api/dataset";

  const SelectedModelInfo = ref<SelectedModel[]>();
  const SelectedDatasetInfo = ref<SelectedModel[]>();
  const subjectiveInfo = ref<SubjectiveEvaluationData[]>();
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

  generateSubEvalData(5).then(returnValue => {
    subjectiveInfo.value = returnValue;
  });
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
    margin: 10% auto 10% 7%;
    padding: 15px;
    width: 91%;
    border: 1px solid #fee6ca;
    border-radius: 20px 20px 0 20px;
    font-size: 20px;
  }

  .modelResponse {
    background-color: #f9fafb;
    margin: 10% auto 10% 2%;
    padding: 15px;
    width: 91%;
    border: 1px solid #e5e7eb;
    border-radius: 20px 20px 20px 0;
    font-size: 20px;
  }
</style>
