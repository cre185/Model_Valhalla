<template>
  <div class="container">
    <Breadcrumb :items="['menu.user', 'menu.user.setting']" />
    <a-row style="margin-bottom: 16px">
      <a-col :span="24">
        <UserPanel :name="newName" />
      </a-col>
    </a-row>
    <a-row class="wrapper">
      <a-col :span="24">
        <a-tabs default-active-key="1" type="rounded">
          <SecuritySettings @change-name="handleChange" />
        </a-tabs>
      </a-col>
    </a-row>
  </div>
</template>

<script lang="ts" setup>
  import { ref } from 'vue';
  import UserPanel from './components/user-panel.vue';
  import BasicInformation from './components/basic-information.vue';
  import SecuritySettings from './components/security-settings.vue';
  import Certification from './components/certification.vue';

  const newName = ref('');
  const handleChange = (username:string) => {
    newName.value = username;
  };
</script>

<script lang="ts">
  export default {
    name: 'Setting',
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }

  .wrapper {
    padding: 20px 0 0 20px;
    min-height: 580px;
    background-color: var(--color-bg-2);
    border-radius: 4px;
  }

  :deep(.section-title) {
    margin-top: 0;
    margin-bottom: 16px;
    font-size: 14px;
  }
</style>
