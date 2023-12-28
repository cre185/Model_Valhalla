<template>
  <a-row style="justify-content:center; align-items: center">
    <a-col :span="6">
        <a-space direction="horizontal">
          <p style="margin-left: 10px">{{ $t('ranking.adversarial.selector.model')}}</p>
          <a-select :style="{width:'150px'}" :placeholder="$t('ranking.adversarial.selector.model.placeholder')"
                    v-model="modelSelected" :allow-search="{ retainInputValue: true }" @change="handleSearch">
            <a-option :value="''">
              {{$t('ranking.adversarial.selector.model.all')}}
            </a-option>
            <a-option v-for="(item, index) in modelOptions" :key="index" :value="item.toString()" >
              {{item}}
            </a-option>
          </a-select>
        </a-space>
    </a-col>
    <a-col span="12">
      <a-space direction="horizontal">
        <p>{{ $t('ranking.adversarial.selector.time')}}</p>
        <a-range-picker
            showTime
            format="YYYY/MM/DD HH:mm:ss"
            value-format="YYYY-MM-DDTHH:mm:ss"
            :time-picker-props="{ defaultValue:['00:00:00','00:00:00']}"
            :placeholder="[$t('ranking.adversarial.selector.time.lowerBound'), $t('ranking.adversarial.selector.time.upperBound')]"
            @change="handlePick"
            style=" width: 380px;"
        />
      </a-space>
    </a-col>
    <a-col span="6">
      <a-space direction="horizontal">
        <p>{{ $t('ranking.adversarial.selector.result')}}</p>
      </a-space>
      <a-button :size="'mini'" :shape="'round'" :type="buttonStatus[2] ? 'primary' : 'outline'" @click="handleClick(2)" style="margin-left: 10px">
        {{ $t('ranking.adversarial.selector.result.win')}}
      </a-button>
      <a-button :size="'mini'" :shape="'round'" :type="buttonStatus[0] ? 'primary' : 'outline'" @click="handleClick(0)">
        {{ $t('ranking.adversarial.selector.result.lost')}}
      </a-button>
      <a-button :size="'mini'" :shape="'round'" :type="buttonStatus[1] ? 'primary' : 'outline'" @click="handleClick(1)">
        {{ $t('ranking.adversarial.selector.result.draw')}}
      </a-button>
    </a-col>
  </a-row>
  <a-table
      row-key="id"
      :pagination="pagination"
      :columns="columns as Column[]"
      :data="renderData"
      :bordered="false"
      :expandable="expandable"
      style="margin-top: 20px"
  >
    <template #testUser="{ record }">
      <a-space direction="horizontal">
        <a-avatar><img :src="record.testUserAvatar"/></a-avatar>
        <p>{{record.testUsername}}</p>
      </a-space>
    </template>
    <template #result="{ record }">
      <icon-check v-if="record.result === 1"/>
      <icon-minus v-if="record.result === 0"/>
      <icon-close v-if="record.result === -1"/>
    </template>
  </a-table>
</template>

<script lang="tsx" setup>
import {computed, ref, reactive, h, defineSlots, watch, nextTick, onMounted, VNode, defineProps} from 'vue';
  import {useI18n} from "vue-i18n";
  import {TableColumnData, TableData, TableExpandable} from "@arco-design/web-vue/es/table/interface";
import {
  BattleRecordsData,
  BattleRecords,
  GetModelInfo,
  QuestionAndAnswer,
  queryLLMBattleRecords,
  queryDatasetbehaviorList
} from "@/api/model-list";
  import {Select, Option, Empty} from "@arco-design/web-vue";
  import {getAvatar, getUsername} from "@/api/user-info";
  import cloneDeep from "lodash/cloneDeep";
  import {reduce} from "lodash";

  type Column = TableColumnData & { checked?: true };

  const { t } = useI18n();
  const props = defineProps({
    modelID: {
      type: String,
    }
  })
  const columns = computed<TableColumnData[]>( ()=> [
    {
      title: t('ranking.adversarial.selector.title.user'),
      dataIndex: 'testUser',
      slotName: 'testUser',
      align: "center",
      headerCellStyle: {backgroundColor: '#1c61ff', color: "white", fontSize: "16px", fontWeight: "550"},
      cellStyle: {height: "50px"},
    },
    {
      title: t('ranking.adversarial.selector.title.model'),
      dataIndex: 'adversarialModel',
      slotName: 'adversarialModel',
      align: "center",
      headerCellStyle: {backgroundColor: '#1c61ff', color: "white", fontSize: "16px", fontWeight: "550"},
      cellStyle: {height: "50px"},
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('ranking.adversarial.selector.title.time'),
      dataIndex: 'battleTime',
      slotName: 'battleTime',
      align: "center",
      headerCellStyle: {backgroundColor: '#1c61ff', color: "white", fontSize: "16px", fontWeight: "550"},
      cellStyle: {height: "50px"},
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('ranking.adversarial.selector.title.result'),
      dataIndex: 'result',
      slotName: 'result',
      align: "center",
      headerCellStyle: {backgroundColor: '#1c61ff', color: "white", fontSize: "16px", fontWeight: "550"},
      cellStyle: {height: "50px"},
    },
  ]);
  const battleHistory = ref<BattleRecords[]>([]);
  const originalData = ref<BattleRecordsData[]>([]);
  const renderData = ref<BattleRecordsData[]>([]);
  const buttonStatus = ref<boolean[]>([false, false, false]);
  const modelOptions = ref<string[]>([]);
  const modelSelected = ref('');
  const dateRange = ref<Date[]>([]);
  const pagination = reactive({
    total: renderData.value.length,
    showTotal: true,
    showJumper: true,
    showPageSize: true,
  });
  const expandable = reactive({
    title: t('ranking.adversarial.selector.title.details'),
    width: 150,
    expandedRowRender: (record: TableData) => {
      function DetailsContent({ currentRecord }: TableData){
        return  (currentRecord.displayRound >= 0) ?
              <div style={{display: 'flex', alignItems: 'center'}}>
                <div style={{margin: '10px 30px 20px 30px'}}>
                  <p style={{color: '#1989fa'}}>{t('ranking.adversarial.detail.question')}</p>
                  <div style={{position: 'relative', padding: '15px 20px',width: '250px', background: 'white', minHeight: '50px',
                    boxShadow: '5px 5px 10px rgba(0, 0, 0, 0.3)'}}>
                    {record.QA[currentRecord.displayRound].question}
                    <div style={{position: 'absolute', top: '100%', left: '0px', borderTop: '10px solid white',
                      borderLeft: '10px solid white', borderBottom: '10px solid transparent', borderRight: '10px solid transparent'}}>
                    </div>
                  </div>
                </div>
                <div style={{margin: '10px 0 20px 0', padding: '0 30px', borderRight: '1px solid white'}}>
                  <p style={{color: '#1989fa'}}>{t('ranking.adversarial.detail.reply.this')}</p>
                  <div style={{position: 'relative', padding: '15px 20px',width: '250px', color:'white', background: '#1989fa', minHeight: '100px',
                    boxShadow: '5px 5px 10px rgba(0, 0, 0, 0.3)'}}>
                    {record.QA[currentRecord.displayRound].answerA}
                    <div style={{position: 'absolute', top: '100%', left: '0px', borderTop: '10px solid #1989fa',
                      borderLeft: '10px solid #1989fa', borderBottom: '10px solid transparent', borderRight: '10px solid transparent'}}>
                    </div>
                  </div>
                </div>
                <div style={{width: '1px', height: '100%', border: '1px solid white'}}/>
                <div style={{margin: '10px 30px 20px 30px'}}>
                  <p style={{color: '#1989fa'}}>{t('ranking.adversarial.detail.reply.opposite')}</p>
                  <div style={{position: 'relative', padding: '15px 20px', width: '250px',color: 'white', background: '#1989fa', minHeight: '100px',
                    boxShadow: '5px 5px 10px rgba(0, 0, 0, 0.3)'}}>
                    {record.QA[currentRecord.displayRound].answerB}
                    <div style={{position: 'absolute', top: '100%', left: 'calc(100% - 20px)', borderTop: '10px solid #1989fa',
                      borderRight: '10px solid #1989fa', borderBottom: '10px solid transparent', borderLeft: '10px solid transparent'}}>
                    </div>
                  </div>
                </div>
              </div>
              :
              <Empty/>
      }
      return <div>
        <div style={{display: 'flex', alignItems: 'center', flexDirection: 'row', paddingLeft: '83%', paddingBottom: '5px',
          borderBottom: '1px solid white'}}>
          <p style={{color: '#1989fa'}}>{t('ranking.adversarial.detail.round')}</p>
          <Select defaultValue={record.displayRound} modelValue={record.displayRound}
                  onChange={(event) => {record.displayRound = event;}}
                  style={{ width: '65px', marginLeft: '20px' }}>
            {record.QA.map((QARound: QuestionAndAnswer, index: number) => (
                <Option value={index}>{index + 1}</Option>
            ))}
          </Select>
        </div>
        <DetailsContent currentRecord={record}/>
      </div>
    }
  });

  const fetchData = async (id: any) => {
    if(id === ''){
      return
    }
    battleHistory.value = await queryLLMBattleRecords(id);
    originalData.value = [];

    originalData.value = battleHistory.value.data.map(async (data) => {
      const adversarialModel =
          (data.llm1 === parseInt(id, 10))
              ? (await GetModelInfo(data.llm2)).name
              : (await GetModelInfo(data.llm1)).name;

      const QA = (data.llm1 === parseInt(id, 10)) ?
          data.result : data.result.map(async (qa: QuestionAndAnswer) => {
            const { answerA, answerB, ...rest } = data;
            const newItem = {
              ...rest,
              answerA: answerB,
              answerB: answerA,
            };
            return newItem;
          })
      if(!(modelOptions.value.includes(adversarialModel))){
        modelOptions.value.push(adversarialModel);
      }
      const newItem = {
        id: data.id,
        testUser: data.user_id,
        testUsername: await getUsername(data.user_id),
        testUserAvatar: await getAvatar(data.user_id),
        adversarialModel,
        battleTime: data.add_time,
        result: (data.llm1 === parseInt(id, 10)) ? data.winner : -data.winner,
        QA: data.result,
        displayRound: data.result.length > 0 ? 0 : -1,
      };

      return newItem;
    });
    originalData.value = await Promise.all(originalData.value);
    renderData.value = cloneDeep(originalData.value);
    pagination.total = renderData.value.length;
  }

  const handleSearch = () => {
    renderData.value = [];
    let selected = 3;
    for(let i = 0; i < 3; i+= 1) {
      if (buttonStatus.value[i] === true) {
        selected = i;
      }
    }
    for(let i = 0; i < originalData.value.length; i += 1){
      const date = new Date(originalData.value[i].battleTime);
      if(originalData.value[i].adversarialModel.includes(modelSelected.value) &&
          ( (date >= dateRange.value[0] && date <= dateRange.value[1]) ||
              dateRange.value[0] === undefined )&&
          ( originalData.value[i].result === selected - 1 || selected === 3 )
      ){
        renderData.value.push(originalData.value[i]);
      }
    }
    pagination.total = renderData.value.length;
  }

  const handleClick = (index: number) => {
    if(buttonStatus.value[index] === false){
      for(let i = 0; i < 3; i += 1){
        if(i !== index){
          buttonStatus.value[i] = false;
        }
      }
      buttonStatus.value[index] = true;
    }
    else {
      buttonStatus.value[index] = false;
    }
    if(!buttonStatus.value[0] && !buttonStatus.value[1] && !buttonStatus.value[2]){
      renderData.value = cloneDeep(originalData.value);
      return;
    }
    handleSearch();
  };

  const handlePick = (event: any) => {
    dateRange.value = [];
    if(event === undefined){
      renderData.value = cloneDeep(originalData.value);
      return;
    }
    dateRange.value.push(new Date(event[0]));
    dateRange.value.push(new Date(event[1]));
    handleSearch();
  }

  onMounted(() => {
    const tHead = document.getElementsByClassName('arco-table-th arco-table-operation');
    tHead[0].style.background = '#1c61ff';
    tHead[0].style.color = "white";
    tHead[0].style.fontSize = "16px";
    tHead[0].style.fontWeight = "550";
  })

  watch(
      () => props.modelID,

      async (newModelid, oldModelid) => {
        try {
          await fetchData(newModelid);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
      {
        immediate: true
      }
  );
</script>

<style lang="less" scoped>
  .arco-col .arco-btn{
    margin: auto 5px auto 5px;
  }
</style>
