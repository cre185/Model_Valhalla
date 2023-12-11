<template>
    <a-modal
        :title="null"
        @ok="handleUpload"
        :ok-text="$t('dataset.upload.button.title')"
        @cancel="handleCancel"
        :closable=false>
        <template #title>
            <div style="display: flex; align-items: center;">
                <icon-upload style="margin-right: 5px;"></icon-upload>
                {{ $t('dataset.upload.title') }}
            </div>
        </template>
        <a-form style="padding-right: 10px;">
            <a-form-item
                :label="$t('dataset.upload.name.title')"
                v-model="UploadModel.datasetName">
                <a-input
                    :placeholder="$t('dataset.upload.name.title.default')">

                </a-input>

            </a-form-item>
            <a-form-item
                :label="$t('dataset.upload.main.title')"
                v-model="UploadModel.datasetMain">
                <a-input
                    :placeholder="$t('dataset.upload.main.title.default')">

                </a-input>

            </a-form-item>
            <a-form-item
                :label="$t('dataset.upload.introduction.title')"
                v-model="UploadModel.datasetIntroduction">
                <a-textarea
                    :placeholder="$t('dataset.upload.introduction.title.default')"
                    style="height: 100px;">

                </a-textarea>
            </a-form-item>
            <a-form-item
                :label="$t('dataset.upload.publisher.title')"
                v-model="UploadModel.datasetPublisher">
                <a-input
                    :placeholder="$t('dataset.upload.publisher.title.default')">

                </a-input>
            </a-form-item>
            <a-form-item
                :label="$t('dataset.upload.application.title')"
                v-model="UploadModel.datasetApplication">
                <a-input
                    :placeholder="$t('dataset.upload.application.title.default')">

                </a-input>
            </a-form-item>
            <a-form-item
                :label="$t('dataset.upload.file.title')"
                v-model="UploadModel.annex">
                <a-upload>

                </a-upload>
            </a-form-item>
        </a-form>
    </a-modal>
</template>

<script lang="ts" setup>
import { useI18n } from 'vue-i18n';
import {ref} from 'vue';

const generateUploadModel = () => {
    return {
        datasetName: '',
        datasetMain: '',
        datasetIntroduction: '',
        datasetApplication: '',
        datasetPublisher: '',
        annex: [] as File[],
    }
}
const UploadModel = ref(generateUploadModel());
const { t } = useI18n();
const handleUpload = async () => {
    UploadModel.value = generateUploadModel();
}
const handleCancel = async () => {
    UploadModel.value = generateUploadModel();
}
</script>
<style scoped lang="less">

</style>