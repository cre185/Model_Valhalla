<script setup lang="ts">
  import axios from "axios";
  import apiCat from "@/api/main";
  import {nextTick, onMounted, ref} from "vue";

  const props = defineProps(['datasetID']);
  const description = ref('');
  const author = ref('');
  const domain = ref('');
  const tag = ref('');
  const license = ref('');

  onMounted(async () => {
    try {
      // const response = await axios.get(apiCat(`/dataset/retrieve/${props.datasetID}`));
      const response = await axios.get(apiCat(`/dataset/retrieve/1`));
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

  const tags = ref(['Tag 1', 'Tag 2', 'Tag 3']);
  const inputRef = ref(null);
  const showInput = ref(false);
  const inputVal = ref('');

  const handleEdit = () => {
    showInput.value = true;

    nextTick(() => {
      if (inputRef.value) {
        // inputRef.value.focus();
      }
    });
  };

  const handleAdd = () => {
    if (inputVal.value) {
      tags.value.push(inputVal.value);
      inputVal.value = '';
    }
    showInput.value = false;
  };

  const handleRemove = (key: string) => {
    tags.value = tags.value.filter((tagg) => tagg !== key);
  };

</script>

<template>
  <div class="container">
      <a-col :span="14" id="firstCol">
        <a-row id="row1">
          <a-card :title="$t('dataset.introduction')" :bordered="false" id="datasetIntroduction">
            {{ description }}
          </a-card>
        </a-row>
        <a-row  id="row2">
          <a-card :title="$t('dataset.author')" :bordered="false" id="datasetAuthor">
            {{ author }}
          </a-card>
        </a-row>
        <a-row  id="row3">
          <a-card :title="$t('dataset.domain')" :bordered="false" id="datasetDomain">
            {{ domain }}
          </a-card>
        </a-row>
      </a-col>
      <a-col :span="1" id="middleCol"><div id="separator"></div></a-col>
      <a-col :span="9" id="lastCol">
        <a-row  id="row4">
          <a-card :title="$t('dataset.tag')" :bordered="false">
            <a-space wrap>
              <a-tag
                  v-for="(tag, index) of tags"
                  :key="tag"
                  :closable="index !== 0"
                  @close="handleRemove(tag)"
              >
                {{ tag }}
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
                Add Tag
              </a-tag>
            </a-space>
          </a-card>
        </a-row>
        <a-row  id="row5">
          <a-card :title="$t('dataset.license')" :bordered="false">
            {{ license }}
          </a-card>
        </a-row>
      </a-col>
  </div>
</template>

<style scoped lang="less">
.container {
  display: flex;
  height: 515px;
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
  border: 1px dashed #ccc;
  background-color: transparent;
}

</style>