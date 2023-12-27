<template>
  <a-space :direction="'horizontal'" :key="subscribed" :style="{visibility: content.name !== undefined ? 'visible' : 'hidden',
  alignItems: 'center', justifyContent: 'center', display: 'flex'}"
  >
    <a-card style="height: 16vh; width: 16vw;" :body-style="{display: 'flex', alignItems: 'center',
    justifyContent: 'center', height: '100%'}" class="clickable-card"
    >
      <a-skeleton v-if="loading" :loading="loading" :animation="true">
        <a-skeleton-line :rows="3" />
      </a-skeleton>
      <a-space v-else size="medium" direction="vertical" style="align-items: center; justify-content: center">
        <a-typography-text class="card-title" v-if="content.name!==undefined" bold>{{ content.name }}</a-typography-text>
        <a-typography-text class="card-title" v-else>{{ 'placeholder' }} </a-typography-text>
        <a-typography-text class="card-content" v-if="content.name===undefined">{{ ' placeholder' }}</a-typography-text>
        <a-typography-text class="card-content" v-else-if="contentType==='llm'" type="secondary">
          {{ `${$t('userInfo.subscribedModel.ranking')} ${content.ranking}
            ${$t('userInfo.subscribedModel.ranking.suffix')}` }}
        </a-typography-text>
        <a-typography-text class="card-content" v-else type="secondary">
          {{ content.domain }}
        </a-typography-text>
      </a-space>
    </a-card>
    <a-button v-if="subscribed"
              type="secondary"
              size="large"
              style="margin-left: 1vw; font-size: 1.5vh; font-weight: bolder; padding: 1vh 1vw"
              @click="handleSubscribe"
    >
      {{ $t('userInfo.subscription.card.subscribed.btn') }}
    </a-button>
    <a-button v-else
              size="large"
              style="margin-left: 1vw; font-size: 1.5vh; font-weight: bolder; padding: 1vh 1vw"
              @click="handleSubscribe"
    >
      {{ $t('userInfo.subscription.card.subscribe.btn') }}
    </a-button>
  </a-space>
</template>

<script setup lang="ts">
  import { ref } from "vue";
  import {isLLMSubscribed, subscribeLLM} from "@/api/model-list";
  import {isDatasetSubscribed, subscribeDataset} from "@/api/dataset";
  import { SubscribedModelRecord, SubscribedDatasetRecord } from "@/api/user-center";

  const props = defineProps({
    contentType: {
      type: String,
    },
    ID: {
      type: Number,
    },
    userID: {
      type: Number,
    },
    content: {
      type: Object as () => SubscribedModelRecord | SubscribedDatasetRecord,
    },
  });
  const subscribed = ref<boolean>(true);

  const handleSubscribe = () => {
    if(props.contentType === 'llm'){
      subscribeLLM(props.ID!);
    }
    else {
      subscribeDataset(props.ID!);
    }
    subscribed.value = !subscribed.value;
  };
</script>

<style scoped>
  .card-title{
    font-size: 2vh;
  }

  .card-content{
    font-size: 1.4vh;
  }

  .clickable-card:hover{
    background: lightgrey;
  }

</style>
