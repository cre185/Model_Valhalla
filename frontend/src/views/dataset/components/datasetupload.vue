<template>
    <a-modal @ok="handleUpload" :ok-text="$t('dataset.feedback.dataset.upload')" @cancel="handleCancel" :closable=false>
        <template #title>
            <div style="display: flex; align-items: center;">
                <icon-upload style="margin-right: 5px;"></icon-upload>
                {{ $t('dataset.upload.title') }}
            </div>
        </template>
        <a-form style="padding-right: 10px;">
            <a-form-item :label="$t('dataset.upload.name.title')">
                <a-input :placeholder="$t('dataset.upload.name.title.default')" v-model="UploadModel.datasetName">

                </a-input>

            </a-form-item>
            <a-form-item :label="$t('dataset.upload.application.title')">
                <a-select :placeholder="$t('dataset.upload.application.title.default')" :options="ApplicationOptions" v-model="UploadModel.datasetApplication">

                </a-select>

            </a-form-item>
            <a-form-item :label="$t('dataset.upload.introduction.title')">
                <a-textarea :placeholder="$t('dataset.upload.introduction.title.default')"
                    :max-length="{ length: 100, errorOnly: false }" show-word-limit style="height: 100px;" v-model="UploadModel.datasetIntroduction">

                </a-textarea>
            </a-form-item>
            <a-form-item :label="$t('dataset.upload.tag.title')">
                <a-tag v-for="(tag) of UploadModel.datasetTags" :key="tag" :closable=true @close="handleRemove(tag)"
                    style="margin-right: 5px;">
                    {{ tag }}
                </a-tag>
                <a-input v-if="showTagInput" ref="inputRef" :style="{ width: '90px' }" size="mini" v-model.trim="inputTag"
                    @keyup.enter="handleAdd" @blur="handleAdd" />
                <a-tag v-else :style="{
                    width: '60px',
                    backgroundColor: 'var(--color-fill-2)',
                    border: '1px dashed var(--color-fill-3)',
                    cursor: 'pointer',
                }" @click="handleEdit">
                    <template #icon>
                        <icon-plus />
                    </template>
                    {{ $t('dataset.upload.tag.add') }}
                </a-tag>
            </a-form-item>
            <a-form-item :label="$t('dataset.upload.file.title')">
                <a-upload action="http://127.0.0.1:8000/user/logout"
                            :file-list="UploadModel.annex"
                            @success="uploadChange"
                            :limit = 1
                            >

                </a-upload>
            </a-form-item>
        </a-form>
    </a-modal>
</template>

<script lang="ts" setup>
import { useI18n } from 'vue-i18n';
import { computed, nextTick, ref } from 'vue';
import { FileItem, SelectOptionData } from '@arco-design/web-vue';
import { sendDataset } from "@/api/dataset";
import { getToken } from '@/utils/auth';

const generateUploadModel = () => {
    return {
        datasetName: '',
        datasetIntroduction: '',
        datasetApplication: '',
        datasetTags: [] as string[],
        annex: [] as FileItem[],
        files: [] as File[],
    }
}
const UploadModel = ref(generateUploadModel());
const inputRef = ref(null);
const showTagInput = ref(false);
const inputTag = ref('');
const handleEdit = () => {
    showTagInput.value = true;

    nextTick(() => {
        if (inputRef.value) {
            inputRef.value.focus();
        }
    });
};

const uploadChange = async (fileItem: FileItem) => {
    UploadModel.value.annex.push(fileItem);
    if(fileItem.file)
    {
        UploadModel.value.files.push(fileItem.file);
    }
  };


const handleAdd = () => {
    if (inputTag.value) {
        UploadModel.value.datasetTags.push(inputTag.value);
        inputTag.value = '';
    }
    showTagInput.value = false;
};

const handleRemove = (key: string) => {
    UploadModel.value.datasetTags = UploadModel.value.datasetTags.filter((tagTemp) => tagTemp !== key);
};

const { t } = useI18n();
const handleUpload = async () => {
    await sendDataset(getToken()!, UploadModel.value);
    UploadModel.value = generateUploadModel();
}
const handleCancel = async () => {
    UploadModel.value = generateUploadModel();
}
const ApplicationOptions = computed<SelectOptionData[]>(() => [
    {
        label: t('dataset.upload.application.one'),
        value: '听',
    },
    {
        label: t('dataset.upload.application.two'),
        value: '说',
    },
    {
        label: t('dataset.upload.application.three'),
        value: '其他',
    },
]);
</script>
<style scoped lang="less"></style>