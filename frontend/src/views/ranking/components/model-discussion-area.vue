<template>
  <!-- 全局评论 -->
  <div style="display: flex; justify-content: center;">
    <span>6</span>
    <a-comment
        id="globalComment"
        align="right"
        :avatar="userStore.avatar"
    >
      <template #actions>
        <a-button key="0" type="primary" @click="handleGlobalAdd"> {{ $t('ranking.profile.discussion.submit') }} </a-button>
      </template>
      <template #content>
        <a-input :placeholder="$t('ranking.profile.discussion.reply.placeholder')" v-model="globalComment.content" />
      </template>
    </a-comment>
  </div>
  <!-- 评论区 -->
  <a-comment
      v-for="(item, index) in props.commentDetails"
      :key="index"
      :author="item.author"
      :avatar="item.avatar"
      :content="item.content"
      :datetime="item.datetime"
  >
    <template #actions>
      <span class="action" key="heart" @click="item.changeLikeState()">
        <span v-if="item.ifLike">
          <IconThumbUpFill :style="{ color: '#1c61ff' }" />
        </span>
        <span v-else>
          <IconThumbUp class="icon" />
        </span>
        {{ item.like }}
      </span>
      <span class="action" key="star" @click="item.changeHateState()">
        <span v-if="item.ifHate">
          <IconThumbDownFill :style="{ color: '#1c61ff' }" />
        </span>
        <span v-else>
          <IconThumbDown class="icon" />
        </span>
      </span>
      <span class="action, reply" key="reply" @click="handleClick(item, -1, index, '')">
        {{ $t('ranking.profile.discussion.reply') }}
      </span>
    </template>
    <a-comment
      v-for="(child, child_index) in item.children"
      :key="child_index"
      :author="child.author"
      :avatar="child.avatar"
      :content="child.content"
      :datetime="child.datetime"
    >
      <template #actions>
        <span class="action" key="heart" @click="child.changeLikeState()">
          <span v-if="child.ifLike">
            <IconThumbUpFill :style="{ color: '#1c61ff' }" />
          </span>
          <span v-else>
            <IconThumbUp class="icon" />
          </span>
          {{ child.like }}
        </span>
        <span class="action" key="star" @click="child.changeHateState()">
          <span v-if="child.ifHate">
            <IconThumbDownFill :style="{ color: '#1c61ff' }" />
          </span>
          <span v-else>
            <IconThumbDown class="icon" />
          </span>
        </span>
        <span class="action, reply" key="reply" @click="handleClick(item, child_index as number, index, child.author)">
          {{ $t('ranking.profile.discussion.reply') }}
        </span>
      </template>
    </a-comment>
    <a-comment
        v-if="item.ifReply"
        align="right"
        :avatar="userStore.avatar"
    >
      <template #actions>
        <a-button key="0" type="primary" @click="item.addComment(item, tmpComment)"> {{ $t('ranking.profile.discussion.submit') }} </a-button>
      </template>
      <template #content>
        <a-input :placeholder="$t('ranking.profile.discussion.replyEmbed.placeholder')+(item.lastClicked == -1 ? item.author : item.children[item.lastClicked].author)" v-model="tmpComment.content" />
      </template>
    </a-comment>
  </a-comment>
</template>

<script lang="ts" setup>
  import MyComment from '@/api/comment'
  import { useUserStore } from '@/store';

  const userStore = useUserStore();
  userStore.setInfo(JSON.parse(localStorage.getItem('userStore')!));
  const props = defineProps({
    commentDetails: Array<MyComment>
  })
  const tmpComment = new MyComment(userStore.username!, '', userStore.avatar!, '', '', 0, false, false, false, []);
  const globalComment = new MyComment(userStore.username!, '', userStore.avatar!, '', '', 0, false, false, false, []);

  const whoClicked = [];
  for (let i = 0; i < props.commentDetails!.length; i+=1) {
    whoClicked.push(props.commentDetails![i].ifReply);
  }

  const ensureOneReply = (currentReply:number) => {
    for (let i = 0; i < props.commentDetails!.length; i+=1) {
      if (i !== currentReply) {
        props.commentDetails![i].ifReply = false;
      }
    }
  }

  const handleClick = (item:MyComment, who:number, index:number, target:string) => {
    tmpComment.toAuthor = target;
    item.changeReplyState(tmpComment, who);
    ensureOneReply(index)
  }

  const handleGlobalAdd = () => {
    const tmp = new MyComment(userStore.username!, '', userStore.avatar!, '', '', 0, false, false, false, []);
    const date = new Date();
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    tmp.datetime = `${year}-${month}-${day} ${hours}:${minutes}`;
    tmp.content = globalComment.content;
    props.commentDetails!.push(tmp);
    globalComment.content = '';
  }
</script>

<style scoped>
  #globalComment {
    width: 100%;
  }
  .action {
    display: inline-block;
    padding: 0 4px;
    color: var(--color-text-1);
    line-height: 24px;
    background: transparent;
    border-radius: 2px;
    cursor: pointer;
    transition: all 0.1s ease;
  }
  .action:hover {
    background: var(--color-fill-3);
  }
  .icon:hover {
    color: #1c61ff;
  }
  .reply {
    color: black;
  }
  .reply:hover {
    color: #1c61ff;
  }
</style>