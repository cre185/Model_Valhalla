<template>
  <div>
    <div class="container">
      <Breadcrumb :items="['menu.ranking', 'menu.ranking.profile']" />
        <a-card class="general-card" :title="$t('menu.list.searchTable')">
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
              </a-button >
              <a-tooltip :content="$t('searchTable.actions.refresh')">
                <div class="action-icon" @click="fetchData"
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
              <a-tooltip :content="$t('ranking.actions.setColumn')">
                <a-popover
                    trigger="click"
                    position="bl"
                    @popup-visible-change="popupVisibleChange"
                >
                  <div class="action-icon"><icon-settings size="18" /></div>
                  <template #content>
                    <div id="tableSetting">
                      <div
                          v-for="(item, index) in showColumns"
                          :key="item.dataIndex"
                          class="setting"
                      >
                        <div style="margin-right: 4px; cursor: move">
                          <icon-drag-arrow />
                        </div>
                        <div>
                          <a-checkbox
                              :value="inOriginalData(item)"
                              :disabled="inOriginalData(item)"
                              v-model="item.checked"
                              @change="handleChange($event, item as TableColumnData, index)"
                          >
                          </a-checkbox>
                        </div>
                        <div class="title">
                          <p>{{ item.title === '#' ? '序列号' : item.title }}</p>
                        </div>
                      </div>
                    </div>
                  </template>
                </a-popover>
              </a-tooltip>
            </a-col>
          </a-row>
          <a-table
              row-key="id"
              :loading="loading"
              :columns="(cloneColumns as TableColumnData[])"
              :data="renderData"
              :bordered="false"
              :size="size"
              :pagination="false"
          >
            <template #details="{ record }">
              <a-button type="text" size="small" @click="handleClick(record)">
                {{ $t('ranking.view.btn') }}
              </a-button>
            </template>
          </a-table>
        </a-card>
    </div>
    <a-drawer :width="1000"
              :visible="visible"
              :footer="false"
              @cancel="handleCancel"
              @open="setDrawer"
              unmountOnClose
    >
      <template #title>
        <header class="drawer-model-title">
          <div class="drawer-model-title-text">
            <p>{{ currentLLM.name }}</p>
          </div>
          <a-button
              class="llm-details-subscribe-btn"
              type="primary"
              size="large"
          >
            <template #icon>
              <icon-star :size="30"/>
            </template>
            <p>{{ $t('rankings.llm.details.subscribe.btn') }}</p>
          </a-button>
        </header>
      </template>
      <div>
        <a-tabs size="large">
          <a-tab-pane key="1" :title="$t('ranking.details.details')">
            <ModelProfile />
          </a-tab-pane>
          <a-tab-pane key="2" :title="$t('ranking.details.datasetScore')">
            <DatasetProfile />
          </a-tab-pane>
          <a-tab-pane key="3" :title="$t('ranking.details.competitionRecords')">
            <p>TODO</p>
          </a-tab-pane>
          <a-tab-pane key="4" :title="$t('ranking.details.discussions')">
            <ModelDiscussionArea :comment-details="commentDetails" @change-comment="handleChangeComment" />
          </a-tab-pane>
        </a-tabs>
      </div>
    </a-drawer>
  </div>
</template>

<script lang="ts" setup>
  import {computed, ref, reactive, watch, nextTick, onMounted} from 'vue';
  import axios from "axios";
  import apiCat from "@/api/main";
  import {getToken} from "@/utils/auth";
  import { useI18n } from 'vue-i18n';
  import useLoading from '@/hooks/loading';
  import { queryPolicyList, PolicyRecord, PolicyParams } from '@/api/list';
  import {LLMRankingData, queryDatasetColumnList, queryLLMList} from "@/api/model-list";
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

  const { loading, setLoading } = useLoading(false);
  const { t } = useI18n();
  const renderData = ref<LLMRankingData[]>();
  const currentColumns = ref<TableColumnData[]>();
  const cloneColumns = ref<Column[]>([]);
  const additionalColumns = ref<Column[]>(await queryDatasetColumnList());
  const showColumns = ref<Column[]>([]);
  const currentLLM = ref<LLMRankingData>();

  const size = ref<SizeProps>('medium');

  const commentDetails = ref([] as MyComment[]);

  const jwt = getToken();

  const handleClick = (data: LLMRankingData) => {
    currentLLM.value = data;
    visible.value = true;
  };

  const handleCancel = () => {
    visible.value = false;
  }

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
  const originalColumns = computed<TableColumnData[]>(() => [
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

  currentColumns.value = cloneDeep(originalColumns.value);
  for(let i = 0; i < additionalColumns.value.length; i += 1){
    currentColumns.value?.push(additionalColumns.value[i]);
  }
  const fetchData = async () => {
    setLoading(true);
    try {
      const { data } = await queryLLMList();
      renderData.value = data;
    } catch (err) {
      // you can report use errorHandler or other
    } finally {
      setLoading(false);
    }
  };

  const inOriginalData = (item: TableColumnData) => {
    for(let i = 0; i < originalColumns.value.length; i += 1){
      if (originalColumns.value[i].title === item.title){
        return true;
      }
    }
    return false;
  }
  fetchData();

  const handleSelectDensity = (
      val: string | number | Record<string, any> | undefined,
      e: Event
  ) => {
    size.value = val as SizeProps;
  };

  const handleChange = (
      checked: boolean | (string | boolean | number)[],
      column: Column,
      index: number
  ) => {
    if (!checked) {
      cloneColumns.value = cloneColumns.value.filter(
          (item) => item.dataIndex !== column.dataIndex
      );
    } else {
      cloneColumns.value.splice(index, 0, column);
    }
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
      () => currentColumns.value,
      (val) => {
        if(val !== undefined){
          cloneColumns.value = cloneDeep(originalColumns.value);
          showColumns.value = cloneDeep(val);
          showColumns.value.forEach((item, index) => {
            if(inOriginalData(item))
              item.checked = true;
          });
        }
      },
      { deep: true, immediate: true }
  );

  const popupVisibleChange = (val: boolean) => {
    if (val) {
      nextTick(() => {
        const el = document.getElementById('tableSetting') as HTMLElement;
        const sortable = new Sortable(el, {
          onEnd(e: any) {
            const { oldIndex, newIndex } = e;
            exchangeArray(cloneColumns.value, oldIndex, newIndex);
            exchangeArray(showColumns.value, oldIndex, newIndex);
          },
        });
      });
    }
  };

  const setDrawer = () => {
    // 设置Drawer样式
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

    getComment(currentLLM.value!.id.toString()!, commentDetails, jwt!);
  };


  const handleChangeComment = async (index: number, content: MyComment) => {
    await updateComment(ModelID, content, jwt!);
    if (index === -1) {
      commentDetails.value.push(content);
    } else {
      commentDetails.value[index].children.push(content);
    }
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

