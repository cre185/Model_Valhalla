<template>
  <a-card
    class="general-card"
    title="我们为您提供："
    :header-style="{ paddingBottom: '0' }"
    :body-style="{ padding: '15px 20px 13px 20px' }"
  >
    <a-row class="grid-demo">
      <a-col :span="5">
        <a-card
          id="card1"
          class="card"
          :body-style="{
            position: 'absolute',
            color: 'black',
            top: '50%',
            left: '20%',
            transform: 'translate(-10%,-50%)',
          }"
          :bordered="false"
        >
          方便的数据集操作
        </a-card>
      </a-col>
      <a-col :span="1"> </a-col>
      <a-col :span="5">
        <a-card
          id="card2"
          class="card"
          :body-style="{
            position: 'absolute',
            color: 'black',
            top: '50%',
            left: '20%',
            transform: 'translate(-10%,-50%)',
          }"
          :bordered="false"
        >
          清晰易查的排行榜
        </a-card>
      </a-col>
      <a-col :span="1"> </a-col>
      <a-col :span="5">
        <a-card
          id="card3"
          class="card"
          :body-style="{
            position: 'absolute',
            color: 'black',
            top: '50%',
            left: '10%',
            transform: 'translate(0%,-50%)',
          }"
          :bordered="false"
        >
          严谨合理的模型测试
        </a-card>
      </a-col>
      <a-col :span="1"> </a-col>
      <a-col :span="5">
        <a-card
          id="card4"
          class="card"
          :body-style="{
            position: 'absolute',
            color: 'black',
            top: '50%',
            left: '30%',
            transform: 'translate(-20%,-50%)',
          }"
          :bordered="false"
        >
          安全的用户管理
        </a-card>
      </a-col>
    </a-row>
  </a-card>
</template>

<script lang="ts" setup></script>

<style scoped lang="less">
  .general-card {
    height: 235px;
  }
  .card {
    height: 150px;
    font-size: 20px;
    transform: translateX(10%);
  }
  #card1 {
    background-color: #f2f9fe;
    border-radius: 20px 20px 20px 20px;
  }
  #card2 {
    background-color: #f5fef2;
    border-radius: 20px 20px 20px 20px;
  }
  #card3 {
    background-color: #fffaf3;
    border-radius: 20px 20px 20px 20px;
  }
  #card4 {
    background-color: #f6f6ff;
    border-radius: 20px 20px 20px 20px;
  }
</style>
