<template>
    <a-modal
        :title="null"
        :closable=false>
        <template #title>
            <div style="display: flex; align-items: center;">
                <icon-upload style="margin-right: 5px;"></icon-upload>
                {{ $t('dataset.upload.title') }}
            </div>
        </template>
        <a-form style="padding-right: 10px;">
            <a-form-item
                :label="$t('dataset.upload.introduction.title')">
                <a-textarea
                    :placeholder="$t('dataset.upload.introduction.title.default')"
                    style="height: 100px;">

                </a-textarea>
            </a-form-item>
            <a-form-item
                :label="$t('dataset.upload.publisher.title')">
                <a-input
                    :placeholder="$t('dataset.upload.publisher.title.default')">

                </a-input>
            </a-form-item>
            <a-form-item
                :label="$t('dataset.upload.application.title')">
                <a-input
                    :placeholder="$t('dataset.upload.application.title.default')">

                </a-input>
            </a-form-item>
        </a-form>
    </a-modal>
</template>

<script lang="ts" setup>
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>
<style scoped lang="less">

</style>