<template>
  <div class="container">
    <Breadcrumb :items="['menu.ranking', 'menu.ranking.profile']" />
    <a-card class="general-card" :title="$t('menu.list.searchTable')">
      <a-row>
        <a-col :flex="1">
          <a-form
              :model="formModel"
              :label-col-props="{ span: 6 }"
              :wrapper-col-props="{ span: 18 }"
              label-align="left"
          >
            <a-row :gutter="16">
              <a-col :span="8">
                <a-form-item
                    field="number"
                    :label="$t('searchTable.form.number')"
                >
                  <a-input
                      v-model="formModel.number"
                      :placeholder="$t('searchTable.form.number.placeholder')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item field="name" :label="$t('searchTable.form.name')">
                  <a-input
                      v-model="formModel.name"
                      :placeholder="$t('searchTable.form.name.placeholder')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                    field="contentType"
                    :label="$t('searchTable.form.contentType')"
                >
                  <a-select
                      v-model="formModel.contentType"
                      :options="contentTypeOptions"
                      :placeholder="$t('searchTable.form.selectDefault')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                    field="filterType"
                    :label="$t('searchTable.form.filterType')"
                >
                  <a-select
                      v-model="formModel.filterType"
                      :options="filterTypeOptions"
                      :placeholder="$t('searchTable.form.selectDefault')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                    field="createdTime"
                    :label="$t('searchTable.form.createdTime')"
                >
                  <a-range-picker
                      v-model="formModel.createdTime"
                      style="width: 100%"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                    field="status"
                    :label="$t('searchTable.form.status')"
                >
                  <a-select
                      v-model="formModel.status"
                      :options="statusOptions"
                      :placeholder="$t('searchTable.form.selectDefault')"
                  />
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </a-col>
        <a-divider style="height: 84px" direction="vertical" />
        <a-col :flex="'86px'" style="text-align: right">
          <a-space direction="vertical" :size="18">
            <a-button type="primary" @click="search">
              <template #icon>
                <icon-search />
              </template>
              {{ $t('searchTable.form.search') }}
            </a-button>
            <a-button @click="reset">
              <template #icon>
                <icon-refresh />
              </template>
              {{ $t('searchTable.form.reset') }}
            </a-button>
          </a-space>
        </a-col>
      </a-row>
      <a-divider style="margin-top: 0" />
      <a-row style="margin-bottom: 16px">
        <a-col :span="12">
          <a-space>
            <a-button type="primary">
              <template #icon>
                <icon-plus />
              </template>
              {{ $t('searchTable.operation.create') }}
            </a-button>
          </a-space>
        </a-col>
        <a-col
            :span="12"
            style="display: flex; align-items: center; justify-content: end"
        >
          <a-button>
            <template #icon>
              <icon-download />
            </template>
            {{ $t('searchTable.operation.download') }}
          </a-button>
          <a-tooltip :content="$t('searchTable.actions.refresh')">
            <div class="action-icon"
            ><icon-refresh size="18"
            /></div>
          </a-tooltip>
          <a-dropdown @select="handleSelectDensity">
            <a-tooltip :content="$t('searchTable.actions.density')">
              <div class="action-icon"><icon-line-height size="18" /></div>
            </a-tooltip>
            <template #content>
              <a-doption
                  v-for="item in densityList"
                  :key="item.value"
                  :value="item.value"
                  :class="{ active: item.value === size }"
              >
                <span>{{ item.name }}</span>
              </a-doption>
            </template>
          </a-dropdown>
        </a-col>
      </a-row>
      <a-table
          row-key="id"
          :loading="loading"
          :pagination="pagination"
          :columns="columns"
          :data="renderData"
          :bordered="false"
          :size="size"
      >
        <template #ranking="{ record }">
          {{ record.ranking }}
        </template>
        <template #name="{ record }">
          {{ record.name }}
        </template>
        <template #mmluScore="{ record }">
          {{ record.mmluScore }}
        </template>
        <template #datasetScore="{ record }">
          {{ record.datasetScore }}
        </template>
        <template #eloScore="{ record }">
          {{ record.eloScore }}
        </template>
        <template #details="{ record }">
          <a-button type="text" size="small" @click="handleClick(record)">
            {{ $t('ranking.view.btn') }}
          </a-button>
        </template>
        <template #license="{ record }">
          {{ record.license }}
        </template>
      </a-table>
    </a-card>
  </div>
  <a-drawer :width="1000"
            :visible="visible"
            :footer="false"
            @cancel="handleCancel"
            @open="setDrawerStyle"
            unmountOnClose>
    <template #title>
      <header class="drawer-model-title">
        <div class="drawer-model-title-text">
          {{ currentLLM.name }}
        </div>
        <a-button
            class="llm-details-subscribe-btn"
            type="primary"
            size="large"
        >
          <template #icon>
            <icon-star :size="30"/>
          </template>
          {{ $t('rankings.llm.details.subscribe.btn') }}
        </a-button>
      </header>
    </template>
    <div>
      <a-tabs size="large">
        <a-tab-pane key="1" title="详细资料">
          <ModelProfile />
        </a-tab-pane>
        <a-tab-pane key="2" title="数据集表现">
          <DatasetProfile />
        </a-tab-pane>
        <a-tab-pane key="3" title="对抗记录">
        </a-tab-pane>
        <a-tab-pane key="4" title="讨论区">
          <ModelDiscussionArea :comment-details="commentDetails" :model-id="ModelID" @change-comment="handleChangeComment" />
        </a-tab-pane>
      </a-tabs>
    </div>
  </a-drawer>
</template>

<script lang="ts" setup>
import {computed, ref, reactive, watch, nextTick, onMounted} from 'vue';
import axios from "axios";
import apiCat from "@/api/main";
import {getToken} from "@/utils/auth";
  import { useI18n } from 'vue-i18n';
  import useLoading from '@/hooks/loading';
  import { queryPolicyList, PolicyRecord, PolicyParams } from '@/api/list';
  import { LLMRankingData } from "@/api/model-list";
  import { Pagination } from '@/types/global';
  import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import Sortable from 'sortablejs';
  import cloneDeep from 'lodash/cloneDeep';
import MyComment, {getComment, updateComment} from "@/api/comment";
  import ModelDiscussionArea from "./components/model-discussion-area.vue";
  import ModelProfile from './components/model-profile.vue';
  import DatasetProfile from './components/model-datasetbehavior.vue'
  
  type SizeProps = 'mini' | 'small' | 'medium' | 'large';
  type Column = TableColumnData & { checked?: true };

  const visible = ref(false);
  const generateFormModel = () => {
    return {
      number: '',
      name: '',
      contentType: '',
      filterType: '',
      createdTime: [],
      status: '',
    };
  };
  const { loading, setLoading } = useLoading(false);
  const { t } = useI18n();
  const renderData = ref<LLMRankingData[]>([{name: 'GPT-4', ranking: 1, mmluScore: 86.4, datasetScore: 8.99, eloScore: 1181, license: 'Proprietary'}]);
  const formModel = ref(generateFormModel());
  const cloneColumns = ref<Column[]>([]);
  const showColumns = ref<Column[]>([]);
  const currentLLM = ref<LLMRankingData>();

  const size = ref<SizeProps>('medium');

  const commentDetails = ref([] as MyComment[]);
  const ModelID = '1';
  const jwt = getToken();

  const handleClick = (data: LLMRankingData) => {
    currentLLM.value = data;
    visible.value = true;
  };

  const handleCancel = () => {
    visible.value = false;
  }

  const basePagination: Pagination = {
    current: 1,
    pageSize: 20,
  };
  const pagination = reactive({
    ...basePagination,
  });
  const densityList = computed(() => [
    {
      name: t('searchTable.size.mini'),
      value: 'mini',
    },
    {
      name: t('searchTable.size.small'),
      value: 'small',
    },
    {
      name: t('searchTable.size.medium'),
      value: 'medium',
    },
    {
      name: t('searchTable.size.large'),
      value: 'large',
    },
  ]);
  const columns = computed<TableColumnData[]>(() => [
    {
      title: t('rankings.llm.data.ranking'),
      dataIndex: 'ranking',
      slotName: 'ranking',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('rankings.llm.data.name'),
      dataIndex: 'name',
      slotName: 'name',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('rankings.llm.data.mmluScore'),
      dataIndex: 'mmluScore',
      slotName: 'mmluScore',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('rankings.llm.data.datasetScore'),
      dataIndex: 'datasetScore',
      slotName: 'dataScore',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('rankings.llm.data.eloScore'),
      dataIndex: 'eloScore',
      slotName: 'eloScore',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('rankings.llm.data.details'),
      dataIndex: 'details',
      slotName: 'details',
      align: "center",
    },
    {
      title: t('rankings.llm.data.license'),
      dataIndex: 'license',
      slotName: 'license',
      align: "center",
    },
  ]);
  const contentTypeOptions = computed<SelectOptionData[]>(() => [
    {
      label: t('searchTable.form.contentType.img'),
      value: 'img',
    },
    {
      label: t('searchTable.form.contentType.horizontalVideo'),
      value: 'horizontalVideo',
    },
    {
      label: t('searchTable.form.contentType.verticalVideo'),
      value: 'verticalVideo',
    },
  ]);
  const filterTypeOptions = computed<SelectOptionData[]>(() => [
    {
      label: t('searchTable.form.filterType.artificial'),
      value: 'artificial',
    },
    {
      label: t('searchTable.form.filterType.rules'),
      value: 'rules',
    },
  ]);
  const statusOptions = computed<SelectOptionData[]>(() => [
    {
      label: t('searchTable.form.status.online'),
      value: 'online',
    },
    {
      label: t('searchTable.form.status.offline'),
      value: 'offline',
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
      ...formModel.value,
    } as unknown as PolicyParams);
  };
  const onPageChange = (current: number) => {
    fetchData({ ...basePagination, current });
  };

  const reset = () => {
    formModel.value = generateFormModel();
  };

  const handleSelectDensity = (
      val: string | number | Record<string, any> | undefined,
      e: Event
  ) => {
    size.value = val as SizeProps;
  };


  const exchangeArray = <T extends Array<any>>(
      array: T,
      beforeIdx: number,
      newIdx: number,
      isDeep = false
  ): T => {
    const newArray = isDeep ? cloneDeep(array) : array;
    if (beforeIdx > -1 && newIdx > -1) {
      // 先替换后面的，然后拿到替换的结果替换前面的
      newArray.splice(
          beforeIdx,
          1,
          newArray.splice(newIdx, 1, newArray[beforeIdx]).pop()
      );
    }
    return newArray;
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

  const setDrawerStyle = () => {
    const drawerHeader = document.querySelector('.arco-drawer-header');
    if (drawerHeader) {
      drawerHeader.style.height = '220px';
      drawerHeader.style.border = '0';
    }

    const drawerTitle = document.querySelector('.arco-drawer-title');
    if (drawerTitle) {
      drawerTitle.style.paddingLeft = '80px';
    }

    const drawerCloseBtn = document.querySelector('.arco-drawer-close-btn');
    if(drawerCloseBtn){
      drawerCloseBtn.style. visibility = 'hidden';
    }

    const starBtn = document.querySelector('.arco-icon-star');
    if(starBtn){
      starBtn.style.display = 'flex';
      starBtn.style.justifyContent = 'center';
      starBtn.style.alignItems = 'center';
    }

    const starFillBtn = document.querySelector('.arco-icon-star-fill');
    if(starFillBtn){
      starFillBtn.style.display = 'flex';
      starFillBtn.style.justifyContent = 'center';
      starFillBtn.style.alignItems = 'center';
    }

    const tabs = document.querySelectorAll('.arco-tabs-tab')
    if(tabs){
      for(let i = 0; i < tabs.length; i += 1){
        tabs[i].style.margin = '0 25px';
        tabs[i].style.fontSize = '15px';
      }
    }

    const firstTab = document.querySelector('.arco-tabs-tab:first-of-type')
    if(firstTab){
      firstTab.style.margin = '0 25px 0 60px';
    }
  };

  const handleChangeComment = async (index: number, content: MyComment) => {
    await updateComment(ModelID, content, jwt!);
    if (index === -1) {
      commentDetails.value.push(content);
    } else {
      commentDetails.value[index].children.push(content);
    }
  };

onMounted(async () => {
  await getComment(ModelID, commentDetails, jwt!);
});
</script>

<script lang="ts">
  export default {
    name: 'SearchTable',
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }

  .drawer-model-title-text{
    font-size: 60px;
  }

  :deep(.arco-table-th) {
    &:last-child {
      .arco-table-th-item-title {
        margin-left: 16px;
      }
    }
  }
  .action-icon {
    margin-left: 12px;
    cursor: pointer;
  }
  .active {
    color: #0960bd;
    background-color: #e3f4fc;
  }
  .setting {
    display: flex;
    align-items: center;
    width: 200px;
    .title {
      margin-left: 12px;
      cursor: pointer;
    }
  }

  .drawer-model-title{
    display: flex;
    flow: right;
    justify-content: center;
    align-items: center;
  }


  .llm-details-subscribe-btn{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: 30px;
    padding: 5px 20px;
    font-size: 18px;
  }
</style>

