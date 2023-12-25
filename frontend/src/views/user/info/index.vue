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
        <a-col class="content-bottom" :span="24" style="margin-top: 5vh">
          <a-grid :cols="24" :col-gap="16" :row-gap="16">
            <a-grid-item :span="18">
              <a-card>
                1
              </a-card>
            </a-grid-item>
            <a-grid-item :span="6">
              <LatestNotification/>
            </a-grid-item>
          </a-grid>
        </a-col>
    </div>
  </div>
  <a-drawer :width="1000"
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
        <div style="font-size: 3vh" v-else>
          {{ $t('userInfo.title.subscribedDatasets') }}
        </div>
      </header>
    </template>
    <a-space class="drawer-space " direction="vertical" fill>
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
            span="12"
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
    />
  </a-drawer>
</template>

<script lang="ts" setup>
  import {ref} from "vue";
  import { useUserStore } from '@/store';
  import {
    querySubscribedDatasets,
    querySubscribedModels,
    SubscribedDatasetRecord,
    SubscribedModelRecord
  } from "@/api/user-center";
  import {Pagination} from "@/types/global";
  import CardWrap from "./components/card-wrap.vue";
  import UserInfoHeader from './components/user-info-header.vue';
  import SubscribedList from './components/subscribed-list.vue';
  import LatestActivity from './components/latest-activity.vue';
  import LatestNotification from "./components/latest-notification.vue";

  const userInfo = useUserStore();
  const visible = ref(false);
  const subscribedDataList = ref<SubscribedModelRecord[] | SubscribedDatasetRecord[]>([]);
  const showingDataType = ref(1);
  const toUpdate = ref(false);
  const totalDataNum = ref();
  const currentPage = ref(1);
  const pageSize = ref(8);
  const searchContent = ref('');

  const fetchData = async ()=> {
    if(showingDataType.value === 1){
      subscribedDataList.value = await querySubscribedModels(parseInt(userInfo.accountId!, 10));
    }
    else{
      subscribedDataList.value = await querySubscribedDatasets(parseInt(userInfo.accountId!, 10));
    }
  }

  const handleShowMore = (type: number) => {
    showingDataType.value = type;
    fetchData().then(() => {
      totalDataNum.value = subscribedDataList.value.length;
      subscribedDataList.value = subscribedDataList.value.slice(0, pageSize.value);
      searchContent.value = '';
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

    const drawerInput = document.querySelector('.drawer-space > .arco-space-item');
    if (drawerInput) {
      drawerInput.style.display = 'flex';
      drawerInput.style.alignItems = 'center';
      drawerInput.style.justifyContent = 'center';
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
