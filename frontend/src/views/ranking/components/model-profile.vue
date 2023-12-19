<script setup lang="ts">
  import axios from "axios";
  import apiCat from "@/api/main";
  import { onMounted, ref } from "vue";

  const props = defineProps(['modelID']);
  const logo = ref('');
  const releasedTime = ref('');
  const description = ref('');
  const website = ref('');
  const license = ref('');
  const paper = ref('');
  const paperLink = ref('');

  onMounted(async () => {
    try {
      const response = await axios.get(apiCat(`/testing/retrieve/${props.modelID}`));
      const responseJson = response.data;
      logo.value = responseJson.logo;
      releasedTime.value = responseJson.released_time;
      description.value = responseJson.description;
      website.value = responseJson.official_website;
      license.value = responseJson.license;
      paper.value = responseJson.document_name;
      paperLink.value = responseJson.document_website;
    } catch (error) {
      console.error(error);
    }
  });
</script>

<template>
  <div class="container">
      <a-col :span="14" id="firstCol">
        <a-row id="row1">
          <img
              alt="模型logo"
              :src="logo"
              :style="{ maxWidth:'100%', maxHeight: '200px' }"
          />
        </a-row>
        <a-row  id="row2">
          <span id="modelTime">Released {{ releasedTime }}</span>
        </a-row>
        <a-row  id="row3">
          <a-card :title="$t('ranking.profile.info.description')" :bordered="false" id="modelDescription">
            {{ description }}
          </a-card>
        </a-row>
      </a-col>
      <a-col :span="1" id="middleCol"><div id="separator"></div></a-col>
      <a-col :span="9" id="lastCol">
        <a-row  id="row4">
          <a-card :title="$t('ranking.profile.info.index')" :bordered="false">
            <a-link :href="website">{{ website }}</a-link>
          </a-card>
        </a-row>
        <a-row  id="row5">
          <a-card :title="$t('ranking.profile.info.paper')" :bordered="false">
            <a-link :href="paperLink">{{ paper }}</a-link>
          </a-card>
        </a-row>
        <a-row  id="row6">
          <a-card :title="$t('ranking.profile.info.license')" :bordered="false">
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
  border: 1px solid #ccc;
  align-items: center;
  justify-content: center;
}

#row2 {
  flex: 1;
  display: flex;
  border: 1px solid #ccc;
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
  border: 1px solid #ccc;
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
  border: 1px solid #ccc;
}

#row5 {
  flex: 2;
  display: flex;
  border: 1px solid #ccc;
}

#row6 {
  flex: 1;
  display: flex;
  border: 1px solid #ccc;
}

#separator {
  width: 1px;
  background-color: #ccc;
}

</style>
