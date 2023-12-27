<template>
  <div class="demo-basic" style="background-color: white; width: 100%; height: 100%">
    <a-spin style="display: block" :loading="loading">
      <a-tabs v-model:activeKey="messageType" type="rounded" size="mini" destroy-on-hide>
        <a-tab-pane v-for="item in tabList" :key="item.key">
          <template #title>
            <span> {{ item.title }}{{ formatUnreadLength(item.key) }} </span>
          </template>
          <a-result v-if="!renderList.length" status="404" :style="{marginTop: size === 'small' ? '15%' : '18%'}">
            <template #subtitle> {{ $t('messageBox.noContent') }} </template>
          </a-result>
          <List :render-list="renderList" :unread-count="unreadCount" @item-click="handleItemClick" :size="props.size"/>
        </a-tab-pane>
        <template #extra>
          <a-button type="text" @click="checkMore" v-if="size==='small'">
            {{ $t('messageBox.viewMore') }}
          </a-button>
        </template>
      </a-tabs>
    </a-spin>
  </div>
</template>

<script setup lang="ts">
  import useLoading from "@/hooks/loading";
  import {computed, defineEmits, onMounted, reactive, ref, toRefs, watch} from "vue";
  import {getMessageData, MessageListType, setMessageStatus, userToDataset} from "@/api/message";
  import axios from "axios";
  import apiCat from "@/api/main";
  import {getToken} from "@/utils/auth";
  import {useI18n} from "vue-i18n";
  import {useRouter} from "vue-router";
  import List from "./list.vue";

  const { t } = useI18n();
  const props = defineProps(['currentLocale', 'size']);
  const emit = defineEmits<{
    (event: 'changeShowingStatus', arg: boolean): void;
  }>();
  const router = useRouter();
  interface TabItem {
    key: string;
    title: string;
    avatar?: string;
  }
  const { loading, setLoading } = useLoading(true);
  const messageType = ref('like');
  const messageData = reactive<{
    renderList: userToDataset[];
    messageList: userToDataset[];
  }>({
    renderList: [],
    messageList: [],
  });
  toRefs(messageData);
  const tabList: TabItem[] = [
    {
      key: 'like',
      title: t('messageBox.tab.title.one'),
    },
    {
      key: 'comment',
      title: t('messageBox.tab.title.two'),
    },
    {
      key: 'system',
      title: t('messageBox.tab.title.three'),
    },
  ];
  const renderList = computed(() => { // 创建一个过滤属性，只包含未读的消息列表，并设置显示四条
    const size = props.size === 'small' ? 4 : 3
    if (messageType.value === 'like') {
      return messageData.messageList.filter(
          (item) => item.msg_type === 'Like'
      ).slice(0, size).sort((a, b) => {
        if(a.read && !b.read){
          return -1;
        }
        return 1;
      });
    }
    if (messageType.value === 'comment') {
      return messageData.messageList.filter(
          (item) => item.msg_type === 'Reply'
      ).slice(0, size).sort((a, b) => {
        if(a.read && !b.read){
          return -1;
        }
        return 1;
      });
    }
    return messageData.messageList.filter(
        (item) => item.msg_type !== 'Reply' && item.msg_type !== 'Like'
    ).slice(0, size).sort((a, b) => {
      if(a.read && !b.read){
        return -1;
      }
      return 1;
    });
  });
  const unreadCount = computed(() => {
    return renderList.value.filter((item) => !item.read).length;
  });
  async function fetchSourceData() {
    setLoading(true);
    messageData.messageList = [] as userToDataset[];
    try {
      messageData.messageList = await getMessageData(props.currentLocale, t);
    } catch (err) {
      // you can report use errorHandler or other
    } finally {
      setLoading(false);
    }
  }
  async function readMessage(data: MessageListType) { // 提前msg_id设置为已读
    const ids = data.map((item) => item.msg_id);
    await setMessageStatus({ ids });
  }
  const getUnreadList = (type: string) => {
    const list = messageData.messageList.filter(
        (item) => item.msg_type === type && !item.read
    );
    return list;
  };
  const formatUnreadLength = (type: string) => {
    const list = getUnreadList(type);
    return list.length ? `(${list.length})` : ``;
  };
  const handleItemClick = (items: MessageListType) => {
    emit('changeShowingStatus', false);
    if (renderList.value.length) {
      readMessage([...items]);
    }
    axios.post(apiCat('/user/check_message'), { id: items[0].msg_id }, { // 点击后先设置消息已读
      headers: {
        Authorization: getToken()!,
      }
    })
    const routerType = items[0].msg_type;
    if (routerType === "Upload") // 设置反馈路由，目前仅调转页面，后续具体参数要沟通
    {
      let target;
      if ('targetID' in items[0].msg_content) {
        target = items[0].msg_content.targetID as string;
      }
      router.push({
        name: 'datasetDetails',
        params: { toShowDetailsID: target, toShowPanelIndex: 1 },
      });
    }
    else if (routerType === "Reply") // 设置回复评论路由
    {
      let target;
      if ('targetID' in items[0].msg_content) {
        target = items[0].msg_content.targetID as string;
      }
      if ('contentFlag' in items[0].msg_content && !items[0].msg_content.contentFlag) {
        router.push({
          name: 'datasetDetails',
          params: { toShowDetailsID: target, toShowPanelIndex: 4 },
        });
      }
      else {
        router.push({
          name: 'leaderboardDetails',
          params: { toShowDetailsID: target, toShowPanelIndex: 4 },
        });
      }
    }
    else if (routerType === "Like") {
      let target;
      if ('targetID' in items[0].msg_content) {
        target = items[0].msg_content.targetID as string;
      }
      if ('likeFlag' in items[0].msg_content && !items[0].msg_content.likeFlag) // 设置点赞信息路由
      {
        router.push({
          name: 'datasetDetails',
          params: { toShowDetailsID: target, toShowPanelIndex: 4 },
        });
      }
      else {
        router.push({
          name: 'leaderboardDetails',
          params: { toShowDetailsID: target, toShowPanelIndex: 4 },
        });
      }
    }
    else if (routerType === "Feedback") { // 设置反馈的路由
      if ('datasetID' in items[0].msg_content) {
        const datasetID = items[0].msg_content.datasetID as string;
        router.push({
          name: 'datasetDetails',
          params: { toShowDetailsID: datasetID, toShowPanelIndex: 1 },
        });
      }
    }
    else if (routerType === "Report") {
      if ('datasetID' in items[0].msg_content) {
        const datasetID = items[0].msg_content.datasetID as string;
        console.log(datasetID);
        router.push({
          name: 'datasetDetails',
          params: { toShowDetailsID: datasetID, toShowPanelIndex: 1 },
        });
      }
    }
  };
  const emptyList = () => {
    messageData.messageList = [];
  };

  const checkMore = () => {
    router.push({
      path: '/user/info',
    });
    emit("changeShowingStatus", false);
  }

  fetchSourceData();
</script>

<style scoped>
  :deep(.arco-popover-popup-content) {
    padding: 0;
  }

  :deep(.arco-list-item-meta) {
    align-items: flex-start;
  }

  :deep(.arco-tabs-nav) {
    padding: 14px 0 12px 16px;
    border-bottom: 1px solid var(--color-neutral-3);
  }

  :deep(.arco-tabs-content) {
    padding-top: 0;
  }

  #msgButton :hover {
    background-color: aliceblue
  }
</style>
