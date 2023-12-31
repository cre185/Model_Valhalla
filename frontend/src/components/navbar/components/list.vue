<template>
    <a-list :bordered="false" id="message-list">
      <a-list-item
        v-for="item in renderList"
        :key="item.msg_id"
        action-layout="vertical"
        :style="{
          opacity: item.read ? 0.5 : 1,
        }"
      >
        <template #extra>
          <a-tag v-if="item.read === false" color="gray">{{ $t('messageBox.message.unread') }}</a-tag>
          <a-tag v-else-if="item.read === true" color="green">{{ $t('messageBox.message.read') }}</a-tag>
        </template>
        <div class="item-wrap" @click="onItemClick(item)">
          <a-list-item-meta>
            <template v-if="item.avatar" #avatar>
              <a-avatar shape="circle">
                <img v-if="item.avatar" :src="item.avatar" />
                <icon-desktop v-else />
              </a-avatar>
            </template>
            <template #title>
              <a-space :size="4"
                       :direction="size === 'small' ? 'vertical' : 'horizontal'"
              >
                <span style="font-size: 90%">{{ item.msg_title }}</span>
                <a-typography-text type="secondary" :style="{fontSize: '80%'}"
                >
                  {{ item.add_time }}
                </a-typography-text>
              </a-space>
            </template>
            <template #description>
              <div>
                <a-typography-paragraph
                  :ellipsis="{
                    rows: 1,
                  }"
                  style="font-size: 90%;"
                  >{{ item.msg_text }}</a-typography-paragraph
                >
                <a-typography-text
                  v-if="item.msg_type === 'message'"
                  class="time-text"
                >
                  {{ item.add_time }}
                </a-typography-text>
              </div>
            </template>
          </a-list-item-meta>
        </div>
      </a-list-item>
      <div
        v-if="renderList.length && renderList.length < 3"
        :style="{ height: (showMax - renderList.length) * 86 + 'px' }"
      ></div>
    </a-list>
  </template>

  <script lang="ts" setup>
    import { PropType } from 'vue';
    import { userToDataset, MessageListType } from '@/api/message';
    import router from '@/router';

    const props = defineProps({
      renderList: {
        type: Array as PropType<MessageListType>,
        required: true,
      },
      unreadCount: {
        type: Number,
        default: 0,
      },
      size: {
        type: String,
        default: 'small',
      }
    });
    const emit = defineEmits(['itemClick']);
    const allRead = () => {
      emit('itemClick', [...props.renderList]);
    };
    const onItemClick = (item: userToDataset) => {
      emit('itemClick', [item]);
    };
    const showMax = 3;
  </script>

  <style scoped lang="less">
    :deep(.arco-list) {
      .arco-list-item {
        min-height: 86px;
        border-bottom: 1px solid rgb(var(--gray-3));
      }
      .arco-list-item-extra {
        position: absolute;
        right: 20px;
      }
      .arco-list-item-meta-content {
        flex: 1;
      }
      .item-wrap {
        cursor: pointer;
      }
      .time-text {
        font-size: 12px;
        color: rgb(var(--gray-6));
      }
      .arco-empty {
        display: none;
      }
      .arco-list-footer {
        padding: 0;
        height: 50px;
        line-height: 50px;
        border-top: none;
        .arco-space-item {
          width: 100%;
          border-right: 1px solid rgb(var(--gray-3));
          &:last-child {
            border-right: none;
          }
        }
        .add-border-top {
          border-top: 1px solid rgb(var(--gray-3));
        }
      }
      .footer-wrap {
        text-align: center;
      }
      .arco-typography {
        margin-bottom: 0;
      }
      .add-border {
        border-top: 1px solid rgb(var(--gray-3));
      }
    }
  </style>
