<template>
    <div class="dataset-behaviour">
        <a-card class="general-card" :title="$t('menu.list.searchTable')">
            <a-row>
                <a-col :flex="1">
                    <a-form
                        :model="SearchFormModel"
                        :label-col-props="{ span: 6}"
                        :wrapper-col-props="{ span: 18}"
                        label-align="left"
                    >
                        <a-row :gutter="16">
                            <a-col :span="8">
                                <a-form-item
                                    field="number"
                                    :label="$t('ranking.behaviour.dataset.num')"
                                >
                                    <a-input
                                        v-model="SearchFormModel.number"
                                        :placeholder="$t('ranking.behaviour.dataset.num.default')"
                                    ></a-input>
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item
                                    field="name"
                                    :label="$t('ranking.behaviour.dataset.name')"
                                >
                                    <a-input
                                        v-model="SearchFormModel.name"
                                        :placeholder="$t('ranking.behaviour.dataset.name.default')"
                                    ></a-input>
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item
                                    field="contentType"
                                    :label="$t('ranking.behaviour.dataset.contenttype')"
                                >
                                    <a-select
                                        v-model="SearchFormModel.contentType"
                                        :options="contentTypeOptions"
                                        :placeholder="$t('ranking.behaviour.dataset.contenttype.default')"
                                    ></a-select>
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item
                                    field="labelSearch"
                                    :label="$t('ranking.behaviour.dataset.labelsearch')"
                                >
                                    <a-select
                                        v-model="SearchFormModel.labelSearch"
                                        :options="labelSearchOptions"
                                        :placeholder="$t('ranking.behaviour.dataset.labelsearch.default')"
                                    ></a-select>
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item
                                    field="contentSize"
                                    :label="$t('ranking.behaviour.dataset.contentsize')"
                                >   
                                    <a-input
                                        v-model="SearchFormModel.contentSize"
                                        :placeholder="$t('ranking.behaviour.dataset.name.default')"
                                    ></a-input>
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item
                                    field="createdTime"
                                    :label="$t('ranking.behaviour.dataset.createdTime')"
                                >
                                    <a-range-picker
                                        v-model="SearchFormModel.createdTime"
                                        style="width: 100%"
                                    ></a-range-picker>
                                </a-form-item>
                            </a-col>
                        </a-row>
                    </a-form>
                </a-col>
                <a-divider style="height: 84px" direction="vertical"></a-divider>
                <a-col :flex="'86px'" style="text-align: right">
                    <a-space direction="vertical" :size="18">
                        <a-button type="primary" @click="search">
                            <template #icon>
                                <icon-search></icon-search>
                            </template>
                            {{ $t('ranking.behaviour.button.filter') }}
                        </a-button>
                        <a-button @click="reset">
                            <template #icon>
                                <icon-refresh></icon-refresh>
                            </template>
                            {{ $t('ranking.behaviour.button.reset') }}
                        </a-button>
                    </a-space>
                </a-col>
            </a-row>
            <a-divider style="margin-top: 0"></a-divider>
            <a-table
                row-key="ID"
                :loading="loading"
                :pagination="pagination"
                :columns="columns"
                :data="renderData"
                :bordered="false"
            >
                <template #num="{ record }">
                    {{ record.num }}
                </template>
                <template #name="{ record }">
                    {{ record.name }}
                </template>
                <template #type="{ record }">
                    {{ record.type }}
                </template>
                <template #size="{ record }">
                    {{ record.size }}
                </template>
                <template #time="{ record }">
                    {{ record.time }}
                </template>
                <template #score="{ record }">
                    {{ record.score }}
                </template>
            </a-table>
        </a-card>
    </div>
</template>

<script lang="ts" setup>
    import { computed, ref, reactive, watch, nextTick } from 'vue';
    import useLoading from '@/hooks/loading';
    import { useI18n } from 'vue-i18n';
    import { Pagination } from '@/types/global';
    import { queryPolicyList, PolicyRecord, PolicyParams } from '@/api/list';
    import type {TableColumnData } from '@arco-design/web-vue/es/table/interface';
    import { DatasetRankingData, DatasetSelectParams } from "@/api/model-list";
    import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
    import cloneDeep from 'lodash/cloneDeep';

    type Column = TableColumnData & { checked?: true };
    const { t } = useI18n();
    const {loading, setLoading} = useLoading(false);
    const showColumns = ref<Column[]>([]);
    const renderData = ref<DatasetRankingData[]>([{num: 1, name: 'LVIS', contentType: "书籍", contentSize: 86, createdTime: "2022-11-11", score: 100}]);
    const cloneColumns = ref<Column[]>([]);
    const basePagination: Pagination = {
        current: 1,
        pageSize: 20,
    };
    const pagination = reactive({
        ...basePagination,
    });

    const generateSearchFormModel = () => {
        return {
            number: '',
            name: '',
            contentType: '',
            labelSearch: '',
            contentSize: '',
            createdTime: [],
        };
    };

    const SearchFormModel= ref(generateSearchFormModel());
    const contentTypeOptions = computed<SelectOptionData[]>(() => [
        {
            label: t('ranking.behaviour.contentType.book'),
            value: 'book',
        },
        {
            label: t('ranking.behaviour.contentType.imageCut'),
            value: 'imageCut',
        },
        {
            label: t('ranking.behaviour.contentType.imageClassify'),
            value: 'imageClassify',
        },
    ]);

    const labelSearchOptions = computed<SelectOptionData[]>(() => [
        {
            label: t('ranking.behaviour.labelSearch.subjective'),
            value: 'subjective',
        },
        {
            label: t('ranking.behaviour.labelSearch.objective'),
            value: 'objective',
        },
    ]);

    const reset = () => {
        SearchFormModel.value = generateSearchFormModel();
    };

    const columns = computed<TableColumnData[]>(() => [
        {
            title: t('ranking.behaviour.table.ID'),
            dataIndex: 'ID',
            slotName: 'ID',
            align: "center",
        },
        {
            title: t('ranking.behaviour.table.name'),
            dataIndex: 'name',
            slotName: 'name',
            align: "center",
        },
        {
            title: t('ranking.behaviour.table.contentType'),
            dataIndex: 'contentType',
            slotName: 'contentType',
            align: "center",
        },
        {
            title: t('ranking.behaviour.table.contentSize'),
            dataIndex: 'contentSize',
            slotName: 'contentSize',
            align: "center",
        },
        {
            title: t('ranking.behaviour.table.createdTime'),
            dataIndex: 'createdTime',
            slotName: 'createdTime',
            align: "center",
        },
        {
            title: t('ranking.behaviour.table.score'),
            dataIndex: 'score',
            slotName: 'score',
            align: "center",
        },
    ]);
    const fetchData = async (
        params: PolicyParams = { current: 1, pageSize: 20 }
    ) => {
    setLoading(true);
    try {
        const { data } = await queryPolicyList(params);
        renderData.value = data.list;
        pagination.current = params.current;
        pagination.total = data.total;
    } catch (err) {
        // you can report use errorHandler or other
    } finally {
        setLoading(false);
    }
    };

    const search = () => {
        fetchData({
        ...basePagination,
        ...SearchFormModel.value,
        } as unknown as PolicyParams);
    };
    watch(
        () => columns.value,
        (val) => {
        cloneColumns.value = cloneDeep(val);
        cloneColumns.value.forEach((item, index) => {
            item.checked = true;
        });
        showColumns.value = cloneDeep(cloneColumns.value);
        },
        { deep: true, immediate: true }
    );
</script>
<style scoped lang="less">

</style>
