<template>
  <div class="container">
    <Breadcrumb :items="['menu.user', 'menu.user.info']" />
    <UserInfoHeader />
    <div class="content">
      <!-- <div class="content-left">
        <a-grid :cols="24" :col-gap="16" :row-gap="16">
          <a-grid-item :span="24">
            <MyProject />
          </a-grid-item>
          <a-grid-item :span="24">
            <LatestActivity />
          </a-grid-item>
        </a-grid>
      </div>
      <div class="content-right">
        <a-grid :cols="24" :row-gap="16">
          <a-grid-item :span="24">
            <MyTeam />
          </a-grid-item>
          <a-grid-item class="panel" :span="24">
            <LatestNotification />
          </a-grid-item>
        </a-grid>
      </div> -->
        <a-col class="content-top" :span="24">
          <a-grid :cols="2" :col-gap="16" :row-gap="16">
            <a-grid-item >
              <SubscribedModels :userID="userInfo.accountId"/>
            </a-grid-item>
            <a-grid-item >
              <LatestActivity />
            </a-grid-item>
          </a-grid>
        </a-col>
        <a-col class="content-bottom" :span="24">
          <a-grid :cols="24" :col-gap="16" :row-gap="16">
            <a-grid-item :span="12">
            </a-grid-item>
            <a-grid-item :span="12">
              <LatestActivity />
            </a-grid-item>
          </a-grid>
        </a-col>
    </div>
  </div>
</template>

<script lang="ts" setup>
  import {useStorage} from "@vueuse/core";
  import { useUserStore } from '@/store';
  import UserInfoHeader from './components/user-info-header.vue';
  import LatestNotification from './components/latest-notification.vue';
  import SubscribedModels from './components/subscribed-models.vue';
  import LatestActivity from './components/latest-activity.vue';

  const userInfo = useUserStore();
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

    /*&-left {
      flex: 1;
      margin-right: 16px;
      overflow: hidden;
      // background-color: var(--color-bg-2);

      :deep(.arco-tabs-nav-tab) {
        margin-left: 16px;
      }
    }

    &-right {
      width: 332px;
    }*/

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
