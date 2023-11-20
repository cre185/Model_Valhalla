<template>
  <div class="container">
    <Breadcrumb :items="['menu.list', 'menu.list.cardList']" />
    <a-row :gutter="20" align="stretch">
      <a-col :span="24">
        <a-card class="general-card">
          <template #title>
            <div class="custom-title"><b>{{ $t('evalution.rules.title') }}</b></div>
          </template>
          <a-list :bordered=false :split=false>
            <a-list-item style="width: auto;">{{ $t('evalution.rules.one') }}</a-list-item>
            <a-list-item style="width: auto;">{{ $t('evalution.rules.two') }}</a-list-item>
            <a-list-item style="width: auto;">{{ $t('evalution.rules.three') }}</a-list-item>
            <a-list-item style="width: auto;">{{ $t('evalution.rules.four') }}</a-list-item>
          </a-list>
        </a-card>
        <a-card :bordered=false>
          <template #title>
            <div class="custom-title"><b>{{ $t('evalution.select.models') }}</b></div>
          </template>
          <a-row :gutter="16">
            <a-col :span="18">
              <a-form :model="formModel" :label-col-props="{ span: 4 }" :wrapper-col-props="{ span: 8 }"
                label-align="left">
                <a-form-item 
                  field="filterType"
                  :label="$t('evalution.select.models.title')"
                  :label-col-props="{ span: 4 }"
                  :wrapper-col-props="{ span: 10 }"
                  >
                  <a-select v-model="formModel.name" :options="ModelSelectOptions"
                    :placeholder="$t('searchTable.form.selectDefault')" />
                </a-form-item>
              </a-form>
            </a-col>
            <a-col :span="6">
              <a-button type="primary" style="margin-right: 20px;">
                <template #icon>
                  <icon-check></icon-check>
                </template>
                {{ $t('evalution.select.models.confirm') }}
              </a-button>
              <a-button>
                <template #icon>
                  <icon-refresh></icon-refresh>
                </template>
                {{ $t('evalution.select.models.reset') }}
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
                    这是文本框 1
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
                  <div class="box-textA">
                    这是文本框 1
                  </div>
                </a-space>
              </div>
            </a-col>
          </a-row>
        </a-card>
        <a-card class="questionInput">
          <a-row :gutter="16" style="padding-bottom: 20px;">
            <a-col :span="18">
              <a-input :placeholder="$t('evalution.question.input')" allow-clear>
              
              </a-input>
            </a-col>
            <a-col :span="6">
              <a-button style="margin-right: 20px;">
                <template #icon>
                  <icon-plus></icon-plus>
                </template>
                {{ $t('evalution.question.button.fill') }}
              </a-button>
              <a-button type="primary">
                <template #icon>
                  <icon-arrow-up></icon-arrow-up>
                </template>
                {{ $t('evalution.question.button.send') }}
              </a-button>
            </a-col>
          </a-row>
          <a-row :gutter="16">
            <a-col :span="8">
              <a-button style="margin-right: 20px; width: 100%;" :disabled=false>
                <template #icon>
                  <icon-delete></icon-delete>
                </template>
                {{ $t('evalution.result.button.clear') }}
              </a-button>
            </a-col>
            <a-col :span="8">
              <a-button style="margin-right: 20px; width: 100%" :disabled=false>
                <template #icon>
                  <icon-loop></icon-loop>
                </template>
                {{ $t('evalution.result.button.regenerate') }}
              </a-button>
            </a-col>
            <a-col :span="8">
              <a-button style="margin-right: 20px; width: 100%" :disabled=false>
                <template #icon>
                  <icon-book></icon-book>
                </template>
                {{ $t('evalution.result.button.advise') }}
              </a-button>
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
import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';

const generateFormModel = () => {
  return {
    name: '',
  };
}
const formModel = ref(generateFormModel());
const { t } = useI18n();
const ModelSelectOptions = computed<SelectOptionData[]>(() => [
  {
    label: t('evalution.select.models.gpt3.5'),
    value: 'Gpt-3.5',
  },
  {
    label: t('evalution.select.models.baidu'),
    value: '文心一言',
  },
  {
    label: t('evalution.select.models.Thu'),
    value: 'ChatGLM',
  },
  {
    label: t('evalution.select.models.Google'),
    value: 'Google Bard',
  },
  {
    label: t('evalution.select.models.iFLYTEK'),
    value: '讯飞星火',
  },
]);
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
