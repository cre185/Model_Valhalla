<script setup lang="ts">
  import axios from "axios";
  import apiCat from "@/api/main";
  import {defineEmits, nextTick, onMounted, ref} from "vue";
  import {updateDatasetTags} from "@/api/dataset";

  const props = defineProps(['datasetID', 'modify']);
  const description = ref('');
  const author = ref('');
  const domain = ref('');
  const tag = ref<string[]>([]);
  const license = ref('');

  const emit = defineEmits<{
    (event: 'changeTag'): void;
  }>();

  onMounted(async () => {
    try {
      const response = await axios.get(apiCat(`/dataset/retrieve/${props.datasetID}`));
      const responseJson = response.data;
      description.value = responseJson.description;
      author.value = responseJson.author;
      domain.value = responseJson.domain;
      tag.value = responseJson.tag;
      license.value = responseJson.license;
    } catch (error) {
      console.error(error);
    }
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

</script>

<template>
  <div class="container">
      <a-col :span="14" id="firstCol">
        <a-row id="row1">
          <a-card :title="$t('dataset.introduction')" :bordered="false" id="datasetIntroduction">
            <span v-if="!props.modify">{{ description }}</span>
            <a-input v-else :default-value="description" :placeholder="$t('dataset.details.modifyIntroduction')" allow-clear />
          </a-card>
        </a-row>
        <a-row  id="row2">
          <a-card :title="$t('dataset.author')" :bordered="false" id="datasetAuthor">
            <span v-if="!props.modify">{{ author }}</span>
            <a-input v-else :default-value="author" :placeholder="$t('dataset.details.modifyAuthor')" allow-clear />
          </a-card>
        </a-row>
        <a-row  id="row3">
          <a-card :title="$t('dataset.domain')" :bordered="false" id="datasetDomain">
            <span v-if="!props.modify">{{ domain }}</span>
            <a-input v-else :default-value="domain" :placeholder="$t('dataset.details.modifyDomain')" allow-clear />
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
                  :closable="props.modify"
                  color="arcoblue"
                  class="tags"
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
        <a-row  id="row5">
          <a-card :title="$t('dataset.license')" :bordered="false">
            <span v-if="!props.modify">{{ license }}</span>
            <a-input v-else :default-value="license" :placeholder="$t('dataset.details.modifyLicense')" allow-clear />
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