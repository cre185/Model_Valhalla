<template>
  <div class="container">
    <Breadcrumb :items="['menu.evaluate', 'menu.evaluate.adversarialEvaluation']" />
    <a-row :gutter="20" align="stretch">
      <a-col :span="24">
        <a-card class="general-card">
          <template #title>
            <div class="custom-title"><b>{{ $t('evaluation.rules.title') }}</b></div>
          </template>
          <a-timeline>
            <a-timeline-item>{{ $t('evaluation.rules.one') }}</a-timeline-item>
            <a-timeline-item>{{ $t('evaluation.rules.two') }}</a-timeline-item>
            <a-timeline-item>{{ $t('evaluation.rules.three') }}</a-timeline-item>
            <a-timeline-item>{{ $t('evaluation.rules.four') }}</a-timeline-item>
          </a-timeline>
        </a-card>
        <a-card :bordered=false>
          <template #title>
            <div class="custom-title"><b>{{ $t('evaluation.select.models') }}</b></div>
          </template>
          <a-row :gutter="16">
            <a-col :span="18">
              <a-form :model="formModel" :label-col-props="{ span: 4 }" :wrapper-col-props="{ span: 8 }"
                      label-align="left">
                <a-form-item
                    field="filterType"
                    :label="$t('evaluation.select.models.title')"
                    :label-col-props="{ span: 4 }"
                    :wrapper-col-props="{ span: 10 }"
                >
                  <a-select v-model="formModel.id" :options="ModelSelectOptions"
                            :placeholder="$t('searchTable.form.selectDefault')" />
                </a-form-item>
              </a-form>
            </a-col>
            <a-col :span="6">
              <a-button type="primary" style="margin-right: 20px;" @click="confirmClick">
                <template #icon>
                  <icon-check></icon-check>
                </template>
                {{ $t('evaluation.select.models.confirm') }}
              </a-button>
            </a-col>
          </a-row>
        </a-card>
        <a-card class="resultShow">
          <a-row :gutter="16">
            <a-col :span="12">
              <div class="text-box">
                <a-space direction="vertical" :size="10">
                  <div class="box-header">
                    <icon-message style="margin-right: 8px; font-size: 20px;"/>
                    <span style="font-size: 18px;">Model A</span>
                  </div>
                  <div class="box-textA">
                    这是文本框A
                  </div>
                </a-space>
              </div>
            </a-col>
            <a-col :span="12">
              <div class="text-box">
                <a-space direction="vertical" :size="10">
                  <div class="box-header">
                    <icon-message style="margin-right: 8px; font-size: 20px;"/>
                    <span style="font-size: 18px;">Model B</span>
                  </div>
                  <div class="box-textB">
                    这是文本框B
                  </div>
                </a-space>
              </div>
            </a-col>
          </a-row>
        </a-card>
        <a-card class="questionInput">
          <a-row :gutter="16" v-if="evaluateButtons" style="padding-bottom: 20px;">
            <a-col :span="6">
              <a-button @click="aBetterClick" style="margin-right: 20px; width: 100%">
                <template #icon>
                  <span class="iconfont icon-hand-left1"></span>
                </template>
                {{ $t('evaluation.evaluate.modelA') }}
              </a-button>
            </a-col>
            <a-col :span="6">
              <a-button @click="bBetterClick" style="margin-right: 20px; width: 100%">
                <template #icon>
                  <span class="iconfont icon-hand-right1"></span>
                </template>
                {{ $t('evaluation.evaluate.modelB') }}
              </a-button>
            </a-col>
            <a-col :span="6">
              <a-button @click="abGoodClick" style="margin-right: 20px; width: 100%">
                <template #icon>
                  <span class="iconfont icon-Outline_fuben11"></span>
                </template>
                {{ $t('evaluation.evaluate.both') }}
              </a-button>
            </a-col>
            <a-col :span="6">
              <a-button @click="abBadClick" style="margin-right: 20px; width: 100%">
                <template #icon>
                  <span class="iconfont icon-Outline_fuben24"></span>
                </template>
                {{ $t('evaluation.evaluate.neither') }}
              </a-button>
            </a-col>
          </a-row>
          <a-row :gutter="16" style="padding-bottom: 20px;">
            <a-col :span="18">
              <a-input
                v-model="formModel.question"
                :placeholder="$t('evaluation.question.input')"
                allow-clear
              >
              </a-input>
            </a-col>
            <a-col :span="6">
              <a-button style="margin-right: 20px;" @click="selectClick">
                <template #icon>
                  <icon-plus></icon-plus>
                </template>
                {{ $t('evaluation.question.button.fill') }}
              </a-button>
              <a-button type="primary" @click="evaluateClick">
                <template #icon>
                  <icon-arrow-up></icon-arrow-up>
                </template>
                {{ $t('evaluation.question.button.send') }}
              </a-button>
            </a-col>
          </a-row>
          <a-row :gutter="16">
            <a-col :span="8">
              <a-button style="margin-right: 20px; width: 100%;" :disabled=false>
                <template #icon>
                  <icon-delete></icon-delete>
                </template>
                {{ $t('evaluation.result.button.clear') }}
              </a-button>
            </a-col>
            <a-col :span="8">
              <a-button style="margin-right: 20px; width: 100%" :disabled=false>
                <template #icon>
                  <icon-loop></icon-loop>
                </template>
                {{ $t('evaluation.result.button.regenerate') }}
              </a-button>
            </a-col>
            <a-col :span="8">
              <a-button style="margin-right: 20px; width: 100%" :disabled=false @click="adviseClick">
                <template #icon>
                  <icon-book></icon-book>
                </template>
                {{ $t('evaluation.result.button.advise') }}
              </a-button>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
      <template>
        <a-modal
            class="selectModal"
            v-model:visible="selectVisible"
            :ok-text="$t('evaluation.question.select.button.confirm')"
            @ok="handleSelect"
            :cancel-text="$t('evaluation.question.select.button.quit')"
            @cancel="handleCancelSelect"
            :closable=false
            :modal-style="{width: '700px'}"
        >
          <a-row :gutter="16">
            <a-col :span="8">
              <a-select
                  v-model="formModel.questionType"
                  :placeholder="$t('evaluation.question.select.type.default')"
                  :options="QuestionTypeSelectOptions"
              >

              </a-select>
            </a-col>
            <a-col :span="16">
              <a-select
                  v-model="selectedQuestions"
                  :placeholder="$t('evaluation.question.select.content.default')"
                  :options="QuestionSelectOptions"
              >

              </a-select>
            </a-col>
          </a-row>
        </a-modal>
      </template>
      <template>
        <a-modal
            class="adviseModal"
            v-model:visible="visible"
            :modal-style="{width: '500px', height: '400px'}"
            :ok-text="$t('evaluation.advise.button.submit')"
            @ok="handleSubmit"
            :cancel-text="$t('evaluation.advise.button.cancel')"
            @cancel="handleCancel"
            :ok-button-props="{ disabled: isOkButtonDisabled }"
        >
          <template #title>
            <span style="color:dodgerblue">{{ $t('evaluation.advise.title') }}</span>
          </template>
          <a-row :gutter="-8">
          <a-form
            :model="formModel"
            label-align="right"
          >
            <a-form-item
              field="advise"
              :label="$t('evaluation.advise.subtitle')"
              :rules="lengthRules"
              :label-col-props="{ span: 5 }"
              :wrapper-col-props="{ span: 19 }"
              >
              <a-textarea
                class="adviseInput"
                v-model="formModel.advise"
                display:center
                :placeholder="$t('evaluation.advise.default')"
                allow-clear
                :style="{height: '220px'}"
              >
              </a-textarea>
            </a-form-item>
          </a-form>
          </a-row>
        </a-modal>
      </template>
    </a-row>
  </div>
</template>

<script lang="ts" setup>
import {computed, ref, reactive, watch, nextTick, onMounted, getCurrentInstance} from 'vue';
import { useI18n } from 'vue-i18n';
import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
import useVisible from '@/hooks/visible';
import '@/assets/icondataset/iconfont.css'
import EvaluateRound, { SelectedModel, queryLLMevaluateList } from "@/api/evaluate";
import * as module from "module";

const generateFormModel = () => {
  return {
    id: '',
    questionType: '',
    question: '',
    advise: '', // 增加建�??属性，方便表单验证
  };
  const selectClick = () => {
    selectVisible.value = true;
  }
  const handleSubmit = () => {

const formModel = ref(generateFormModel());
const { t } = useI18n();
const visible = ref(false);
const selectVisible = ref(false);
const evaluateButtons = ref(true);
const isOkButtonDisabled = ref(false); // 反�?�建�?的ok按钮�?否�?�用属�?,false表示没有禁用
const { proxy } = getCurrentInstance();
const SelectedModelInfo = ref<SelectedModel[]>();
SelectedModelInfo.value = (await queryLLMevaluateList()).data;
const ModelSelectOptions = computed<SelectOptionData[]>(() => {
  return (SelectedModelInfo.value || []).map((model) => ({
    label: model.name,
    value: model.id,
  }));
});
const ModelAId = computed(() => formModel.value.id);
const ABresult = ref<EvaluateRound>();
const selectedQuestions = ref('');
watch(() => formModel.value.questionType, (newQuestionType, oldQuestionType) => {
  selectedQuestions.value = '';
}); // �?题�?�类改变时，�?题选项会清零，否则上�?�选择的内容会遗留
const lengthRules = [
  {
    required: false,
    validator: (value: string, callback: (error?: string) => void) => {
      return new Promise<void>((resolve) => {
        window.setTimeout(() => {
          value = formModel.value.advise;
          if (value.length > 100) { // 防�?�用户用大量字�?�串恶意攻击系统
            isOkButtonDisabled.value = true;
            callback(proxy.$t('evaluation.advice.error.default'));
          }
          resolve();
        }, 1000);
      });
    },
    trigger: ['change', 'blur'],
  },
];
const QuestionTypeSelectOptions = computed<SelectOptionData[]>(() => [
  {
    label: "机器翻译",
    value: '机器翻译',
  },
  {
    label: "数�?�运�?",
    value: '数�?�运�?'
  },
]);
const QuestionSelectOptions = computed<SelectOptionData[]>(() => {
  if (formModel.value.questionType === '机器翻译') { // 之后�?充的�?题�?�定在�?��?�架上修改具体内容即�?
    return [
      {
        label: "Question A(translate)",
        value: 'Question A(translate)',
      },
      {
        label: "Question D(translate)",
        value: 'Question D(translate)',
      },
    ];
  }
  if (formModel.value.questionType === '数�?�运�?') {
    return [
      {
        label: "Question B(evaluate)",
        value: 'Question B(evaluate)',
      },
      {
        label: "Question C(evaluate)",
        value: 'Question C(evaluate)',
      },
    ];
  }
  return [];
});
const confirmClick = () => {
    ABresult.value = new EvaluateRound(-1);
    ABresult.value.modelA = Number(formModel.value.id);
    ABresult.value.getModelB();
    formModel.value.question = ABresult.value.modelB.toString(); // 检验是否�?�确调用getModelB()
};
const adviseClick = () => {
  visible.value = true;
  isOkButtonDisabled.value = false;
};
const selectClick = () => {
  selectVisible.value = true;
};
const evaluateClick = () => {
  evaluateButtons.value = true;
};
const handleSubmit = () => {
  formModel.value.advise = '';
  // formModel.value.question = adviseText.value;
};
const handleCancel = () => {
  visible.value = false;
  formModel.value.advise = '';
};

const handleSelect = () => {
  formModel.value.question = selectedQuestions.value; // �?充问题�?�话框确定按�?事件的绑�?
  formModel.value.questionType = '';
  selectedQuestions.value = '';
};

const handleCancelSelect = () => {

};
const aBetterClick = () => {
  if (ABresult.value?.modelA) {
    ABresult.value.result = 1;
    formModel.value.question = ABresult.value.result.toString();
  }
}

const bBetterClick = () => {
  if (ABresult.value?.modelA) {
    ABresult.value.result = -1;
    formModel.value.question = ABresult.value.result.toString();
  }
}

const abGoodClick = () => {
  if (ABresult.value?.modelA) {
    ABresult.value.result = 0;
    formModel.value.question = ABresult.value.result.toString();
  }
}

const abBadClick = () => {
  if (ABresult.value?.modelA) {
    ABresult.value.result = 0;
    formModel.value.question = ABresult.value.result.toString();
  }
}
</script>

<script lang="ts">
export default {
  name: 'Card',
};
</script>

<style scoped lang="less">
.container {
  padding: 0 20px 20px 20px;

  :deep(.arco-list-content) {
    overflow-x: hidden;
  }

  :deep(.arco-card-meta-title) {
    font-size: 14px;
  }
}

:deep(.arco-list-col) {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
}

:deep(.arco-list-item) {
  width: 33%;
}

:deep(.block-title) {
  margin: 0 0 12px 0;
  font-size: 14px;
}

:deep(.list-wrap) {

  // min-height: 140px;
  .list-row {
    align-items: stretch;

    .list-col {
      margin-bottom: 16px;
    }
  }

  :deep(.arco-space) {
    width: 100%;

    .arco-space-item {
      &:last-child {
        flex: 1;
      }
    }
  }
}
.custom-title {
  font-size: 18px;
}
.text-box {
  border: 1px solid #ccc;
  padding: 10px;
  height: 300px;
}
.box-header {
  display: flex;
  align-items: center;
}

</style>
