<script setup lang="ts">
  import axios from "axios";
  import apiCat from "@/api/main";
  import {defineEmits, nextTick, onMounted, onUnmounted, ref, watch} from "vue";
  import {updateDataset, updateDatasetTags} from "@/api/dataset";

  const props = defineProps(['datasetID', 'update', 'updateNow']);
  const description = ref('');
  const author = ref('');
  const domain = ref('');
  const tag = ref<string[]>([]);
  let oldFlag = false;

  const emit = defineEmits<{
    (event: 'changeTag'): void;
    (event: 'updateModify'): void;
  }>();

  onMounted(async () => {
    const response = await axios.get(apiCat(`/dataset/retrieve/${props.datasetID}`));
    const responseJson = response.data;
    description.value = responseJson.description;
    author.value = responseJson.author_name;
    domain.value = responseJson.domain;
    tag.value = responseJson.tag;
  });

  const inputRef = ref(null);
  const showInput = ref(false);
  const inputVal = ref('');

  const handleEdit = () => {
    showInput.value = true;

    nextTick(() => {
      if (inputRef.value) {
        inputRef.value.focus();
      }
    });
  };

  const handleAdd = async () => {
    if (inputVal.value) {
      if (!tag.value.includes(inputVal.value)) {
        tag.value.push(inputVal.value);
        await updateDatasetTags(props.datasetID, tag.value);
        emit('changeTag');
      }
      inputVal.value = '';
    }
    showInput.value = false;
  };

  const handleRemove = (key: any) => {
    tag.value = tag.value.filter((tags) => tags !== key);
  }

  const timerId = ref();
  timerId.value = setInterval(async () => {
    if (oldFlag !== props.update.edit) {
      if (oldFlag && !props.update.edit) {
        const data = {
          description: description.value,
          domain: domain.value,
          tag: tag.value,
        };
        await updateDataset(props.datasetID, data);
        emit('updateModify');
        emit('changeTag');
      }
      oldFlag = props.update.edit;
    }
  }, 500);

  onUnmounted(() => {
    clearInterval(timerId.value);
  });
</script>

<template>
  <div class="container">
      <a-col :span="14" id="firstCol">
        <a-row id="row1">
          <a-card :title="$t('dataset.introduction')" :bordered="false" id="datasetIntroduction">
            <span v-if="!props.updateNow">{{ description }}</span>
            <a-input v-else v-model="description" :placeholder="$t('dataset.details.modifyIntroduction')" allow-clear />
          </a-card>
        </a-row>
        <a-row  id="row2">
          <a-card :title="$t('dataset.author')" :bordered="false" id="datasetAuthor">
            <span>{{ author }}</span>
          </a-card>
        </a-row>
        <a-row  id="row3">
          <a-card :title="$t('dataset.domain')" :bordered="false" id="datasetDomain">
            <span v-if="!props.updateNow">{{ domain }}</span>
            <a-input v-else v-model="domain" :placeholder="$t('dataset.details.modifyDomain')" allow-clear />
          </a-card>
        </a-row>
      </a-col>
      <div id="separator"></div>
      <a-col :span="9" id="lastCol">
        <a-row  id="row4">
          <a-card :title="$t('dataset.tag')" :bordered="false">
            <a-space wrap>
              <a-tag
                  v-for="tagItem of tag"
                  :key="tagItem"
                  :closable="props.updateNow"
                  color="arcoblue"
                  class="tags"
                  @close="handleRemove(tagItem)"
              >
                {{ tagItem }}
              </a-tag>

              <a-input
                  v-if="showInput"
                  ref="inputRef"
                  :style="{ width: '90px'}"
                  size="mini"
                  v-model.trim="inputVal"
                  @keyup.enter="handleAdd"
                  @blur="handleAdd"
              />
              <a-tag
                  v-else
                  :style="{
        width: '90px',
        backgroundColor: 'var(--color-fill-2)',
        border: '1px dashed var(--color-fill-3)',
        cursor: 'pointer',
      }"
                  @click="handleEdit"
              >
                <template #icon>
                  <icon-plus />
                </template>
                {{ $t('searchDataset.tags.addTag') }}
              </a-tag>
            </a-space>
          </a-card>
        </a-row>
      </a-col>
  </div>
</template>

<style scoped lang="less">
.container {
  display: flex;
  height: 460px;
}

#firstCol {
  display: flex;
  flex-direction: column;
}

#row1 {
  flex: 3;
  display: flex;
}

#row2 {
  flex: 1;
  display: flex;
}

#modelTime{
  display: block;
  line-height: 50px;
  height: 50px;
  padding-left: 10px;
}

#row3 {
  flex: 10;
  display: flex;
}

#modelDescription {
  overflow: auto;
}

#middleCol {
  display: flex;
  align-content: center;
  justify-content: center;
}

#lastCol {
  display: flex;
  flex-direction: column;
}

#row4 {
  flex: 1;
  display: flex;
}

#row5 {
  flex: 2;
  display: flex;
}

#row6 {
  flex: 1;
  display: flex;
}

#separator {
  width: 1px;
  border-left: 1px dashed #ccc;
  height: 500px;
  margin-left: 10px;
  margin-right: 10px;
}

.tags {
  padding-left: 10px;
  padding-right: 10px;
  border-radius: 0 10px 10px 0;
}

</style>