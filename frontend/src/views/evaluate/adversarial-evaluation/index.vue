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
                <a-space direction="vertical" :size="10" class="QAShower">
                  <div class="box-header">
                    <a-space>
                      <icon-message/>
                      <span style="font-size: 13px;">Model A</span>
                    </a-space>
                  </div>
                  <div class="QA" ref="QAModelA">
                    <a-space direction="vertical" :size="15" v-for="(divItem, index) in round.QA" :key="index" class="added-div">
                      <div class="userQuestion">
                        {{ divItem.question }}
                      </div>
                      <div class="modelResponse">
                        {{ divItem.answerA }}
                      </div>
                    </a-space>
                  </div>
                </a-space>
              </div>
              <div>
                {{ modelAname }}
              </div>
            </a-col>
            <a-col :span="12">
              <div class="text-box">
                <a-space direction="vertical" :size="10" class="QAShower">
                  <div class="box-header">
                    <a-space>
                      <icon-message/>
                      <span style="font-size: 13px;">Model B</span>
                    </a-space>
                  </div>
                  <div class="QA" ref="QAModelB">
                    <a-space direction="vertical" :size="15" v-for="(divItem, index) in round.QA" :key="index" class="added-div">
                      <div class="userQuestion">
                        {{ divItem.question }}
                      </div>
                      <div class="modelResponse">
                        {{ divItem.answerB }}
                      </div>
                    </a-space>
                  </div>
                </a-space>
              </div>
              <div>
                {{ modelBname }}
              </div>
            </a-col>
          </a-row>
        </a-card>
        <a-card class="questionInput">
          <a-row :gutter="16" v-if="evaluateFourButtonsVisible" style="padding-bottom: 20px;">
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
            <a-col :span="20">
              <a-input
                v-model="formModel.question"
                :placeholder="$t('evaluation.question.input')"
                allow-clear
              >
              </a-input>
            </a-col>
            <a-col :span="4">
              <a-button style="margin-right: 24px;" @click="selectClick">
                <template #icon>
                  <icon-plus></icon-plus>
                </template>
                {{ $t('evaluation.question.button.fill') }}
              </a-button>
              <a-button type="primary" @click="evaluateClick" :disabled="sendQuestionsDisabled">
                <template #icon>
                  <icon-arrow-up></icon-arrow-up>
                </template>
                {{ $t('evaluation.question.button.send') }}
              </a-button>
            </a-col>
          </a-row>
          <a-row :gutter="16">
            <a-col :span="8">
              <a-button style="margin-right: 20px; width: 100%;" :disabled="newRoundButtonDisabled" @click="newRoundClick">
                <template #icon>
                  <icon-dice></icon-dice>
                </template>
                {{ $t('evaluation.result.button.newround') }}
              </a-button>
            </a-col>
            <a-col :span="8">
              <a-button style="margin-right: 20px; width: 100%;" :disabled="regenerateButtonDisabled" @click="regenerateClick">
                <template #icon>
                  <icon-loop></icon-loop>
                </template>
                {{ $t('evaluation.result.button.regenerate') }}
              </a-button>
            </a-col>
            <a-col :span="8">
              <a-button class="aaa" style="margin-right: 20px; width: 100%" :disabled="adviseButtonDisabled" @click="adviseClick">
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
import EvaluateRound, { SelectedModel, queryLLMevaluateList, getLLMName, QuestionAndAnswer } from "@/api/evaluate";
import * as module from "module";
import {getToken} from "@/utils/auth";

const generateFormModel = () => {
  return {
    id: '',
    questionType: '',
    question: '',
    advise: '', // 增加建议属性，方便表单验证
  };
}

const formModel = ref(generateFormModel());
const lastQuestion = ref(''); // 存储上一个问题，用来重新生成结果
const { t } = useI18n();
const visible = ref(false);
const selectVisible = ref(false);
const evaluateFourButtonsVisible = ref(false); // 四个评价按钮是否可见，false表示不可见
const sendQuestionsDisabled = ref(true); // 发送按钮是否禁用，true表示禁用
const adviseButtonDisabled = ref(true); // 建议按钮是否禁用，true表示禁用
const modelAname = ref('');
const modelBname = ref('');
const newRoundButtonDisabled = ref(true);
const regenerateButtonDisabled = ref(true);
const isOkButtonDisabled = ref(false); // 反馈建议的ok按钮是否禁用属性,false表示没有禁用
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
const round = reactive(new EvaluateRound(-1));
const selectedQuestions = ref('');
const QAModelA = ref();
const QAModelB = ref();

watch(() => formModel.value.questionType, (newQuestionType, oldQuestionType) => {
  selectedQuestions.value = '';
}); // 问题种类改变时，问题选项会清零，否则上次选择的内容会遗留
const lengthRules = [
  {
    required: false,
    validator: (value: string, callback: (error?: string) => void) => {
      return new Promise<void>((resolve) => {
        window.setTimeout(() => {
          value = formModel.value.advise;
          isOkButtonDisabled.value = false;
          if (value.length > 100) { // 防止用户用大量字符串恶意攻击系统
            isOkButtonDisabled.value = true;
            callback(proxy.$t('evaluation.advice.error.default'));
          }
          resolve();
        }, 1);
      });
    },
    trigger: ['input'],
  },
];
const QuestionTypeSelectOptions = computed<SelectOptionData[]>(() => [
  {
    label: "机器翻译",
    value: '机器翻译',
  },
  {
    label: "数学运算",
    value: '数学运算',
  },
]);
const QuestionSelectOptions = computed<SelectOptionData[]>(() => {
  if (formModel.value.questionType === '机器翻译') { // 之后填充的问题设定在此框架上修改具体内容即可
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
  if (formModel.value.questionType === '数学运算') {
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

const scrollToBottom = () => {
    QAModelA.value.scrollTop = QAModelA.value.scrollHeight;
    QAModelB.value.scrollTop = QAModelB.value.scrollHeight;
  }

const confirmClick = () => {
    round.modelA = Number(formModel.value.id);
    round.getModelB();
    sendQuestionsDisabled.value = false; // 解除send按钮禁用
    
};
const adviseClick = () => {
  visible.value = true;
  isOkButtonDisabled.value = false;
};
const selectClick = () => {
  selectVisible.value = true;
};
const evaluateClick = async () => {
  sendQuestionsDisabled.value = true;
  if (!formModel.value.question || formModel.value.question.trim() === '')
  {
    window.alert(proxy.$t('evaluation.question.button.emptyMsg'));
  } else {
    round.QA.push(new QuestionAndAnswer(formModel.value.question, '...', '...'));
    await nextTick(() => {
      scrollToBottom();
    });
    lastQuestion.value = formModel.value.question;
    formModel.value.question = '';
    await round.getStreamResponse(getToken()!, QAModelA.value, QAModelB.value);
    evaluateFourButtonsVisible.value = true;
  }
  sendQuestionsDisabled.value = false;
  newRoundButtonDisabled.value = false;
  regenerateButtonDisabled.value = false;
  adviseButtonDisabled.value = false;
};
const handleSubmit = () => {
  formModel.value.advise = '';
  adviseButtonDisabled.value = true;
};
const handleCancel = () => {
  visible.value = false;
  formModel.value.advise = '';
};

const handleSelect = () => {
  formModel.value.question = selectedQuestions.value; // 填充问题对话框确定按钮事件的绑定
  formModel.value.questionType = '';
  selectedQuestions.value = '';
};

const handleCancelSelect = () => {
  formModel.value.question = '';
  formModel.value.questionType = '';
};
const aBetterClick = async () => { // 前面的getmodelB调用后没有及时更新可能也是没有在调用时加await async?
  if (round.modelA) {
    round.result = 1;
    evaluateFourButtonsVisible.value = false;
    let tempName = await getLLMName(round.modelA.toString());
    modelAname.value = tempName;
    tempName = await getLLMName(round.modelB.toString());
    modelBname.value = tempName;
    sendQuestionsDisabled.value = true;
    regenerateButtonDisabled.value = true;
    console.log(round);
    round.updateEloResult();
  }
}

const bBetterClick = async () => {
  if (round.modelA) {
    round.result = -1;
    evaluateFourButtonsVisible.value = false;
    let tempName = await getLLMName(round.modelA.toString());
    modelAname.value = tempName;
    tempName = await getLLMName(round.modelB.toString());
    modelBname.value = tempName;
    sendQuestionsDisabled.value = true;
    regenerateButtonDisabled.value = true;
    round.updateEloResult();
  }
}

const abGoodClick = async () => {
  if (round.modelA) {
    round.result = 0;
    evaluateFourButtonsVisible.value = false;
    let tempName = await getLLMName(round.modelA.toString());
    modelAname.value = tempName;
    tempName = await getLLMName(round.modelB.toString());
    modelBname.value = tempName;
    sendQuestionsDisabled.value = true;
    regenerateButtonDisabled.value = true;
    round.updateEloResult();
  }
}
const abBadClick = async () => {
  if (round.modelA) {
    round.result = 0;
    evaluateFourButtonsVisible.value = false;
    let tempName = await getLLMName(round.modelA.toString());
    modelAname.value = tempName;
    tempName = await getLLMName(round.modelB.toString());
    modelBname.value = tempName;
    sendQuestionsDisabled.value = true;
    regenerateButtonDisabled.value = true;
    round.updateEloResult();
  }
}
const newRoundClick = async () => {
  round.QA = [] as QuestionAndAnswer[];
  round.modelA = -1;
  round.modelB = -1;
  modelAname.value = '';
  modelBname.value = '';

  formModel.value.id = '';

  sendQuestionsDisabled.value = true;
  adviseButtonDisabled.value = true;
  isOkButtonDisabled.value = true;
  newRoundButtonDisabled.value = true;
  regenerateButtonDisabled.value = true;
  evaluateFourButtonsVisible.value = false;

}
const regenerateClick = async () => {
  round.QA.pop();
  round.QA.push(new QuestionAndAnswer(lastQuestion.value, '...', '...'));
  await nextTick(() => {
    scrollToBottom();
  });
  await round.getStreamResponse(getToken()!, QAModelA.value, QAModelB.value);
}
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
  margin-left: 7%;
  padding: 15px;
  width: 91%;
  border: 1px solid #fee6ca;
  border-radius: 20px 20px 0 20px;
  font-size: 20px;
}

.modelResponse {
  background-color: #f9fafb;
  margin-left: 2%;
  padding: 15px;
  width: 91%;
  border: 1px solid #e5e7eb;
  border-radius: 20px 20px 20px 0;
  font-size: 20px;
}

</style>
