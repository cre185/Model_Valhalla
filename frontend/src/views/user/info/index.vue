<template>
  <div class="container">
    <Breadcrumb :items="['menu.user', 'menu.user.info']" />
    <UserInfoHeader />
    <div class="content">
        <a-col class="content-top" :span="24">
          <a-grid :cols="2" :col-gap="16" :row-gap="16">
            <a-grid-item >
              <SubscribedList :userID="userInfo.accountId" :subscriptionType="'llm'" @showMore="handleShowMore" :key="toUpdate"/>
            </a-grid-item>
            <a-grid-item >
              <SubscribedList :userID="userInfo.accountId" :subscriptionType="'dataset'" @showMore="handleShowMore" :key="toUpdate"/>
            </a-grid-item>
          </a-grid>
        </a-col>
        <a-col class="content-bottom" :span="24" style="margin-top: 2vh">
          <a-grid :cols="24" :col-gap="16" :row-gap="16" style="height: 60vh">
            <a-grid-item :span="16">
              <AdversarialRecords @showMore="handleShowMore"/>
            </a-grid-item>
            <a-grid-item :span="8">
              <a-card class="general-card" style="height: 100%">
                <template #title>
                  <span style="font-weight: 900">
                    {{ $t('userInfo.title.receivedMessages') }}
                  </span>
                </template>
                <template #extra>
                  <a-link @click="handleShowMore(4)">{{ $t('userInfo.viewAll') }}</a-link>
                </template>
                <MessageBox :currentLocale="getLocale()" @changeShowingStatus="handleChangeStatus"/>
              </a-card>
            </a-grid-item>
          </a-grid>
        </a-col>
    </div>
    <a-drawer :width="showingDataType>=3 ? 700 : 1000"
              :visible="visible"
              :footer="false"
              style="display: flex;"
              unmountOnClose
              @open="setDrawer"
              @cancel="handleCancel"
    >
      <template #title>
        <header>
          <div style="font-size: 3vh" v-if="showingDataType===1">
            {{ $t('userInfo.title.subscribedModels') }}
          </div>
          <div style="font-size: 3vh" v-else-if="showingDataType===2">
            {{ $t('userInfo.title.subscribedDatasets') }}
          </div>
          <div style="font-size: 3vh" v-else-if="showingDataType===3">
            {{ $t('userInfo.title.adversarialRecords') }}
          </div>
          <div style="font-size: 3vh" v-else>
            {{ $t('userInfo.title.receivedMessages') }}
          </div>
        </header>
      </template>
      <MessageBox :current-locale="getLocale()" :size="'big'" v-if="showingDataType === 4"/>
      <a-space class="drawer-space" direction="vertical" fill v-else-if="showingDataType === 3">
        <a-row justify="center" align="center" style="margin-left: 1vw">
          <a-col :span="20">
            <a-form label-align="left">
              <a-row :gutter="16">
                <a-col :span="12" flex="auto">
                  <a-form-item
                      :label-col-props="{ span: 6 }"
                      :wrapper-col-props="{ span: 18 }"
                      field="modelA"
                      :label="$t('userInfo.adversarial.records.modelA')"
                  >
                    <a-input v-model="searchModelA"
                             :placeholder="$t('userInfo.adversarial.records.modelA.placeholder')"
                    />
                  </a-form-item>
                </a-col>
                <a-col :span="12">
                  <a-form-item
                      :label-col-props="{ span: 6 }"
                      :wrapper-col-props="{ span: 18 }"
                      field="modelB"
                      :label="$t('userInfo.adversarial.records.modelB')"
                  >
                    <a-input v-model="searchModelB"
                             :placeholder="$t('userInfo.adversarial.records.modelB.placeholder')"
                    />
                  </a-form-item>
                </a-col>
              </a-row>
              <a-row :gutter="16">
                <a-col :span="24">
                  <a-form-item
                      :label-col-props="{ span: 3 }"
                      :wrapper-col-props="{ span: 21 }"
                      field="contentSizeLowerBound"
                      :label="$t('searchDataset.form.contentSize')"
                      style="margin-bottom: 0"
                  >
                    <a-range-picker
                        v-model="searchDateRange"
                        :placeholder="[$t('userInfo.adversarial.records.testTime.placeholder1'),
                                    $t('userInfo.adversarial.records.testTime.placeholder2')]"
                        style=" width: 100%;"
                    />
                  </a-form-item>
                </a-col>
              </a-row>
            </a-form>
          </a-col>
          <a-col :span="4" style="display:flex; flex-direction: column">
            <a-button style="margin: auto auto 1vh auto" type="primary" @click="handleSearchRecord">
              <template #icon>
                <icon-search/>
              </template>
              {{ $t('userInfo.adversarial.records.search.btn') }}
            </a-button>
            <a-button style="margin: 1vh auto auto auto" @click="handleReset">
              <template #icon>
                <icon-refresh/>
              </template>
              {{ $t('userInfo.adversarial.records.reset.btn') }}
            </a-button>
          </a-col>
        </a-row>
        <a-list :bordered="false"
        >
          <a-list-item v-for="(data, index) in subscribedDataList" :key="index">
            <a-list-item-meta
                :title="`${$t('userInfo.adversarial.models')}${data.model} & ${data.adversarialModel}`"
                :description="data.battleTime"
                :style="{visibility: data.id !== undefined ? 'visible' : 'hidden'}"
            >
            </a-list-item-meta>
            <template #actions>
              <a-button type="outline" size="mini" @click="handleShowDetails(data)">
                <template #icon>
                  <icon-exclamation-circle />
                </template>
                {{ $t('userInfo.adversarial.records.details.btn') }}
              </a-button>
            </template>
          </a-list-item>
        </a-list>
      </a-space>
      <a-space class="drawer-space" direction="vertical" fill v-else>
        <a-input-search v-model="searchContent"
                        :style="{width:'45vw', alignItems: 'center'}"
                        :placeholder="showingDataType===1 ? $t('userInfo.subscription.llm.input.placeholder') :
                                $t('userInfo.subscription.dataset.input.placeholder') "
                        @search="handleSearch"
                        @blur="handleSearch"
        />
        <a-row :gutter="[24, 24]" style="margin-top: 3vh">
          <a-col
              v-for="item in subscribedDataList"
              :key="item.id"
              :span="12"
              class="list-col"
          >
            <div class="card-wrap">
              <CardWrap
                  :content="item"
                  :contentType="showingDataType===1 ? 'llm' : 'dataset'"
                  :ID="item.id"
                  :userID="parseInt(userInfo.accountId, 10)"
              />
            </div>
          </a-col>
        </a-row>
      </a-space>
      <a-pagination style="justify-content: center; margin: auto auto 2vh auto"
                    :total="totalDataNum"
                    :current="currentPage"
                    :page-size="pageSize"
                    @change="handlePageChange"
                    show-jumper
                    v-if="showingDataType !== 4"
      />
    </a-drawer>
    <a-modal v-if="showingRecord!==undefined"
             :visible="recordVisible"
             :footer="false"
             width="40vw"
             @cancel="handleCancelModal"
             :hide-title="true">
      <div style="display: flex; flex-direction: column; height: 70vh">
        <a-space v-for="(data, index) in showingRecord.QA"
                 direction="vertical"
                 :key="index"
        >
          <div style="font-size: 2vh; font-weight: 600; padding-bottom: 1.5vh; border-bottom: solid 4px lightgrey">
            {{ `Round ${index + 1}` }}
          </div>
          <a-form
              :label-col-props="{ span: 5 }"
              :wrapper-col-props="{ span: 19 }"
          >
            <a-form-item :label="$t('userInfo.adversarial.records.details.question')" :label-attrs="{style: {color: '#1c61ff'}}">
              {{ data.question }}
            </a-form-item>
            <a-form-item :label="showingRecord.model" :label-attrs="{style: {color: '#1c61ff'}}">
              {{ data.answerA }}
            </a-form-item>
            <a-form-item :label="showingRecord.adversarialModel" :label-attrs="{style: {color: '#1c61ff'}}">
              {{ data.answerB }}
            </a-form-item>
          </a-form>
        </a-space>
        <a-divider orientation="center">{{
            `${$t('userInfo.adversarial.records.details.result.prefix')} ${ showingRecord.winner } ${$t('userInfo.adversarial.records.details.result.suffix')}` }}</a-divider>
      </div>
    </a-modal>
  </div>
</template>

<script lang="ts" setup>
  import {computed, onMounted, reactive, ref} from "vue";
  import { useUserStore } from '@/store';
  import {
    BattleRecordsData, queryBattleRecordsData,
    querySubscribedDatasets,
    querySubscribedModels,
    SubscribedDatasetRecord,
    SubscribedModelRecord
  } from "@/api/user-center";
  import router from "@/router";
  import List from "@/components/navbar/components/list.vue";
  import {getMessageData, userToDataset} from "@/api/message";
  import {useI18n} from "vue-i18n";
  import {getLocale} from "@arco-design/web-vue";
  import MessageBox from "@/components/navbar/components/message-box.vue";
  import eventBus from "@/api/event-bus";
  import CardWrap from "./components/card-wrap.vue";
  import UserInfoHeader from './components/user-info-header.vue';
  import SubscribedList from './components/subscribed-list.vue';
  import AdversarialRecords from "./components/adversarial-records.vue";

  const userInfo = useUserStore();
  const visible = ref(false);
  const recordVisible = ref(false);
  const t = useI18n();
  const subscribedDataList = ref<SubscribedModelRecord[] | SubscribedDatasetRecord[] | BattleRecordsData[]>([]);
  const showingDataType = ref(1);
  const toUpdate = ref(false);
  const totalDataNum = ref();
  const currentPage = ref(1);
  const pageSize = ref(8);
  const searchContent = ref('');
  const showingRecord = ref<BattleRecordsData>();
  const searchModelA = ref('');
  const searchModelB = ref('');
  const searchDateRange = ref([]);
  const messageData = ref< userToDataset[]>([]);
  const unreadCount = computed(() => {
    return messageData.value.filter((item) => !item.read).length;
  });

  const fetchData = async ()=> {
    if(showingDataType.value === 1){
      subscribedDataList.value = await querySubscribedModels(parseInt(userInfo.accountId!, 10));
    }
    else if (showingDataType.value === 2){
      subscribedDataList.value = await querySubscribedDatasets(parseInt(userInfo.accountId!, 10));
    }
    else if (showingDataType.value === 3) {
      subscribedDataList.value = await queryBattleRecordsData(parseInt(userInfo.accountId!, 10));
      subscribedDataList.value.sort((a: any, b: any) => {
        if(new Date(a.battleTime) > new Date(b.battleTime)) {
          return -1;
        }
        if(new Date(a.battleTime) < new Date(b.battleTime)) {
          return 1;
        }
        return (a.model > b.model) ? -1 : 1;
      });
    }
    else {
      messageData.value = await getMessageData(getLocale(), t);
    }
  }

  const handleShowMore = (type: number) => {
    showingDataType.value = type;
    searchModelA.value = '';
    searchModelB.value = '';
    searchDateRange.value = [];
    if(type === 3){
      pageSize.value = 7;
    }
    fetchData().then(() => {
      if(type < 4){
        totalDataNum.value = subscribedDataList.value.length;
        subscribedDataList.value = subscribedDataList.value.slice(0, pageSize.value);
        searchContent.value = '';
      }
      else{
        totalDataNum.value = messageData.value.length;
      }
      visible.value = true;
    })
  }

  const handleCancel = () => {
    visible.value = false;
    toUpdate.value = !toUpdate.value;
  }

  const setDrawer = () => {
    const drawerHeader = document.querySelector('.arco-drawer-header');
    if (drawerHeader) {
      drawerHeader.style.height = '8vh';
      drawerHeader.style.paddingLeft = '3vw';
    }

    const drawerBody = document.querySelector('.arco-drawer-body');
    if (drawerBody) {
      drawerBody.style.display = 'flex';
      drawerBody.style.flexDirection = 'column';
      drawerBody.style.justifyContent= 'center';
    }

    if(showingDataType.value < 3){
      const drawerInput = document.querySelector('.drawer-space > .arco-space-item');
      if (drawerInput) {
        drawerInput.style.display = 'flex';
        drawerInput.style.alignItems = 'center';
        drawerInput.style.justifyContent = 'center';
      }
    }

    const drawerCloseBtn = document.querySelector('.arco-drawer-close-btn');
    if(drawerCloseBtn){
      drawerCloseBtn.style.visibility = 'hidden';
    }
  }

  const handlePageChange = (current: number) => {
    fetchData().then(() => {
      currentPage.value = current;
      subscribedDataList.value =
            subscribedDataList.value.slice((current - 1) * pageSize.value, currentPage.value * pageSize.value);
    });
  }

  const handleSearch = () => {
    fetchData().then(() => {
      currentPage.value = 1;
      subscribedDataList.value =
          subscribedDataList.value.filter((item: any) => item.name.includes(searchContent.value));
      subscribedDataList.value = subscribedDataList.value.slice(0, pageSize.value);
    });
  }

  const handleSearchRecord = () => {
    fetchData().then(() => {
      currentPage.value = 1;
      subscribedDataList.value =
          subscribedDataList.value.filter((item: any) => item.model.includes(searchModelA.value) &&
              item.adversarialModel.includes(searchModelB.value) &&
              ( new Date(item.battleTime) >= new Date(searchDateRange.value[0]) ||
              new Date(searchDateRange.value[0]).toString() === 'Invalid Date') &&
              ( new Date(item.battleTime) <= new Date(searchDateRange.value[1]) ||
                  new Date(searchDateRange.value[1]).toString() === 'Invalid Date')
          );
      subscribedDataList.value = subscribedDataList.value.slice(0, pageSize.value);
    });
  }

  const handleReset = () => {
    searchModelA.value = '';
    searchModelB.value = '';
    searchDateRange.value = [];
    fetchData().then(() => {
      currentPage.value = 1;
      subscribedDataList.value = subscribedDataList.value.slice(0, pageSize.value);
    });
  }

  const handleShowDetails = (record: BattleRecordsData) => {
    recordVisible.value = true;
    showingRecord.value = record;
  }

  const handleCancelModal = () => {
    recordVisible.value = false;
  }

  const handleChangeStatus = () => {
    eventBus.emit('messageRead');
  }
</script>

<script lang="ts">
  export default {
    name: 'Info',
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }

  .content {
    margin-top: 12px;

    .tab-pane-wrapper {
      padding: 0 16px 16px 16px;
    }
  }
</style>

<style lang="less" scoped>
  .mobile {
    .content {
      display: block;
      /*&-left {
        margin-right: 0;
        margin-bottom: 16px;
      }
      &-right {
        width: 100%;
      }*/
    }
  }
</style>
