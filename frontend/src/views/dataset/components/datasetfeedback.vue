<template>
    <a-modal :closable=false :ok-text="$t('dataset.feedback.ok.text')" @ok="handleSubmit" @cancel="handleCancel">

        <div style="display: flex; justify-content: center; flex-direction: row;">
            <a-button @click="switchClick('feedbackForm')" size="large"
                :style="{ marginRight: '10px', backgroundColor: '#fff', color: feedbackColor }">
                <template #icon>
                    <icon-edit />
                </template>
                {{ $t('dataset.feedback.title') }}
            </a-button>
            <a-button @click="switchClick('reportForm')" size="large"
                :style="{ backgroundColor: '#fff', color: reportColor }">
                <template #icon>
                    <icon-message />
                </template>
                {{ $t('dataset.report.title') }}
            </a-button>
        </div>
        <div style="border-top: 2px solid rgb(var(--gray-2)); width: 100%; margin-top: 10px; margin-bottom: 10px;"></div>
        <template v-if="currentForm === 'feedbackForm'">
            <a-form style="padding-right: 10px;">
                <a-form-item :label="$t('dataset.feedback.dataset.name')">
                    <a-select v-model="formModel.datasetName" :options="DatasetSelectOptions" :disabled="datasetIdKnown"
                        :placeholder="$t('dataset.feedback.dataset.name.defalut')">
                    </a-select>
                </a-form-item>
                <a-form-item :label="$t('dataset.feedback.dataset.feedtype')">
                    <a-radio-group v-model="formModel.feedbackType" style="margin-top: 5px;">
                        <a-grid :cols="2" :colGap="24" :rowGap="16">
                            <a-grid-item>
                                <a-radio value="数据错误">{{ $t('dataset.feedback.dataset.feedtype.one') }}</a-radio>
                            </a-grid-item>
                            <a-grid-item>
                                <a-radio value="数据不全">{{ $t('dataset.feedback.dataset.feedtype.two') }}</a-radio>
                            </a-grid-item>
                            <a-grid-item>
                                <a-radio value="存在可更新版本">{{ $t('dataset.feedback.dataset.feedtype.three') }}</a-radio>
                            </a-grid-item>
                            <a-grid-item>
                                <a-radio value="相关信息错误">{{ $t('dataset.feedback.dataset.feedtype.four') }}</a-radio>
                            </a-grid-item>
                            <a-grid-item>
                                <a-radio value="其他">{{ $t('dataset.feedback.dataset.feedtype.five') }}</a-radio>
                            </a-grid-item>
                        </a-grid>
                    </a-radio-group>
                </a-form-item>
                <a-form-item :label="$t('dataset.feedback.dataset.description')">
                    <a-textarea v-model="formModel.feedbackContent"
                        :placeholder="$t('dataset.feedback.dataset.description.default')"
                        :max-length="{length:100,errorOnly:false}"
                        allow-clear
                        show-word-limit
                        style="margin-top: 5px; height: 150px;">

                    </a-textarea>
                </a-form-item>
                <a-form-item :label="$t('dataset.upload.button.title')">
                    <div style="display: flex; flex-direction: column; align-items: left;">
                    <a-upload   action="http://127.0.0.1:8000/dataset/test_upload"
                               :file-list="formModel.annex"
                                @success="uploadChange"
                                :limit = 1
                                >
                        
                    </a-upload>
                    <span style="margin-top: 5px; font-size: smaller; color: darkgray;">{{ $t('dataset.upload.file.title.default') }}</span>
                    </div>
                </a-form-item>
            </a-form>
        </template>
        <template v-else-if="currentForm === 'reportForm'">
            <a-form style="padding-right: 10px;">
                <a-form-item :label="$t('dataset.feedback.dataset.name')">
                    <a-select v-model="formModel.datasetName" :options="DatasetSelectOptions"
                        :placeholder="$t('dataset.feedback.dataset.name.defalut')">
                    </a-select>
                </a-form-item>
                <a-form-item :label="$t('dataset.report.reason')">
                    <a-radio-group v-model="formModel.reportReason" style="margin-top: 5px;">
                        <a-grid :cols="1" :colGap="24" :rowGap="16">
                            <a-grid-item>
                                <a-radio value="违法许可">{{ $t('dataset.report.reason.one') }}</a-radio>
                            </a-grid-item>
                            <a-grid-item>
                                <a-radio value="包含非法内容">{{ $t('dataset.report.reason.two') }}</a-radio>
                            </a-grid-item>
                            <a-grid-item>
                                <a-radio value="不利于社区和平">{{ $t('dataset.report.reason.three') }}</a-radio>
                            </a-grid-item>
                        </a-grid>
                    </a-radio-group>
                </a-form-item>
                <a-form-item :label="$t('dataset.feedback.dataset.description')">
                    <a-textarea v-model="formModel.reportContent"
                        :placeholder="$t('dataset.feedback.dataset.description.default')"
                        :max-length="{length:100,errorOnly:false}"
                        allow-clear
                        show-word-limit
                        style="margin-top: 5px; height: 150px;">

                    </a-textarea>
                </a-form-item>
            </a-form>
        </template>
    </a-modal>
</template>
<script lang="ts" setup>
import { ref, computed, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { FileItem } from '@arco-design/web-vue';
import { simplifiedQueryDatasetList, SelectedDataset, sendFeedback, sendReport} from "@/api/dataset";
import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
import {getToken} from "@/utils/auth";

const props = defineProps({
    datasetid: {
      type: String,
      default: '-1',
    },
});
console.log(props.datasetid)
const currentForm = ref('feedbackForm')
const datasetIdKnown = ref(false) // datasetid是否已确定，决定是否禁用选择框
const generateFormModel = () => {
    if(props.datasetid === '-1')
    {
        return {
            datasetName: '',
            feedbackType: '',
            feedbackContent: '',
            reportReason: '',
            reportContent: '',
            annex: [] as FileItem[],
            file: [] as File[] ,
        }
    }
    datasetIdKnown.value = true;
    return {
        datasetName: props.datasetid,
        feedbackType: '',
        feedbackContent: '',
        reportReason: '',
        reportContent: '',
        annex: [] as FileItem[],
        file: [] as File[] , 
    }
};
/* watch(
        () => currentForm,
    
        async (newModelid, oldModelid) => {
            try {
                currentForm.value = newModelid.value;

            } catch (error) {
                console.error('Error fetching data:', error);
            }
            },
        {
            immediate: true // 立即执行一次回调函数
        }
     ); */
const feedbackColor = ref('rgb(45, 92, 246)');
const reportColor = ref('#000000');
const formModel = ref(generateFormModel());
const { t } = useI18n();

const SelectedModelInfo = ref<SelectedDataset[]>();
SelectedModelInfo.value = (await simplifiedQueryDatasetList()).data;
const DatasetSelectOptions = computed<SelectOptionData[]>(() => {
    return (SelectedModelInfo.value || []).map((model) => ({
        label: model.name,
        value: model.id,
    }));
});
const uploadChange = async (fileItem: FileItem) => {
    // fileItemList.push(fileItem);
    formModel.value.annex.push(fileItem);
    if(fileItem.file)
    {
        formModel.value.file.push(fileItem.file);
        console.log(formModel.value.file[0].name);
    }
    
  };
const handleSubmit = async () => {
    if(currentForm.value === 'feedbackForm') {
        await sendFeedback(getToken()!, formModel.value);
    }
    if(currentForm.value === 'reportForm') {
        await sendReport(getToken()!, formModel.value);
    }

    formModel.value = generateFormModel();
}
const switchClick = async (formType: string) => {
    currentForm.value = formType;
    if (formType === 'feedbackForm') {
        feedbackColor.value = 'rgb(45, 92, 246)';
        reportColor.value = '#000000';
    }
    if (formType === 'reportForm') {
        feedbackColor.value = '#000000';
        reportColor.value = 'rgb(45, 92, 246)';
    }
}
const handleCancel = async () => {
    currentForm.value = 'feedbackForm';
    formModel.value = generateFormModel();
    switchClick(currentForm.value);
}
</script>
<style scoped lang="less"></style>
