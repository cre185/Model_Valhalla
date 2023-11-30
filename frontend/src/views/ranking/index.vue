<template>
  <div>
    <div class="container">
      <Breadcrumb id="breadCrumb" :items="['menu.ranking', 'menu.ranking.profile']" />
          <div id="llm-rotatingGallery" style="z-index: 100;" >
            <div id="drag-container">
              <div id="spin-container">
                <img src="@/assets/images/llm_logos/ChatGPT_logo.png">
                <img src="@/assets/images/llm_logos/Claude_logo.png">
                <img src="@/assets/images/llm_logos/Claude2_logo.png">
                <img src="@/assets/images/llm_logos/Falcon_logo.png">
                <img src="@/assets/images/llm_logos/GPT-4_logo.png">
                <img src="@/assets/images/llm_logos/MetaLlama_logo.png">
                <img src="@/assets/images/llm_logos/Mistral-7b_logo.png">
                <img src="@/assets/images/llm_logos/Qwen-chat_logo.png">
                <img src="@/assets/images/llm_logos/Vicuna_logo.png">
                <img src="@/assets/images/llm_logos/Xinghuo_logo.png">
                <img src="@/assets/images/llm_logos/Yiyan_logo.png">
                <img src="@/assets/images/llm_logos/zephyr_logo.png">
                <img src="@/assets/images/llm_logos/MPT-7b_logo.png">
                <img src="@/assets/images/llm_logos/etc.png">
              </div>
              <div id="ground"></div>
            </div>
            <div id="slogan" style="display: flex; flex-direction: column; align-items: center; justify-content: center">
              <ul class="sloganContent"
                  style="font-size: 60px; margin-bottom: 20px; font-weight: 900; color: #1c61ff;"
              >
                <li class="sloganContentText" v-for="(char, index) in $t('ranking.welcome')" :key="index" :style="{'animation-delay': `${index * 100}ms`}">
                  {{ char }}
                </li>
              </ul>
              <ul class="sloganContent" style="margin: 0 auto 0 auto; font-size: 24px; color: black; ">
                <li class="sloganContentSubText" v-for="(char, index) in $t('ranking.slogan1')" :key="index" :style="{'animation-delay': `${index * 50}ms`}">
                  {{ char }}
                </li>
              </ul>
              <ul class="sloganContent" style="margin: 20px auto 0 auto; font-size: 24px; color: black;">
                <li class="sloganContentSubText" v-for="(char, index) in $t('ranking.slogan2')" :key="index" :style="{'animation-delay': `${index * 50}ms`}">
                  {{ char }}
                </li>
              </ul>
            </div>
          </div>
        <a id="startBtn" href="#">
          Get Started
        </a>
        <icon-double-down id="doubleDown" style="display: flex; margin: 50px auto auto auto; animation: upAndDown 3s cubic-bezier(.7,.3,.3,.7) infinite"/>
        <a-card class="general-card"
                style="height: 80vh; z-index: 0; margin-top: 20px; animation: upAndDown 3s cubic-bezier(.7,.3,.3,.7) infinite;"
                id="rankings"
        >
          <a-row style="margin-bottom: 16px">
            <a-col :span="6">
              <a-space>
                <a-button id="upload" type="primary" style="margin-top: 20px">
                  <template #icon>
                    <icon-plus />
                  </template>
                  {{ $t('ranking.llm.upload') }}
                </a-button>
              </a-space>
            </a-col>
            <a-col id="search" :span="12" style="display: flex; align-items:center; justify-content: center; margin-top: 20px">
              <a-input-search :style="{width:'600px'}" :placeholder="$t('ranking.llm.search.placeholder')" :loading="loading" @search="handleSearch" search-button/>
            </a-col>
            <a-col
                id="settings"
                :span="6"
                style="display: flex; align-items: center; justify-content: end; margin-top: 20px"
            >
              <a-button>
                <template #icon>
                  <icon-download />
                </template>
                {{ $t('searchTable.operation.download') }}
              </a-button >
              <a-tooltip :content="$t('searchTable.actions.refresh')">
                <div class="action-icon" @click="fetchData"
                ><icon-refresh size="18"
                /></div>
              </a-tooltip>
              <a-dropdown @select="handleSelectDensity">
                <a-tooltip :content="$t('searchTable.actions.density')">
                  <div class="action-icon"><icon-line-height size="18" /></div>
                </a-tooltip>
                <template #content>
                  <a-doption
                      v-for="item in densityList"
                      :key="item.value"
                      :value="item.value"
                      :class="{ active: item.value === size }"
                  >
                    <span>{{ item.name }}</span>
                  </a-doption>
                </template>
              </a-dropdown>
              <a-tooltip :content="$t('ranking.actions.setColumn')">
                <a-popover
                    trigger="click"
                    position="bl"
                    @popup-visible-change="popupVisibleChange"
                >
                  <div class="action-icon"><icon-settings size="18" /></div>
                  <template #content>
                    <div id="tableSetting">
                      <div
                          v-for="(item, index) in showColumns"
                          :key="item.dataIndex"
                          class="setting"
                      >
                        <div style="margin-right: 4px; cursor: move">
                          <icon-drag-arrow />
                        </div>
                        <div>
                          <a-checkbox
                              :value="inOriginalData(item)"
                              :disabled="inOriginalData(item)"
                              v-model="item.checked"
                              @change="handleChange($event, item as TableColumnData, index)"
                          >
                          </a-checkbox>
                        </div>
                        <div class="title">
                          <p>{{ item.title === '#' ? '序列号' : item.title }}</p>
                        </div>
                      </div>
                    </div>
                  </template>
                </a-popover>
              </a-tooltip>
            </a-col>
          </a-row>
          <a-table
              row-key="id"
              :loading="loading"
              :columns="(cloneColumns as TableColumnData[])"
              :data="renderData"
              :bordered="false"
              :size="size"
              :pagination="false"
          >
            <template #details="{ record }">
              <a-button type="text" size="small" @click="handleClick(record)">
                {{ $t('ranking.view.btn') }}
              </a-button>
            </template>
          </a-table>
        </a-card>
    </div>
    <a-drawer :width="1000"
              :visible="visible"
              :footer="false"
              @cancel="handleCancel"
              @open="setDrawer"
              unmountOnClose
              v-if="currentLLM !== undefined"
    >
      <template #title>
        <header class="drawer-model-title">
          <div class="drawer-model-title-text">
            <p>{{ currentLLM.name }}</p>
          </div>
          <a-button
              class="llm-details-subscribe-btn"
              type="primary"
              size="large"
          >
            <template #icon>
              <icon-star :size="30"/>
            </template>
            <p>{{ $t('rankings.llm.details.subscribe.btn') }}</p>
          </a-button>
          <div style="text-align: center; position: absolute; right: 20px; padding: 30px 20px 20px 0; border-right: 1px solid darkgray">
            <div style="font-size: 30px; color: darkgray; font-weight: 500">
              {{ $t('ranking.profile.ranking') }}
            </div>
            <div style="margin-top: 6px; font-size: 30px; color: darkgray; font-weight: 500">
              {{currentLLM.ranking}}
            </div>
          </div>
        </header>
      </template>
      <div>
        <a-tabs size="large">
          <a-tab-pane key="1" :title="$t('ranking.details.details')">
            <ModelProfile />
          </a-tab-pane>
          <a-tab-pane key="2" :title="$t('ranking.details.datasetScore')">
            <DatasetProfile :modelid="ModelID" />
          </a-tab-pane>
          <a-tab-pane key="3" :title="$t('ranking.details.competitionRecords')">
            <AdversarialRecords/>
          </a-tab-pane>
          <a-tab-pane key="4" :title="$t('ranking.details.discussions')">
            <ModelDiscussionArea :comment-details="commentDetails" :model-id=ModelID
                                 @change-comment="handleChangeComment" />
          </a-tab-pane>
        </a-tabs>
      </div>
    </a-drawer>
  </div>
</template>

<script lang="ts" setup>
  import {computed, ref, reactive, watch, nextTick, onMounted} from 'vue';
  import axios from "axios";
  import apiCat from "@/api/main";
  import {getToken} from "@/utils/auth";
  import { useI18n } from 'vue-i18n';
  import useLoading from '@/hooks/loading';
  import { queryPolicyList, PolicyRecord, PolicyParams } from '@/api/list';
  import {LLMRankingData, queryDatasetColumnList, queryLLMList} from "@/api/model-list";
  import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import Sortable from 'sortablejs';
  import cloneDeep from 'lodash/cloneDeep';
  import MyComment, {getComment, updateComment} from "@/api/comment";
  import ModelDiscussionArea from "./components/model-discussion-area.vue";
  import ModelProfile from './components/model-profile.vue';
  import DatasetProfile from './components/model-datasetbehavior.vue';
  import AdversarialRecords from './components/model-adversarial-records.vue';

  type SizeProps = 'mini' | 'small' | 'medium' | 'large';
  type Column = TableColumnData & { checked?: true };

  const visible = ref(false);

  const { loading, setLoading } = useLoading(false);
  const { t } = useI18n();
  const renderData = ref<LLMRankingData[]>();
  const currentColumns = ref<TableColumnData[]>();
  const cloneColumns = ref<Column[]>([]);
  const additionalColumns = ref<Column[]>(await queryDatasetColumnList());
  const showColumns = ref<Column[]>([]);
  const currentLLM = ref<LLMRankingData>();
  const ModelID = ref('');
  const ModelRanking = ref(0);

  const size = ref<SizeProps>('medium');

  const commentDetails = ref([] as MyComment[]);

  const jwt = getToken();

  const handleClick = (data: LLMRankingData) => {
    currentLLM.value = data;
    visible.value = true;
  };

  const handleCancel = () => {
    visible.value = false;
  }

  const densityList = computed(() => [
    {
      name: t('searchTable.size.mini'),
      value: 'mini',
    },
    {
      name: t('searchTable.size.small'),
      value: 'small',
    },
    {
      name: t('searchTable.size.medium'),
      value: 'medium',
    },
    {
      name: t('searchTable.size.large'),
      value: 'large',
    },
  ]);
  const originalColumns = computed<TableColumnData[]>(() => [
    {
      title: t('rankings.llm.data.ranking'),
      dataIndex: 'ranking',
      slotName: 'ranking',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('rankings.llm.data.name'),
      dataIndex: 'name',
      slotName: 'name',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('rankings.llm.data.datasetScore'),
      dataIndex: 'datasetScore',
      slotName: 'dataScore',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('rankings.llm.data.eloScore'),
      dataIndex: 'eloScore',
      slotName: 'eloScore',
      align: "center",
      sortable: {
        sortDirections: ['ascend', 'descend']
      },
    },
    {
      title: t('rankings.llm.data.details'),
      dataIndex: 'details',
      slotName: 'details',
      align: "center",
    },
    {
      title: t('rankings.llm.data.license'),
      dataIndex: 'license',
      slotName: 'license',
      align: "center",
    },
  ]);

  currentColumns.value = cloneDeep(originalColumns.value);
  for(let i = 0; i < additionalColumns.value.length; i += 1){
    currentColumns.value?.push(additionalColumns.value[i]);
  }
  const fetchData = async () => {
    setLoading(true);
    try {
      const { data } = await queryLLMList();
      renderData.value = data;
    } catch (err) {
      // you can report use errorHandler or other
    } finally {
      setLoading(false);
    }
  };

  const inOriginalData = (item: TableColumnData) => {
    for(let i = 0; i < originalColumns.value.length; i += 1){
      if (originalColumns.value[i].title === item.title){
        return true;
      }
    }
    return false;
  }
  fetchData();

  const handleSelectDensity = (
      val: string | number | Record<string, any> | undefined,
      e: Event
  ) => {
    size.value = val as SizeProps;
  };

  const handleChange = (
      checked: boolean | (string | boolean | number)[],
      column: Column,
      index: number
  ) => {
    if (!checked) {
      cloneColumns.value = cloneColumns.value.filter(
          (item) => item.dataIndex !== column.dataIndex
      );
    } else {
      cloneColumns.value.splice(index, 0, column);
    }
  };

  const exchangeArray = <T extends Array<any>>(
      array: T,
      beforeIdx: number,
      newIdx: number,
      isDeep = false
  ): T => {
    const newArray = isDeep ? cloneDeep(array) : array;
    if (beforeIdx > -1 && newIdx > -1) {
      // 先替换后面的，然后拿到替换的结果替换前面的
      newArray.splice(
          beforeIdx,
          1,
          newArray.splice(newIdx, 1, newArray[beforeIdx]).pop()
      );
    }
    return newArray;
  };

  watch(
      () => currentColumns.value,
      (val) => {
        if(val !== undefined){
          cloneColumns.value = cloneDeep(originalColumns.value);
          showColumns.value = cloneDeep(val);
          showColumns.value.forEach((item, index) => {
            if(inOriginalData(item))
              item.checked = true;
          });
        }
      },
      { deep: true, immediate: true }
  );

  const popupVisibleChange = (val: boolean) => {
    if (val) {
      nextTick(() => {
        const el = document.getElementById('tableSetting') as HTMLElement;
        const sortable = new Sortable(el, {
          onEnd(e: any) {
            const { oldIndex, newIndex } = e;
            exchangeArray(cloneColumns.value, oldIndex, newIndex);
            exchangeArray(showColumns.value, oldIndex, newIndex);
          },
        });
      });
    }
  };

  const handleSearch = async (modelName: string) => {
    setLoading(true);
    try {
      await fetchData();
      renderData.value = renderData.value?.filter(item => item.name.includes(modelName))
    } catch (err) {
      console.log('Search error');
    } finally {
      setLoading(false);
    }
  }

  const setDrawer = () => {
    // 设置Drawer样式
    const drawerHeader = document.querySelector('.arco-drawer-header');
    if (drawerHeader) {
      drawerHeader.style.height = '220px';
      drawerHeader.style.border = '0';
    }

    const drawerTitle = document.querySelector('.arco-drawer-title');
    if (drawerTitle) {
      drawerTitle.style.paddingLeft = '80px';
    }

    const drawerCloseBtn = document.querySelector('.arco-drawer-close-btn');
    if(drawerCloseBtn){
      drawerCloseBtn.style. visibility = 'hidden';
    }

    const starBtn = document.querySelector('.arco-icon-star');
    if(starBtn){
      starBtn.style.display = 'flex';
      starBtn.style.justifyContent = 'center';
      starBtn.style.alignItems = 'center';
    }

    const starFillBtn = document.querySelector('.arco-icon-star-fill');
    if(starFillBtn){
      starFillBtn.style.display = 'flex';
      starFillBtn.style.justifyContent = 'center';
      starFillBtn.style.alignItems = 'center';
    }

    const tabs = document.querySelectorAll('.arco-tabs-tab')
    if(tabs){
      for(let i = 0; i < tabs.length; i += 1){
        tabs[i].style.margin = '0 25px';
        tabs[i].style.fontSize = '15px';
      }
    }

    const firstTab = document.querySelector('.arco-tabs-tab:first-of-type')
    if(firstTab){
      firstTab.style.margin = '0 25px 0 60px';
    }

    ModelID.value=currentLLM.value!.id.toString();
    getComment(ModelID.value!, commentDetails, jwt!);
  };

  const handleChangeComment = async (index: number, content: MyComment) => {
    await updateComment(currentLLM.value!.id.toString()!, content, jwt!);
    if (index === -1) {
      commentDetails.value.push(content);
    } else {
      commentDetails.value[index].children.push(content);
    }
  };

  type listenerType = (event: Event) => void;
  const scrollAnimation = (listener: listenerType | null, clicked: boolean) => {
    const gallery = document.getElementById('llm-rotatingGallery');
    gallery!.style.transform = `translateX(${gallery!.offsetWidth * window.scrollY / 1000}px)`;
    if(window.scrollY >= 200 || clicked){
      if(!clicked){
        document.removeEventListener('wheel', listener)
      }
      const startBtn = document.getElementById('startBtn');
      const doubleDown = document.getElementById('doubleDown');
      const rankings = document.getElementById('rankings');
      startBtn!.style.visibility = 'hidden';
      doubleDown!.style.visibility = 'hidden';
      gallery!.style.animation = 'galleryLeft 0.1s';
      const distance = rankings!.getBoundingClientRect().top - document.getElementById('breadCrumb')!.getBoundingClientRect().bottom;
      setTimeout(() => {
        startBtn!.style.display = 'none';
        doubleDown!.style.display = 'none';
        gallery!.style.display = 'none';
        rankings!.style.marginTop = `${distance}px`;
        rankings!.style.animation = '';
        setTimeout(() => {
          rankings!.style.transition = 'margin-top 1s ease-out';
          rankings!.style.marginTop = '10px';
        }, 500)
      }, 100);
    }
  }

  const handleRotatingGallery = () =>{
    let radius = 360;
    const autoRotate = true;
    const rotateSpeed = -60;
    const imgWidth = 80;
    const imgHeight = 80;

    const oDrag = document.getElementById('drag-container');
    const oSpin = document.getElementById('spin-container');
    const aImg = oSpin!.getElementsByTagName('img');
    const aEle = [...aImg];
    let sX: number;
    let sY: number;
    let nX: number;
    let nY: number;
    let desX = 0;
    let desY = 0;
    let tX = -10;
    let tY = 40;

    oSpin!.style.width = `${imgWidth}px`;
    oSpin!.style.height = `${imgHeight}px`;

    const ground = document.getElementById('ground');
    ground!.style.width = `${radius * 3}px`;
    ground!.style.height = `${radius * 3}px`
    function init(delayTime: any){
      for(let i = 0; i < aEle.length; i += 1){
        aEle[i].style.transform = `rotateY(${i * (360 / aEle.length)}deg) translateZ(${radius}px)`;
        aEle[i].style.transition = `transform 1s`;
        aEle[i].style.transitionDelay = `${delayTime || (aEle.length - i) / 4}s`;
      }
    }
    setTimeout(init, 200);

    function applyTransform(obj: any){
      if( tY > 180) tY = 180;
      if( tY < 0) tY = 0;
      obj.style.transform = `rotateX(${-tY}deg) rotateY(${tX}deg)`;
    }

    function playSpin(yes: boolean){
      oSpin!.style.animationPlayState = (yes?'running' : 'paused');
    }

    if(autoRotate) {
      const animationName = rotateSpeed > 0 ? 'spin' : 'spinRevert';
      oSpin!.style.animation = `${animationName} ${Math.abs(rotateSpeed)}s infinite linear `;
    }

    document.getElementById('llm-rotatingGallery')!.onpointerdown = function (e) {
      clearInterval(oDrag!.timer);
      e = e || window.event;
      sX = e.clientX;
      sY = e.clientY;

      document.onpointermove = function (event){
        event = event || window.event;
        nX = event.clientX ;
        nY = event.clientY;
        desX = nX - sX;
        desY = nY - sY;
        tX += desX * 0.1;
        tY += desY * 0.1;
        applyTransform(oDrag);
        sX = nX;
        sY = nY;
      };

      document.onpointerup = function(event) {
        oDrag!.timer = setInterval(function (){
          desX *= 0.95;
          desY *= 0.95;
          tX += desX * 0.1;
          tY += desY * 0.1;
          applyTransform(oDrag);
          playSpin(false);
          if(Math.abs(desX) < 0.5 && Math.abs(desY) < 0.5){
            clearInterval(oDrag!.timer);
            playSpin(true);
          }
        }, 17);
        this.onpointermove = null;
        this.onpointerup = null;
      };
      return false;
    }
    document.addEventListener('wheel', function changeGalleryRadius(e) {
      e = e || window.event;
      if (radius !== imgWidth * 2 + 20) {
        e.preventDefault();
        radius += e.wheelDelta / 20 || -e.detail;
        if (radius < imgWidth * 2 + 20) {
          radius = imgWidth * 2 + 20;
        } else if (radius > 500) {
          radius = 500;
        }
        init(0.01);
      }
      else{
        scrollAnimation(changeGalleryRadius, false);
      }
    }, { passive: false })
  }

  onMounted(() => {
    handleRotatingGallery();
    const startBtn = document.getElementById('startBtn');
    startBtn!.addEventListener('click', function(event: Event) {
      scrollAnimation(null, true);
      event.preventDefault();
    });
    setTimeout(() => {
      startBtn!.style.visibility = 'visible';
      startBtn!.style.opacity = '1';
    }, 3000)
  })
</script>

<style scoped lang="less">
  html{
    scroll-behavior: smooth;
  }

  .container {
    padding: 0 20px 20px 20px;
  }

  .drawer-model-title-text{
    font-size: 60px;
  }

  :deep(.arco-table-th) {
    &:last-child {
      .arco-table-th-item-title {
        margin-left: 16px;
      }
    }
  }
  .action-icon {
    margin-left: 12px;
    cursor: pointer;
  }
  .active {
    color: #0960bd;
    background-color: #e3f4fc;
  }
  .setting {
    display: flex;
    align-items: center;
    width: 200px;
    .title {
      margin-left: 12px;
      cursor: pointer;
    }
  }

  .drawer-model-title{
    display: flex;
    flow: right;
    justify-content: center;
    align-items: center;
  }

  .llm-details-subscribe-btn{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: 30px;
    padding: 5px 20px;
    font-size: 18px;
  }

  #slogan{
    z-index: 0;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
  }

  #llm-rotatingGallery{
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-perspective: 1000px;
    perspective: 1000px;
    -webkit-transform-style: preserve-3d;
    transform-style: preserve-3d;
    margin-top: 200px;
  }

  #drag-container, #spin-container{
    z-index: 10;
    position: relative;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    margin: 10px auto 40px auto;
    -webkit-transform-style: preserve-3d;
    transform-style: preserve-3d;
    -webkit-transform: rotateX(-10deg);
    transform: rotateX(-40deg);
  }

  #drag-container img{
    -webkit-transform-style: preserve-3d;
    transform-style: preserve-3d;
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    line-height: 200px;
    font-size: 50px;
    text-align: center;
    -webkit-box-shadow: 0 0 8px #fff;
    box-shadow: 0 0 #fff;
    -webkit-box-reflect: below 10px linear-gradient(transparent, transparent, #0005);
  }

  #drag-container img:hover{
    -webkit-box-shadow: 0 0 15px #fffd;
    box-shadow: 0 0 15px #fffd;
    -webkit-box-reflect: below 10px linear-gradient(transparent, transparent, #0007);
  }

  #ground{
    width: 900px;
    height: 900px;
    position: absolute;
    top: 100%;
    left: 50%;
    -webkit-transform: translate(-50%, -50%) rotateX(90deg);
    transform: translate(-50%, -50%) rotateX(90deg);
    background: -wekbit-radial-gradient(center center, farthest-side, #9993, transparent);
  }

  .sloganContent{
    padding-left: 0;
    display: flex;
    list-style-type: none;
    align-items: center;
  }

  .sloganContentText .sloganContentSubText{
    list-style: none;
  }

  .sloganContentText{
    letter-spacing: 10px;
    animation: titleFadeIn linear 3500ms;
  }

  .sloganContentSubText{
    letter-spacing: 5px;
    animation: subTitleFadeIn linear 3500ms;
  }

  #startBtn{
    display: inline-block;
    margin: 290px 50% auto 50%;
    transform: translateX(-50%);
    visibility: hidden;
    opacity: 0;
    text-align: center;
    line-height: 50px;
    font-size: 18px;
    white-space: nowrap;
    height: 50px;
    width: 130px;
    background: #1c61ff;
    color: whitesmoke;
    text-decoration: none;
    font-family: sans-serif;
    box-shadow: 0 4px 4px rgba(0,0,0,.2);
    border: 2px solid #3967FF;
    transition: .5s, opacity .5s linear;
  }

  #startBtn:hover{
    background: whitesmoke;
    text-shadow: 0 3px 3px rgba(0,0,0,.5);
  }

  #startBtn:before, #startBtn:after{
    content: '';
    position: absolute;
    width: 54%;
    height: 100%;
    background: #1c61ff;
    z-index: -1;
    opacity: 0;
  }

  #startBtn:hover:before{
    opacity: 1;
    top: 5px;
    left: -5px;
    box-shadow: 5px 2px 5px rgba(0,0,0,.2);
    animation: buttonAnimation 2s linear infinite;
  }

  #startBtn:hover:after{
    opacity: 1;
    top: -5px;
    right: -5px;
    box-shadow: -5px 2px 5px rgba(0,0,0,.2);
    animation: buttonAnimation 2s linear infinite;
    animation-delay: -1s;
  }
</style>

<style>
  @keyframes spin {
    from{
      transform: rotateY(0deg);
    }
    to{
      transform: rotateY(360deg);
    }
  }

  @keyframes spinRevert {
    from{
      transform: rotateY(360deg);
    }
    to{
      transform: rotateY(0deg);
    }
  }

  @keyframes upAndDown {
    0%{
      transform: translateY(0px);
    }
    50%{
      transform: translateY(-30px);
    }
    100%{
      transform: translateY(0px);
    }
  }

  @keyframes galleryLeft {
    100%{
      transform: translateX(1000px);
    }
  }

  @keyframes titleFadeIn {
    0%{
      transform: translateX(-50px);
      letter-spacing: 10px;
      opacity: 0;
      color: #00308f;
    }
    5%{
      opacity: 1;
    }
    25%{
      letter-spacing: -10px;
    }
    50%{
      transform: translateX(50px);
      letter-spacing: 10px;
      opacity: 0;
      color: #1c61ff;
    }
    100%{
      transform: translateX(0px);
      opacity: 1;
    }
  }

  @keyframes subTitleFadeIn {
    0%{
      transform: translateX(-30px);
      letter-spacing: 5px;
      opacity: 0;
      color: black;
    }
    5%{
      opacity: 1;
    }
    25%{
      letter-spacing: -5px;
    }
    50%{
      transform: translateX(30px);
      letter-spacing: 5px;
      opacity: 0;
      color: lightgrey;
    }
    100%{
      transform: translateX(0px);
      opacity: 1;
    }
  }

  @keyframes buttonAnimation {
    0%{
      top: 5px;
    }
    50%{
      top: -5px;
    }
    100%{
      top: 5px
    }
  }
</style>
