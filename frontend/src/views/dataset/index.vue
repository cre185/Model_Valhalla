<template>
  <div class="container">
    <Breadcrumb :items="['menu.dataset', 'menu.dataset.details']" />
    <a-card class="general-card" :title="$t('dataset.searchDataset')">
      <a-row>
        <a-col :flex="1">
          <a-form
              :model="formModel"
              :label-col-props="{ span: 6 }"
              :wrapper-col-props="{ span: 18 }"
              label-align="left"
          >
            <a-row :gutter="16">
              <a-col :span="4">
                <a-form-item
                    field="number"
                    :label="$t('searchDataset.form.number')"
                >
                  <a-input style="width: 90%"
                      v-model="formModel.number"
                      :placeholder="$t('searchDataset.form.number.placeholder')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item field="name" :label="$t('searchDataset.form.name')">
                  <a-input
                      v-model="formModel.name"
                      :placeholder="$t('searchDataset.form.name.placeholder')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="4">
                <a-form-item
                    field="isSubjective"
                    :label="$t('searchDataset.form.isSubjective')"
                >
                  <a-select
                      style="margin-left: 10%"
                      v-model="formModel.isSubjective"
                      :options="isSubjectiveOptions"
                      :placeholder="$t('searchDataset.form.selectDefault')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                    field="domain"
                    :label="$t('searchDataset.form.domain')"
                >
                  <a-select
                      v-model="formModel.domain"
                      :options="domainOptions"
                      :placeholder="$t('searchDataset.form.domain.placeholder')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                    field="tags"
                    :label="$t('searchDataset.form.tags')"
                >
                  <a-select
                      v-model="formModel.tags"
                      multiple :max-tag-count="3" allow-clear
                      :options="tagOptions"
                      :placeholder="$t('searchDataset.form.selectDefault')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="4">
                <a-form-item
                    field="contentSizeLowerBound"
                    :label="$t('searchDataset.form.contentSize')"
                >
                  <a-input-number style="margin-left: 10%" v-model="formModel.contentSizeLowerBound"
                                  :placeholder="$t('searchDataset.form.contentSize.lowerBound')" class="input-demo" />
                </a-form-item>
              </a-col>
              <a-col :span="4">
                <a-form-item
                    field="contentSizeUpperBound"
                    :label="$t('searchDataset.form.contentSize.to')"
                >
                  <a-input-number style="width: 90%" v-model="formModel.contentSizeUpperBound"
                                  :placeholder="$t('searchDataset.form.contentSize.upperBound')" class="input-demo" />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                    field="createdTime"
                    :label="$t('searchDataset.form.createdTime')"
                >
                  <a-range-picker
                      v-model="formModel.createdTime"
                      style="width: 100%"
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
              {{ $t('searchDataset.form.search') }}
            </a-button>
            <a-button @click="reset">
              <template #icon>
                <icon-refresh />
              </template>
              {{ $t('searchDataset.form.reset') }}
            </a-button>
          </a-space>
        </a-col>
      </a-row>
      <a-divider style="margin-top: 0" />
      <a-row style="margin-bottom: 16px">
        <a-col :span="12">
          <a-space>
            <a-button type="primary" @click="UploadClick">
              <template #icon>
                <icon-plus />
              </template>
              {{ $t('searchDataset.operation.create') }}
            </a-button>
            <a-button @click="feedbackClick">
              <template #icon>
                <icon-exclamation/>
              </template>
              {{ $t('searchDataset.operation.feedback') }}
            </a-button>
          </a-space>
        </a-col>
        <a-col
            :span="12"
            style="display: flex; align-items: center; justify-content: end"
        >
          <a-button @click="handleBatchDownload">
            <template #icon>
              <icon-download />
            </template>
            {{ $t('searchDataset.operation.download') }}
          </a-button>
          <a-tooltip :content="$t('searchDataset.actions.refresh')">
            <div class="action-icon" @click="search"
            ><icon-refresh size="18"
            /></div>
          </a-tooltip>
        </a-col>
      </a-row>
      <a-table
          row-key="id"
          :loading="loading"
          :pagination="pagination"
          :columns="(columns as TableColumnData[])"
          :data="renderData"
          @page-change="onPageChange"
      >
        <template #id="{ record }">
          <a-checkbox :value="record.id" @change="handleSelectDataset(record)">{{record.id}}</a-checkbox>
        </template>
        <template #tags="{ record }">
          <a-tag v-for="(tag, index) in record.tags.slice(0, 3)" :key="index" style="margin: 1% 2%">
            {{ tag }}
          </a-tag>
          <a-tag style="margin: 1% 2%" v-if="record.tags.length > 3">
            {{ `+${record.tags.length - 3}...`}}
          </a-tag>
          <a-input
              v-if="record.showInput"
              :id="`tagInput${record.id}`"
              :style="{ width: '5vw'}"
              size="mini"
              v-model.trim="record.newTag"
              @keyup.enter="handleAddTag(record)"
              @blur="handleAddTag(record)"
          />
          <a-tag
              v-else
              :style="{
                width: '5vw',
                backgroundColor: 'var(--color-fill-2)',
                border: '1px dashed var(--color-fill-3)',
                cursor: 'pointer',
              }"
              @click="handleEditTag(record)"
          >
            <template #icon>
              <icon-plus />
            </template>
            {{ $t('searchDataset.tags.addTag') }}
          </a-tag>
        </template>
        <template #isSubjective="{ record }">
          <div v-if="record.isSubjective">
            {{ $t('searchDataset.form.isSubjective.subjective') }}
          </div>
          <div v-else>
            {{ $t('searchDataset.form.isSubjective.objective') }}
          </div>
        </template>
        <template #operations="{ record }">
          <a-button type="text" size="small" @click="handleDownload(record)">
            {{ $t('searchDataset.columns.operations.download') }}
          </a-button>
          <a-button type="text" size="small" @click="handleDetails(record)">
            {{ $t('searchDataset.columns.operations.view') }}
          </a-button>
        </template>
      </a-table>
    </a-card>
    <a-drawer :width="1000"
              :visible="visible"
              :footer="false"
              @cancel="handleCancel"
              @open="setDrawer"
              unmountOnClose
              v-if="currentDataset !== undefined"
    >
      <template #title>
        <header class="drawer-model-title" :key="currentDataset.isSubscribed">
          <a-space direction="horizontal" style="margin-top: 8vh; margin-left: -6vw; padding: 2vh 0vw 3vh 3vw;
          border-bottom: 5px solid lightgrey ">
            <a-avatar><img :src="currentDataset.uploadUserAvatar"/></a-avatar>
            <p style="padding-right: 20vw">
              {{`${currentDataset.uploadUsername} · ${currentDataset.createdTime} ${$t('searchDataset.operation.create')}`}}
            </p>
            <a-button shape="round" type="primary" style="width: 7vw" @click="handleDownload(currentDataset)">
              <template #icon>
                <icon-download/>
              </template>
              <p style="font-weight: bolder">
                {{ $t('searchDataset.columns.operations.download') }}
              </p>
            </a-button>
            <a-button v-if="!modify" shape="round" style="margin-left: 1.5vw; width: 7vw" @click="handleFeedback()">
              <template #icon>
                <icon-exclamation/>
              </template>
              <p style="font-weight: bolder">
                {{ $t('searchDataset.operation.feedback') }}
              </p>
            </a-button>
            <a-button v-else-if="!modifySign" shape="round" style="margin-left: 1.5vw; width: 7vw" @click="handleEdit()">
              <template #icon>
                <icon-pen/>
              </template>
              <p style="font-weight: bolder">
                {{ $t('searchDataset.operation.edit') }}
              </p>
            </a-button>
            <a-button v-else-if="modifySign" shape="round" style="margin-left: 1.5vw; width: 7vw" @click="handleSave()">
              <template #icon>
                <icon-save/>
              </template>
              <p style="font-weight: bolder">
                {{ $t('searchDataset.operation.save') }}
              </p>
            </a-button>
          </a-space>
          <a-space direction="horizontal">
            <div class="drawer-model-title-text">
              <p v-if="modifySign">
                <a-input :input-attrs="{style: {marginTop: '-1vh', fontSize: '60px'}}" :default-value="currentDataset.name"
                         :placeholder="$t('dataset.details.modifyName')" @change="handleChange" allow-clear />
              </p>
              <p v-else>{{ currentDataset.name }}</p>
            </div>
            <a-button
                v-if="!modify && currentDataset.isSubscribed"
                class="llm-details-subscribe-btn"
                type="primary"
                size="large"
                @click="handleSubscribe"
            >
              <template #icon>
                <icon-star-fill style="margin-top: 15%" :size="18"/>
              </template>
              <p>{{ $t('dataset.details.unsubscribe.btn') }}</p>
            </a-button>
            <a-upload
                v-else
                action="http://localhost:8000/user/logout"
                accept=".csv"
                :file-list="fileList"
                :limit="1"
                @change="uploadChange"
            >
              <template #upload-button>
                <a-button
                    :disabled="!modifySign"
                    class="llm-details-subscribe-btn"
                    type="primary"
                    size="large"
                >
                  <template #icon>
                    <icon-attachment :size="18"/>
                  </template>
                  <p>{{ $t('dataset.details.changeFile.btn') }}</p>
                </a-button>
              </template>
            </a-upload>
          </a-space>
        </header>
      </template>
      <div>
        <a-tabs size="large"
                style="margin-top: 7vh"
                default-active-key="1"
                v-if="toShowTab===1"
        >
          <a-tab-pane key="1" :title="$t('dataset.details.details')">
            <DatasetProfile :datasetID="currentDataset.id.toString()" :update="updateFlag" :update-now="updateNow" @change-tag="fetchData" @update-modify="handleUpdateModify"/>
          </a-tab-pane>
          <a-tab-pane key="2" :title="$t('dataset.details.preview')">
            <DatasetPreview :datasetID="currentDataset.id.toString()"/>
          </a-tab-pane>
          <a-tab-pane key="3" :title="$t('dataset.details.testScore')">
            <DatasetPerformance :datasetID="currentDataset.id.toString()" />
          </a-tab-pane>
          <a-tab-pane key="4" :title="$t('dataset.details.discussions')">
            <DatasetDiscussionArea :comment-details="commentDetails" :dataset-id="currentDataset.id.toString()"
            @change-comment="handleChangeComment"/>
          </a-tab-pane>
        </a-tabs>
        <a-tabs size="large"
                style="margin-top: 7vh"
                default-active-key="2"
                v-else-if="toShowTab===2"
        >
          <a-tab-pane key="1" :title="$t('dataset.details.details')">
            <DatasetProfile :datasetID="currentDataset.id.toString()" :modify="modifySign" @change-tag="fetchData"/>
          </a-tab-pane>
          <a-tab-pane key="2" :title="$t('dataset.details.preview')">
            <DatasetPreview :datasetID="currentDataset.id.toString()"/>
          </a-tab-pane>
          <a-tab-pane key="3" :title="$t('dataset.details.testScore')">
            <DatasetPerformance :datasetID="currentDataset.id.toString()" />
          </a-tab-pane>
          <a-tab-pane key="4" :title="$t('dataset.details.discussions')">
            <DatasetDiscussionArea :comment-details="commentDetails" :dataset-id="currentDataset.id.toString()"
                                   @change-comment="handleChangeComment"/>
          </a-tab-pane>
        </a-tabs>
        <a-tabs size="large"
                style="margin-top: 7vh"
                default-active-key="3"
                v-else-if="toShowTab===3"
        >
          <a-tab-pane key="1" :title="$t('dataset.details.details')">
            <DatasetProfile :datasetID="currentDataset.id.toString()" :modify="modifySign" @change-tag="fetchData"/>
          </a-tab-pane>
          <a-tab-pane key="2" :title="$t('dataset.details.preview')">
            <DatasetPreview :datasetID="currentDataset.id.toString()"/>
          </a-tab-pane>
          <a-tab-pane key="3" :title="$t('dataset.details.testScore')">
            <DatasetPerformance :datasetID="currentDataset.id.toString()" />
          </a-tab-pane>
          <a-tab-pane key="4" :title="$t('dataset.details.discussions')">
            <DatasetDiscussionArea :comment-details="commentDetails" :dataset-id="currentDataset.id.toString()"
                                   @change-comment="handleChangeComment"/>
          </a-tab-pane>
        </a-tabs>
        <a-tabs size="large"
                style="margin-top: 7vh"
                default-active-key="4"
                v-else
        >
          <a-tab-pane key="1" :title="$t('dataset.details.details')">
            <DatasetProfile :datasetID="currentDataset.id.toString()" :modify="modifySign" @change-tag="fetchData"/>
          </a-tab-pane>
          <a-tab-pane key="2" :title="$t('dataset.details.preview')">
            <DatasetPreview :datasetID="currentDataset.id.toString()"/>
          </a-tab-pane>
          <a-tab-pane key="3" :title="$t('dataset.details.testScore')">
            <DatasetPerformance :datasetID="currentDataset.id.toString()" />
          </a-tab-pane>
          <a-tab-pane key="4" :title="$t('dataset.details.discussions')">
            <DatasetDiscussionArea :comment-details="commentDetails" :dataset-id="currentDataset.id.toString()"
                                   @change-comment="handleChangeComment"/>
          </a-tab-pane>
        </a-tabs>
      </div>
    </a-drawer>
    <DatasetFeedback :datasetFeedbackID="currentDataset?.id.toString()" :datasetShown="visible.toString()"
    v-model:visible="showDatasetFeedback"/>
    <DatasetUpload
    v-model:visible="showDatasetUpload"/>
  </div>
</template>

<script lang="ts" setup>
/* eslint-disable */
import {computed, ref, reactive, nextTick, shallowRef, onMounted} from 'vue';
  import { useI18n } from 'vue-i18n';
  import { useUserStore } from "@/store";
  import useLoading from '@/hooks/loading';
  import { PolicyParams } from '@/api/list';
  import { Pagination } from '@/types/global';
  import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import { FileItem } from "@arco-design/web-vue/es/upload/interfaces";
  import {
    DatasetData,
    queryDatasetList,
    updateDatasetTags,
    getDatasetFile,
    updateDataset,
    uploadDatasetFile,
    isDatasetSubscribed,
    subscribeDataset
  } from "@/api/dataset";
  import MyComment, {getComment, updateComment} from "@/api/comment";
  import DatasetProfile from "@/views/dataset/components/dataset-profile.vue";
  import DatasetPreview from "@/views/dataset/components/dataset-preview.vue";
  import DatasetPerformance from "@/views/dataset/components/dataset-performance.vue";
  import DatasetDiscussionArea from "@/views/dataset/components/dataset-discussion-area.vue";
  import { getToken } from "@/utils/auth";
  import DatasetFeedback from "./components/datasetfeedback.vue";
  import DatasetUpload from "./components/datasetupload.vue";

  const userStore = useUserStore();
  const modify = userStore.role === 'admin';
  const modifySign = ref(false);
  const updateFlag = shallowRef({edit: false});
  const updateNow = ref(false);
  const fileList = ref<FileItem[]>([]);
  const props = defineProps(['toShowDetailsID', 'toShowPanelIndex']);
  const toShowTab = ref(1);

  const generateFormModel = () => {
    return {
      number: '',
      name: '',
      isSubjective: '',
      domain: '',
      tags: [],
      contentSizeLowerBound: undefined,
      contentSizeUpperBound: undefined,
      createdTime: [],
      status: '',
    };
  };
  const { loading, setLoading } = useLoading(true);
  const { t } = useI18n();
  const formModel = ref(generateFormModel());
  const renderData = ref<DatasetData[]>();
  const basePagination: Pagination = {
    current: 1,
    pageSize: 20,
  };
  const pagination = reactive({
    ...basePagination,
  });
  const columns = computed<TableColumnData[]>(() => [
    {
      title: t('searchDataset.columns.index'),
      dataIndex: 'id',
      slotName: 'id',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('searchDataset.columns.name'),
      dataIndex: 'name',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('searchDataset.columns.isSubjective'),
      dataIndex: 'isSubjective',
      slotName: 'isSubjective',
      align: "center",
    },
    {
      title: t('searchDataset.columns.domain'),
      dataIndex: 'domain',
      align: "center",
    },
    {
      title: t('searchDataset.columns.contentSize'),
      dataIndex: 'contentSize',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('searchDataset.columns.createdTime'),
      dataIndex: 'createdTime',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('searchDataset.columns.tags'),
      dataIndex: 'tags',
      slotName: 'tags',
      align: "center",
    },
    {
      title: t('searchDataset.columns.operations'),
      dataIndex: 'operations',
      slotName: 'operations',
      align: "center",
    },
  ]);
  const isSubjectiveOptions = computed<SelectOptionData[]>(() => [
    {
      label: t('searchDataset.form.isSubjective.subjective'),
      value: 'subjective',
    },
    {
      label: t('searchDataset.form.isSubjective.objective'),
      value: 'objective',
    },
  ]);
  const tagOptions = ref<SelectOptionData[]>([]);
  const domainOptions = ref<SelectOptionData[]>([]);
  const visible = ref(false);
  const currentDataset = ref<DatasetData>();
  const commentDetails = ref([] as MyComment[]);
  const userInfo = useUserStore();
  const jwt = getToken();
  const showDatasetFeedback = ref(false);
  const showDatasetUpload = ref(false);
  const UploadClick = () => {
    showDatasetUpload.value = true;
  }

  const feedbackClick = () => {
    showDatasetFeedback.value = true;
  }

  const getTagOptions = () => {
    const currentTags = new Set();
    tagOptions.value = [];
    for(let i = 0; i < renderData.value!.length; i += 1){
      for(let j = 0; j < renderData.value![i].tags.length; j += 1){
        currentTags.add(renderData.value![i].tags[j]);
      }
    }
    currentTags.forEach((value, valueAgain, set) => {
      const tag = value as string;
      tagOptions.value.push({label: tag, value: tag})
    })
  }
  const getDomainOptions = () => {
    const currentDomains = new Set();
    domainOptions.value = [];
    for(let i = 0; i < renderData.value!.length; i += 1){
      if(renderData.value![i].domain){
        currentDomains.add(renderData.value![i].domain);
      }
    }
    currentDomains.forEach((value, valueAgain, set) => {
      const domain = value as string;
      domainOptions.value.push({label: domain, value: domain})
    })
  }
  const fetchData = async (
      params: PolicyParams = { current: 1, pageSize: 20 }
  ) => {
    setLoading(true);
    try {
      const data = await queryDatasetList();
      renderData.value = data.data;
      getTagOptions();
      getDomainOptions();
      pagination.current = params.current;
      pagination.total = data.total;
    } catch (err) {
      // you can report use errorHandler or other
    } finally {
      setLoading(false);
    }
  };

  const onPageChange = (current: number) => {
    pagination.current = current;
  };

  const reset = () => {
    formModel.value = generateFormModel();
    fetchData();
  };

  const search = () => {
    fetchData().then(returnValue => {
      renderData.value = renderData.value!.filter(data => data.name.includes(formModel.value.name));
      if(formModel.value.number){
        renderData.value = renderData.value!.filter(data => data.id === parseInt(formModel.value.number, 10));
      }
      if(formModel.value.isSubjective){
        renderData.value = renderData.value!.filter(data => data.isSubjective === (formModel.value.isSubjective === "subjective"));
      }
      if(formModel.value.domain){
        renderData.value = renderData.value!.filter(data => data.domain === formModel.value.domain);
      }
      if(formModel.value.tags.length !== 0){
        renderData.value = renderData.value!.filter(data => {
          for(let i = 0; i < formModel.value.tags.length; i += 1){
            if(data.tags.includes(formModel.value.tags[i])){
              return true;
            }
          }
          return false;
        })
      }
      const lowerBound = formModel.value.contentSizeLowerBound === undefined ? 0 : formModel.value.contentSizeLowerBound;
      const upperBound = formModel.value.contentSizeUpperBound === undefined ? Infinity : formModel.value.contentSizeUpperBound;
      renderData.value = renderData.value!.filter(data => data.contentSize >= lowerBound && data.contentSize <= upperBound);
      const dateEarliest = new Date(formModel.value.createdTime[0]);
      const dateLatest = new Date(formModel.value.createdTime[1]);
      renderData.value = renderData.value!.filter(data => {
        const createdTime = new Date(data.createdTime)
        const laterThanEarliest = dateEarliest.toString() === 'Invalid Date' ? true : createdTime >= dateEarliest;
        const earlierThanLatest = dateLatest.toString() === 'Invalid Date' ? true : createdTime <= dateLatest;
        return laterThanEarliest && earlierThanLatest;
      })
    });
  }

  const handleEditTag = (record: DatasetData) => {
    record.showInput = true;
    renderData.value?.map(dataset => {
      if(dataset.id !== record.id){
        dataset.showInput = false;
      }
      return dataset;
    })

    nextTick(() => {
      for(let i = 0; i < renderData.value!.length; i += 1){
        if(renderData.value![i].showInput){
          document.getElementById(`tagInput${renderData.value![i].id}`)!.childNodes[1].focus();
        }
      }
      getTagOptions();
    });
  }

  const handleAddTag = (record: DatasetData) => {
    if (record.newTag) {
      if(!record.tags.includes(record.newTag)){
        record.tags.unshift(record.newTag)
        updateDatasetTags(record.id, record.tags);
        record.newTag = '';
      }
    }
    record.showInput = false;
  };

  const handleDownload = async (record: DatasetData) => {
    const downloadLink = document.createElement('a');
    await getDatasetFile(record.id).then(returnValue => {
      downloadLink.href = returnValue.data.data_file;
      downloadLink.download = `${record.name}.csv`;
      const container = document.createElement('div');
      container.appendChild(downloadLink);
      document.body.appendChild(container);
      downloadLink.click();
      document.body.removeChild(container);
    });
  };

  const handleFeedback = () => {
    showDatasetFeedback.value = true;

  }
  const handleSelectDataset = (record: DatasetData) => {
    record.toDownload = !record.toDownload;
  }

  const handleBatchDownload = async () => {
    for (const item of renderData.value!.filter(item => item.toDownload)) {
      await handleDownload(item);
    }
  };

  const handleCancel = () => {
    toShowTab.value = 1;
    visible.value = false;
  }

  const handleDetails = (record: DatasetData) => {
    currentDataset.value = record;
    visible.value = true;
  }

  const handleChangeComment = async (index: number, content: MyComment) => {
    await updateComment(currentDataset.value!.id.toString()!, content, jwt!, false);
    if (index === -1) {
      commentDetails.value.push(content);
    } else {
      commentDetails.value[index].children.push(content);
    }
  };

  const handleSubscribe = () =>{
    subscribeDataset(currentDataset.value!.id);
    currentDataset.value!.isSubscribed = !currentDataset.value!.isSubscribed;
  }

  const setDrawer = () => {
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

    isDatasetSubscribed(parseInt(userInfo.accountId!, 10), currentDataset.value!.id).then(returnValue => {
      currentDataset.value!.isSubscribed = returnValue;
    });
    getComment(currentDataset.value!.id.toString(), commentDetails, jwt!, false);
  };

  const handleEdit = () => {
    modifySign.value = true;
    updateFlag.value.edit = true;
    updateNow.value = true;
  }

  const handleSave = async () => {
    modifySign.value = false;
    updateFlag.value.edit = false;
    const data = {name: currentDataset.value?.name};
    await updateDataset(currentDataset.value!.id, data);
    if (fileList.value.length > 0) {
      const uploadPacket = new FormData();
      uploadPacket.append('name', currentDataset.value!.name);
      uploadPacket.append('file', fileList.value[0].file as Blob);
      await uploadDatasetFile(uploadPacket);
      fileList.value = [];
    }
  }

  const handleChange = (value:any) => {
    currentDataset.value!.name = value;
  }

  const uploadChange = (fileItemList: FileItem[], fileItem: FileItem) => {
    fileList.value = fileItemList;
  }

  const handleUpdateModify = () => {
    updateNow.value = false;
  }

  onMounted(() => {
    fetchData().then(() => {
      if(props.toShowDetailsID !== '' || props.toShowDetailsID === undefined){
        for(let i = 0; i < renderData.value!.length; i += 1){
          if(renderData.value![i].id === parseInt(props.toShowDetailsID, 10)){
            currentDataset.value = renderData.value![i];
            visible.value = true;
            break;
          }
        }
      }
      if(props.toShowPanelIndex !== '' || props.toShowPanelIndex === undefined){
        toShowTab.value = parseInt(props.toShowPanelIndex, 10);
        console.log(toShowTab.value);
      }
    })
  });
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }
  :deep(.arco-table-th) {
    &:last-child {
      .arco-table-th-item-title {
        margin-left: 16px;
      }
    }
  }
  :deep(.arco-form-item-label){
    white-space: nowrap;
    font-size: 100%;
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

  .drawer-model-title-text{
    margin-top: -1vh;
    font-size: 60px;
  }

  .llm-details-subscribe-btn{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: 2vw;
    padding: 5px 20px;
    font-size: 18px;
  }
</style>
