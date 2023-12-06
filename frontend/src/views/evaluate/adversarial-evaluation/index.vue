<template>
  <div class="container">
    <Breadcrumb :items="['menu.evaluate', 'menu.evaluate.adversarialEvaluation']" />
    <a-row :gutter="20" align="stretch">
      <a-col :span="24">
        <a-card class="general-card" >
          <template #title>
            <div class="custom-title"><b>{{ $t('evaluation.rules.title') }}</b></div>
          </template>
          <a-space direction="vertical" size="large">
            <div class="boxTest">
              <div class="contentTest">
                <h3>
                  {{ $t('evaluation.rules.one') }}
                </h3>
              </div>
            </div>
            <div class="boxTest">
              <div class="contentTest">
                <h3>
                  {{ $t('evaluation.rules.two') }}
                </h3>
              </div>
            </div>
            <div class="boxTest">
              <div class="contentTest">
                <h3>
                  {{ $t('evaluation.rules.three') }}
                </h3>
              </div>
            </div>
            <div class="boxTest">
              <div class="contentTest">
                <h3>
                  {{ $t('evaluation.rules.four') }}
                </h3>
              </div>
            </div>
          </a-space>
        </a-card>
        <br>
        <a-card class="resultShow">
          <div id="selectModel">
            <a-select v-model="formModel.id" :options="ModelSelectOptions"
                      :placeholder="$t('evaluation.select.models')" />
            <a-button type="primary" style="margin-right: 20px;" @click="confirmClick" :disabled="confirmButtonDisabled">
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
              <div style="font-weight: bold; padding-top: 5px;">
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
              <div style="font-weight: bold; padding-top: 5px;">
                {{ modelBname }}
              </div>
            </a-col>
          </a-row>
        </a-card>
        <a-card class="questionInput">
          <a-row :gutter="16" v-if="evaluateFourButtonsVisible" style="padding-bottom: 20px;">
            <a-col :span="6">
              <a-button id="aBetter" @click="aBetterClick" style="margin-right: 20px; width: 100%" :disabled="evaluateFourButtonsDisabled">
                <template #icon>
                  <span class="iconfont icon-hand-left1"></span>
                </template>
                {{ $t('evaluation.evaluate.modelA') }}
              </a-button>
            </a-col>
            <a-col :span="6">
              <a-button id="bBetter" @click="bBetterClick" style="margin-right: 20px; width: 100%" :disabled="evaluateFourButtonsDisabled">
                <template #icon>
                  <span class="iconfont icon-hand-right1"></span>
                </template>
                {{ $t('evaluation.evaluate.modelB') }}
              </a-button>
            </a-col>
            <a-col :span="6">
              <a-button id="abGood" @click="abGoodClick" style="margin-right: 20px; width: 100%" :disabled="evaluateFourButtonsDisabled">
                <template #icon>
                  <span class="iconfont icon-Outline_fuben11"></span>
                </template>
                {{ $t('evaluation.evaluate.both') }}
              </a-button>
            </a-col>
            <a-col :span="6">
              <a-button id="abBad" @click="abBadClick" style="margin-right: 20px; width: 100%" :disabled="evaluateFourButtonsDisabled">
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
                @press-enter="evaluateClick"
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
import EvaluateRound, { SelectedModel, queryLLMevaluateList, getLLMName, QuestionAndAnswer} from "@/api/evaluate";
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
const evaluateFourButtonsDisabled = ref(false); // 四个按钮是否可选
const sendQuestionsDisabled = ref(true); // 发送按钮是否禁用，true表示禁用
const adviseButtonDisabled = ref(true); // 建议按钮是否禁用，true表示禁用
const confirmButtonDisabled = ref(false);
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
    label: t('evaluation.question.fill.typeone'),
    value: '机器翻译',
  },
  {
    label: t('evaluation.question.fill.typetwo'),
    value: '数学运算',
  },
  {
    label: t('evaluation.question.fill.typethree'),
    value: '文本生成',
  },
  {
    label: t('evaluation.question.fill.typefour'),
    value: '推理和逻辑',
  },
  {
    label: t('evaluation.question.fill.typefive'),
    value: '语法和语义理解',
  }
]);
const QuestionSelectOptions = computed<SelectOptionData[]>(() => {
  if (formModel.value.questionType === '机器翻译') { // 之后填充的问题设定在此框架上修改具体内容即可
    return [
      {
        label: t('evaluation.evaluate.fill.typeone.q1'),
        value: '请将“大家早上好”翻译成日语',
      },
      {
        label: t('evaluation.evaluate.fill.typeone.q2'),
        value: '请将下面这句话翻译成中文: I have never had such a fantastic start',
      },
      {
        label: t('evaluation.evaluate.fill.typeone.q3'),
        value: '请问“今天中午你吃了什么”用英语怎么说'
      },
      {
        label: t('evaluation.evaluate.fill.typeone.q4'),
        value: 'Please translate "这本书是由一位著名的作家写的" into English'
      },
      {
        label: t('evaluation.evaluate.fill.typeone.q5'),
        value: '请将“This is a well-known restaurant located in Shanghai”翻译成日语'
      },
    ];
  }
  if (formModel.value.questionType === '数学运算') {
    return [
      {
        label: t('evaluation.evaluate.fill.typetwo.q1'),
        value: '114+514等于多少',
      },
      {
        label: t('evaluation.evaluate.fill.typetwo.q2'),
        value: 'sin(x)关于x的导数是多少',
      },
      {
        label: t('evaluation.evaluate.fill.typetwo.q3'),
        value: '36除以7，余数是多少',
      },
      {
        label: t('evaluation.evaluate.fill.typetwo.q4'),
        value: '计算下面的式子："2 * (3 + 5) / 4"',
      },
      {
        label: t('evaluation.evaluate.fill.typetwo.q5'),
        value: '已知2x+4=10，x的值是多少',
      },
    ];
  }
  if (formModel.value.questionType === '文本生成') {
    return [
      {
        label: t('evaluation.evaluate.fill.typethree.q1'),
        value: '简述一下电影《战狼II》的情节',
      },
      {
        label: t('evaluation.evaluate.fill.typethree.q2'),
        value: '讲一个冷笑话',
      },
      {
        label: t('evaluation.evaluate.fill.typethree.q3'),
        value: '请写一首关于自由的诗歌',
      },
      {
        label: t('evaluation.evaluate.fill.typethree.q4'),
        value: '我计划去得克萨斯州旅行，请给我一份旅行指南',
      },
      {
        label: t('evaluation.evaluate.fill.typethree.q5'),
        value: '我最近想开始健身，请给我一些关于饮食上的建议',
      },
      {
        label: t('evaluation.evaluate.fill.typethree.q6'),
        value: '评价一下《原神》这款游戏',
      },
    ];
  }
  if (formModel.value.questionType === '推理和逻辑') {
    return [
      {
        label: t('evaluation.evaluate.fill.typefour.q1'),
        value: '如果今天是星期五，明天是哪一天？',
      },
      {
        label: t('evaluation.evaluate.fill.typefour.q2'),
        value: '假设A是B的兄弟，而B是C的兄弟，是否可以得出A是C的兄弟的结论？',
      },
      {
        label: t('evaluation.evaluate.fill.typefour.q3'),
        value: '如果所有人都会死亡，那么小明是否会死？',
      },
      {
        label: t('evaluation.evaluate.fill.typefour.q4'),
        value: '汤姆有一只喜欢骨头的宠物，那么他的宠物可能是狗吗？',
      },
      {
        label: t('evaluation.evaluate.fill.typefour.q5'),
        value: '小刚的父母都是AB型血，小刚可能是O型血吗',
      },
    ];
  }
  if (formModel.value.questionType === '语法和语义理解') {
    return [
      {
        label: t('evaluation.evaluate.fill.typefive.q1'),
        value: '找出下列句子中的语法错误："Every one of the students are here"',
      },
      {
        label: t('evaluation.evaluate.fill.typefive.q2'),
        value: '找出下列句子中的语义错误：自行车早上喜欢骑小明',
      },
      {
        label: t('evaluation.evaluate.fill.typefive.q3'),
        value: '检查下列句子是否有语法错误："He don\'t like apples."',
      },
    ];
  }
  return [];
});

const scrollToBottom = () => {
    QAModelA.value.scrollTop = QAModelA.value.scrollHeight;
    QAModelB.value.scrollTop = QAModelB.value.scrollHeight;
  }

const confirmClick = async () => {
    round.modelA = Number(formModel.value.id);
    round.QA = [] as QuestionAndAnswer[];
    await round.getModelB();
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
  if (sendQuestionsDisabled.value === true) {
    return;
  }
  if (!formModel.value.question || formModel.value.question.trim() === '')
  {
    window.alert(proxy.$t('evaluation.question.button.emptyMsg'));
  } else {
    sendQuestionsDisabled.value = true;
    round.QA.push(new QuestionAndAnswer(formModel.value.question, '...', '...'));
    await nextTick(() => {
      scrollToBottom();
    });
    await round.getStreamResponse(getToken()!, QAModelA.value, QAModelB.value, sendQuestionsDisabled); // 多传入了一个对象，直接传值不能奏效
    evaluateFourButtonsVisible.value = true;
    // sendQuestionsDisabled.value = false;
    lastQuestion.value = formModel.value.question;
    formModel.value.question = '';

  }
  confirmButtonDisabled.value = true;
  newRoundButtonDisabled.value = false;
  regenerateButtonDisabled.value = false;
  adviseButtonDisabled.value = false;
};
const handleSubmit = async () => {
  await round.sendAdvise(getToken()!, formModel.value.advise);
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
    let tempName = await getLLMName(round.modelA.toString());
    modelAname.value = tempName;
    tempName = await getLLMName(round.modelB.toString());
    modelBname.value = tempName;
    sendQuestionsDisabled.value = true;
    regenerateButtonDisabled.value = true;
    evaluateFourButtonsDisabled.value = true;
    const element = document.getElementById('aBetter');

    if (element) {
      element.style.backgroundColor = 'rgb(45, 92, 246)';
      element.style.color = 'white';
    }
    await round.updateEloResult();
  }
}

const bBetterClick = async () => {
  if (round.modelA) {
    round.result = -1;
    let tempName = await getLLMName(round.modelA.toString());
    modelAname.value = tempName;
    tempName = await getLLMName(round.modelB.toString());
    modelBname.value = tempName;
    sendQuestionsDisabled.value = true;
    regenerateButtonDisabled.value = true;
    evaluateFourButtonsDisabled.value = true;
    const element = document.getElementById('bBetter');

    if (element) {
      element.style.backgroundColor = 'rgb(45, 92, 246)';
      element.style.color = 'white';
    }
    await round.updateEloResult();
  }
}

const abGoodClick = async () => {
  if (round.modelA) {
    round.result = 0;
    let tempName = await getLLMName(round.modelA.toString());
    modelAname.value = tempName;
    tempName = await getLLMName(round.modelB.toString());
    modelBname.value = tempName;
    sendQuestionsDisabled.value = true;
    regenerateButtonDisabled.value = true;
    evaluateFourButtonsDisabled.value = true;
    const element = document.getElementById('abGood');

    if (element) {
      element.style.backgroundColor = 'rgb(45, 92, 246)';
      element.style.color = 'white';
    }
    await round.updateEloResult();
  }
}
const abBadClick = async () => {
  if (round.modelA) {
    round.result = 0;
    let tempName = await getLLMName(round.modelA.toString());
    modelAname.value = tempName;
    tempName = await getLLMName(round.modelB.toString());
    modelBname.value = tempName;
    sendQuestionsDisabled.value = true;
    regenerateButtonDisabled.value = true;
    evaluateFourButtonsDisabled.value = true;
    const element = document.getElementById('abBad');

    if (element) {
      element.style.backgroundColor = 'rgb(45, 92, 246)';
      element.style.color = 'white';
    }
    await round.updateEloResult();
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
  confirmButtonDisabled.value = false;
  evaluateFourButtonsVisible.value = false;

}
const regenerateClick = async () => {
  round.QA.pop();
  round.QA.push(new QuestionAndAnswer(lastQuestion.value, '...', '...'));
  await nextTick(() => {
    scrollToBottom();
  });
  sendQuestionsDisabled.value = true;
  await round.getStreamResponse(getToken()!, QAModelA.value, QAModelB.value, sendQuestionsDisabled);
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
