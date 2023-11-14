<template>
  <a-card
    id="bottom"
    :body-style="{
      position: 'absolute',
      color: 'black',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%,-50%)',
    }"
  >
    模型竞技场，帮您选择最合适的LLM
  </a-card>
</template>

<script>
  import '@/assets/font/font.css';
</script>

<style lang="less" scoped>
  #bottom {
    height: 110px;
    font-size: 20px;
    text-align: center;
    font-family: DouYin;
  }
</style>
