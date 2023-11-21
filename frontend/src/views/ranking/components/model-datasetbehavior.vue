<template>
    <div class="dataset-behaviour">
        <a-card class="general-card">
            <a-row>
                <a-col :flex="1">
                    <a-form
                        :model="SearchFormModel"
                        label-align="left"
                    >
                        <a-row :gutter="16">
                            <a-col :span="8">
                                <a-form-item
                                    field="number"
                                    :label="$t('ranking.behaviour.dataset.num')"
                                    :rules="numRules"
                                    :label-col-props="{ span: 7 }"
                                    :wrapper-col-props="{ span: 17 }"
                                >
                                    <a-input
                                        v-model="SearchFormModel.num"
                                        :placeholder="$t('ranking.behaviour.dataset.num.default')"
                                    ></a-input>
                                </a-form-item>
                            </a-col>
                            <a-col :span="9">
                                <a-form-item
                                    field="name"
                                    :label="$t('ranking.behaviour.dataset.name')"
                                    :label-col-props="{ span: 7 }"
                                    :wrapper-col-props="{ span: 17 }"
                                >
                                    <a-input
                                        v-model="SearchFormModel.name"
                                        :placeholder="$t('ranking.behaviour.dataset.name.default')"
                                    ></a-input>
                                </a-form-item>
                            </a-col>
                            <a-col :span="7">
                                <a-form-item
                                    field="contentType"
                                    :label="$t('ranking.behaviour.dataset.contenttype')"
                                    :label-col-props="{ span: 7 }"
                                    :wrapper-col-props="{ span: 17 }"
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
                                    field="contentSize"
                                    :label="$t('ranking.behaviour.dataset.contentsize')"
                                    :rules="sizeRules"
                                    :label-col-props="{ span: 7 }"
                                    :wrapper-col-props="{ span: 17 }"
                                >   
                                    <a-input
                                        v-model="SearchFormModel.contentSize_min"
                                        :placeholder="$t('ranking.behaviour.dataset.size.min.default')"
                                    ></a-input>
                                    <span> ~ </span>
                                    <a-input
                                        v-model="SearchFormModel.contentSize_max"
                                        :placeholder="$t('ranking.behaviour.dataset.size.max.default')"
                                    ></a-input>
                                </a-form-item>
                            </a-col>
                            <a-col :span="9">
                                <a-form-item
                                    field="createdTime"
                                    :label="$t('ranking.behaviour.dataset.createdTime')"
                                    :label-col-props="{ span: 7 }"
                                    :wrapper-col-props="{ span: 17 }"
                                >
                                    <a-range-picker
                                        v-model="SearchFormModel.createdTime"
                                        style="width: 100%"
                                    ></a-range-picker>
                                </a-form-item>
                            </a-col>
                            <a-col :span="7">
                                <a-form-item
                                    field="score"
                                    :label="$t('ranking.behaviour.dataset.score')"
                                    :rules="scoreRules"
                                    :label-col-props="{ span: 7 }"
                                    :wrapper-col-props="{ span: 17 }"
                                >   
                                    <a-input
                                        v-model="SearchFormModel.score_min"
                                        :placeholder="$t('ranking.behaviour.dataset.score_min.default')"
                                    ></a-input>
                                    <span> ~ </span>
                                    <a-input
                                        v-model="SearchFormModel.score_max"
                                        :placeholder="$t('ranking.behaviour.dataset.score_max.default')"
                                    ></a-input>
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
                <template #contentType="{ record }">
                    {{ record.contentType }}
                </template>
                <template #contentSize="{ record }">
                    {{ record.contentSize }}
                </template>
                <template #createdTime="{ record }">
                    {{ record.createdTime }}
                </template>
                <template #score="{ record }">
                    {{ record.score }}
                </template>
            </a-table>
        </a-card>
    </div>
</template>

<script lang="ts" setup>
    import { computed, ref, reactive, watch, nextTick,getCurrentInstance} from 'vue';
    import { IconSearch } from '@arco-design/web-vue/es/icon';
    import useLoading from '@/hooks/loading';
    import { useI18n } from 'vue-i18n';
    import { Pagination } from '@/types/global';
    import { queryDatasetList, DatasetRecord, DatasetParams } from '@/api/list';
    import type {TableColumnData } from '@arco-design/web-vue/es/table/interface';
    import { DatasetRankingData, DatasetSelectParams } from "@/api/model-list";
    import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
    import cloneDeep from 'lodash/cloneDeep';

    type Column = TableColumnData & { checked?: true };
    const { t } = useI18n();
    const { proxy } = getCurrentInstance();
    const {loading, setLoading} = useLoading(false);
    const showColumns = ref<Column[]>([]);
    const renderData = ref<DatasetRankingData[]>([{num: 1, name: 'BookCorpus', contentType: "主观题", contentSize: 283, createdTime: "2021-02-28", score: 98},
                                                {num: 2, name: 'LVIS', contentType: "混合题", contentSize: 253, createdTime: "2022-10-11", score: 98},
                                                {num: 3, name: 'Crowd Segmentation', contentType: "客观题", contentSize: 895, createdTime: "2022-09-11", score: 96},
                                                {num: 4, name: 'MNIST', contentType: "混合题", contentSize: 284, createdTime: "2019-05-21", score: 100},
                                                {num: 5, name: 'Kaggle', contentType: "客观题", contentSize: 442, createdTime: "2023-11-19", score: 98},
                                                {num: 6, name: 'LVIS-II', contentType: "主观题", contentSize: 666, createdTime: "2019-12-25", score: 60},
                                                {num: 7, name: 'LVIS-III', contentType: "主观题", contentSize: 359, createdTime: "2022-01-01", score: 99},
                                                
                                            ]);
    const originData = ref<DatasetRankingData[]>([{num: 1, name: 'BookCorpus', contentType: "主观题", contentSize: 283, createdTime: "2021-02-28", score: 98},
                                                {num: 2, name: 'LVIS', contentType: "混合题", contentSize: 253, createdTime: "2022-10-11", score: 98},
                                                {num: 3, name: 'Crowd Segmentation', contentType: "客观题", contentSize: 895, createdTime: "2022-09-11", score: 96},
                                                {num: 4, name: 'MNIST', contentType: "混合题", contentSize: 284, createdTime: "2019-05-21", score: 100},
                                                {num: 5, name: 'Kaggle', contentType: "客观题", contentSize: 442, createdTime: "2023-11-19", score: 98},
                                                {num: 6, name: 'LVIS-II', contentType: "主观题", contentSize: 666, createdTime: "2019-12-25", score: 60},
                                                {num: 7, name: 'LVIS-III', contentType: "主观题", contentSize: 359, createdTime: "2022-01-01", score: 99},
                                            ]);
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
            num: '',
            name: '',
            contentType: '',
            contentSize_min: '',
            contentSize_max: '',
            createdTime: ['',''],
            score_min: '',
            score_max: '',
        };
    };

    const SearchFormModel= ref(generateSearchFormModel());
    const contentTypeOptions = computed<SelectOptionData[]>(() => [
        {
            label: t('ranking.behaviour.contentType.mix'),
            value: '混合题',
        },
        {
            label: t('ranking.behaviour.contentType.subjective'),
            value: '主观题',
        },
        {
            label: t('ranking.behaviour.contentType.objective'),
            value: '客观题',
        },
    ]);

    const reset = () => {
        SearchFormModel.value = generateSearchFormModel();
    };
    
    const numRules=[
        {
            required: false,
            validator: (value: string, callback: (error?: string) => void) => {
                return new Promise<void>((resolve) => {
                    window.setTimeout(() => {
                        value = SearchFormModel.value.num;
                        if(value !== '')
                        {
                            if(!/^\d+$/.test(value))
                            {
                                callback(proxy.$t('ranking.behaviour.dataset.num.errormsg'));
                            }
                        }
                        resolve();
                    }, 1000);
                });
            },
            trigger: ['change', 'blur'],
        },
    ];
    const sizeRules=[
        {
            required: false,
            validator: (value: string, callback: (error?: string) => void) => {
                return new Promise<void>((resolve) => {
                    window.setTimeout(() => {
                        value = SearchFormModel.value.contentSize_min;
                        if(value !== '')
                        {
                            if(!/^\d+$/.test(value))
                            {
                                callback(proxy.$t('ranking.behaviour.dataset.size.errormsg'));
                            }
                        }
                        resolve();
                    }, 1000);
                });
            },
            trigger: ['blur', 'change'],
        },
        {
            required: false,
            validator: (value: string, callback: (error?: string) => void) => {
                return new Promise<void>((resolve) => {
                    window.setTimeout(() => {
                        value = SearchFormModel.value.contentSize_max;
                        if(value !== '')
                        {
                            if(!/^\d+$/.test(value))
                            {
                                callback(proxy.$t('ranking.behaviour.dataset.size.errormsg'));
                            }
                        }
                        resolve();
                    }, 1000);
                });
            },
            trigger: ['blur', 'change'],
        },
    ];

    const scoreRules=[
        {
            required: false,
            validator: (value: string, callback: (error?: string) => void) => {
                return new Promise<void>((resolve) => {
                    window.setTimeout(() => {
                        value = SearchFormModel.value.score_min;
                        if(value !== '')
                        {
                            const scoreNumMin = parseInt(value, 10);
                            if(!/^\d+$/.test(value))
                            {
                                callback(proxy.$t('ranking.behaviour.dataset.size.errormsg'));
                            }
                            else if(scoreNumMin < 0 || scoreNumMin > 100)
                            {
                                callback(proxy.$t('ranking.behaviour.dataset.score.errormsg'));
                            }
                        }
                        resolve();
                    }, 1000);
                });
            },
            trigger: ['blur', 'change'],
        },
        {
            required: false,
            validator: (value: string, callback: (error?: string) => void) => {
                return new Promise<void>((resolve) => {
                    window.setTimeout(() => {
                        value = SearchFormModel.value.score_max;
                        if(value !== '')
                        {
                            const scoreNum = parseInt(value, 10);
                            if(!/^\d+$/.test(value))
                            {
                                callback(proxy.$t('ranking.behaviour.dataset.size.errormsg'));
                            }
                            else if(scoreNum < 0 || scoreNum > 100)
                            {
                                callback(proxy.$t('ranking.behaviour.dataset.score.errormsg'));
                            }
                        }
                        resolve();
                    }, 1000);
                });
            },
            trigger: ['blur', 'change'],
        },
    ];
    
    const columns = computed<TableColumnData[]>(() => [
        {
            title: t('ranking.behaviour.table.num'),
            dataIndex: 'num',
            slotName: 'num',
            align: "center",
            sortable: {
                sortDirections: ['ascend', 'descend']
            },
        },
        {
            title: t('ranking.behaviour.table.name'),
            dataIndex: 'name',
            slotName: 'name',
            align: "center",
            sortable: {
                sortDirections: ['ascend', 'descend']
            },
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
            sortable: {
                sortDirections: ['ascend', 'descend']
            },
        },
        {
            title: t('ranking.behaviour.table.createdTime'),
            dataIndex: 'createdTime',
            slotName: 'createdTime',
            align: "center",
            sortable: {
                sortDirections: ['ascend', 'descend']
            },
        },
        {
            title: t('ranking.behaviour.table.score'),
            dataIndex: 'score',
            slotName: 'score',
            align: "center",
            sortable: {
                sortDirections: ['ascend', 'descend']
            },
        },
    ]);
    const fetchData = async (
        params: DatasetParams = { current: 1, pageSize: 20 }
    ) => {
    setLoading(true);
    try {
        const { data } = await queryDatasetList(params);
        // renderData.value = data.list;
        const filteredData = computed(() => {
            let result = originData.value;
            if(SearchFormModel.value.num !== '')
            {
                result=result.filter(item => item.num.toString() === SearchFormModel.value.num);
            }
            if(SearchFormModel.value.name !== '')
            {
                result=result.filter(item => item.name.includes(SearchFormModel.value.name));
            }
            if(SearchFormModel.value.contentType !== '')
            {
                result=result.filter(item => item.contentType === SearchFormModel.value.contentType);
            }
            if(SearchFormModel.value.contentSize_min !== '')
            {
                result=result.filter(item => item.contentSize >= Number(SearchFormModel.value.contentSize_min));
            }
            if(SearchFormModel.value.contentSize_max !== '')
            {
                result=result.filter(item => item.contentSize <= Number(SearchFormModel.value.contentSize_max));
            }
            if(SearchFormModel.value.score_min !== '')
            {
                result=result.filter(item => item.score >= Number(SearchFormModel.value.score_min));
            }
            if(SearchFormModel.value.score_max !== '')
            {
                result=result.filter(item => item.score <= Number(SearchFormModel.value.score_max));
            }
            if(SearchFormModel.value.createdTime[0] === '' || SearchFormModel.value.createdTime[1] === '')
            {
                return result;
            }
            if(SearchFormModel.value.createdTime){
                result=result.filter(item => {
                    const itemCreatedTime = new Date(item.createdTime);
                    const dateMin = new Date(SearchFormModel.value.createdTime[0]);
                    const dateMax = new Date(SearchFormModel.value.createdTime[1]);
                    const meetsMinCondition = dateMin ? itemCreatedTime >= dateMin : true;
                    const meetsMaxCondition = dateMax ? itemCreatedTime <= dateMax : true;

                    return meetsMinCondition && meetsMaxCondition;
                });
            }
            return result;
        });
        renderData.value = filteredData.value;
        pagination.current = params.current;
        pagination.total = data.total;
    } catch (err) {
        // you can report use errorHandler or other
    } finally {
        setLoading(false);
    }
    };
    // const filteredData = computed(() => {
        // 根据输入框的内容进行筛选
    // return renderData.value.filter(item => item.num.toString() === SearchFormModel.value.num);
    // });
    const search = () => {
        fetchData({
        ...basePagination,
        ...SearchFormModel.value,
        } as unknown as DatasetParams);
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

.custom-filter {
  padding: 20px;
  background: var(--color-bg-5);
  border: 1px solid var(--color-neutral-3);
  border-radius: var(--border-radius-medium);
  box-shadow: 0 2px 5px rgb(0 0 0 / 10%);
}
.general-card {
    padding: 10px;
    
}
.custom-filter-footer {
  display: flex;
  justify-content: space-between;
}
</style>
