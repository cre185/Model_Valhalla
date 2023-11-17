<script setup lang="ts">
  const props = defineProps(['modelDescription', 'website', 'paper', 'license',
    'date', 'img', 'maxHeight']);
</script>

<template>
  <div class="container">
      <a-col :span="14" id="firstCol">
        <a-row id="row1">
          <img
              alt="模型logo"
              :src="props.img"
          />
        </a-row>
        <a-row  id="row2">
          <span>Released {{props.date}}</span>
        </a-row>
        <a-row  id="row3">
          <a-card :title="$t('ranking.profile.info.description')" :bordered="false">
            {{ props.modelDescription }}
          </a-card>
        </a-row>
      </a-col>
      <a-col :span="1" id="middleCol"><div id="separator"></div></a-col>
      <a-col :span="9" id="lastCol">
        <a-row  id="row4">
          <a-card :title="$t('ranking.profile.info.index')" :bordered="false">
            <a-link :href="props.website">{{ props.website }}</a-link>
          </a-card>
        </a-row>
        <a-row  id="row5">
          <a-card :title="$t('ranking.profile.info.paper')" :bordered="false">
            <a-list :bordered="false">
              <a-list-item v-for="(value, key) in props.paper" :key="key">
                <a-link :href="key as string">{{ value }}</a-link>
              </a-list-item>
            </a-list>
          </a-card>
        </a-row>
        <a-row  id="row6">
          <a-card :title="$t('ranking.profile.info.license')" :bordered="false">
            {{ props.license }}
          </a-card>
        </a-row>
      </a-col>
  </div>
</template>

<style scoped lang="less">
.container {
  display: flex;
  height: 100%;
}

#firstCol {
  display: flex;
  flex-direction: column;
}

#row1 {
  flex: 3;
  display: flex;
  border: 1px solid #ccc;
}

#row2 {
  flex: 1;
  display: flex;
  border: 1px solid #ccc;
}

#row3 {
  flex: 10;
  display: flex;
  border: 1px solid #ccc;
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