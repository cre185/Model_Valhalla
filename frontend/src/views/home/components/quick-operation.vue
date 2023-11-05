<template>
  <a-card :body-style="{ padding: '15px 20px 13px 20px' }">
    <a-row class="grid-demo">
      <a-col :span="12">
        <a-row>
          <a-card
            id="card1"
            :body-style="{
              color: 'black',
              height: '200px',
            }"
            :bordered="false"
          >
            欢迎使用<br />
            模型竞技场<br />Model Valhalla!</a-card
          >
        </a-row>
        <a-row>
          <a-row>
            <a-card id="card2" :bordered="false">
              这是一个值得信赖的开放大模型能力众测平台</a-card
            >
          </a-row>
        </a-row>
      </a-col>
      <a-col :span="12">
        <div id="img">
          <a-image width="550" src="/src/assets/valhalla.jpg" />
        </div>
      </a-col>
    </a-row>
  </a-card>
</template>

<script lang="ts" setup>
</script>

<style scoped lang="less">
  .grid-demo {
    height: 350px;
  }
  #card1 {
    font-size: 60px;
    font-weight: bold;
    font-family: SiYuan;
    transform: translate(10%, 0%);
    line-height: 1.5em;
  }
  #card2 {
    height: 50px;
    transform: translate(13%, 170%);
    font-size: 17px;
  }
  #img {
    position: absolute;
    transform: translate(10%, 5%);
  }
</style>
