import axios from 'axios';
import qs from 'query-string';
import type { DescData } from '@arco-design/web-vue/es/descriptions/interface';
import { PolicyListRes, PolicyParams, PolicyRecord } from '@/api/list';
import apiCat from '@/api/main';
import { newArray } from '@arco-design/web-vue/es/date-picker/utils';
import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';

type Column = TableColumnData & { checked?: true };

export class QuestionAndAnswer {
  question: string

  answerA: string

  answerB: string

  constructor(question:string, answerA:string, answerB:string) {
    this.question = question;
    this.answerA = answerA;
    this.answerB = answerB;
  }
}
export interface LLMRankingData {
  id: number;
  ranking: number;
  name: string;
  datasetScore: number;
  eloScore: number;
  license: string;
  [key: string]: any;
}

export interface DatasetRankingData {
  id: number;
  name: string;
  contentType: string;
  contentSize: number;
  createdTime: string;
  score: number;
}

export interface BattleRecords{
  id: number;
  llm1: number;
  llm2: number;
  winner: number;
  round: number;
  result: string;
  add_time: string;
  user_id: number;
}

export interface BattleRecordsData{
  id: number;
  testUser: number;
  testUsername: string;
  testUserAvatar: string;
  adversarialModel: string;
  battleTime: string;
  result: number;
  QA: QuestionAndAnswer[];
  displayRound: number;
}

export interface LLMListRes {
  message: string;
  data: [];
}

export async function queryLLMList() {
  const LLMRankingList: { data: any; total: number } = { data: [], total: 0 };
  let totalDatasetNum = 0;
  await axios.get<LLMListRes>(apiCat('/dataset/list')).then((res) => {
    totalDatasetNum = res.data.data.length;
  });
  let response = await axios.get<LLMListRes>(apiCat('/testing/list'));
  const averageScore = await axios.get<LLMListRes>(
    apiCat('/ranking/average_list')
  );
  LLMRankingList.total = response.data.data.length;
  for (let i = 0; i < response.data.data.length; i += 1) {
    const model = response.data.data[i] as {
      id: number;
      name: string;
      add_time: string;
      api_url: string;
      api_data: string;
      api_headers: string;
      description: string;
      api_RPM: number;
      elo_credit: number;
    };
    // LLMRankingList.data.push({id: model.id, name: model.name, ranking: 0, datasetScore: averageScore.data.data[model.id - 1], eloScore: model.elo_credit,
    // license: '', datasetDetails: new Array(totalDatasetNum).fill(0)})
    LLMRankingList.data.push({
      id: model.id,
      name: model.name,
      ranking: 0,
      datasetScore: averageScore.data.data[model.id - 1].toFixed(2),
      eloScore: model.elo_credit.toFixed(2),
      license: '',
    });
  }
  // 获取排名
  LLMRankingList.data.sort((a: any, b: any) => {
    return b.datasetScore - a.datasetScore;
  });
  for (let i = 0; i < LLMRankingList.data.length; i += 1) {
    LLMRankingList.data[i].ranking = i + 1;
  }
  // 获取数据集具体评分
  response = await axios.get<LLMListRes>(apiCat('/ranking/list'));
  for (let i = 0; i < response.data.data.length; i += 1) {
    const score = response.data.data[i] as {
      LLM: number;
      dataset: number;
      add_time: string;
      credit: number;
    };
    for (let j = 0; j < LLMRankingList.data.length; j += 1) {
      if (LLMRankingList.data[j].id === score.LLM) {
        LLMRankingList.data[j][score.dataset] = score.credit;
        break;
      }
    }
  }
  return LLMRankingList;
}

export async function queryDatasetbehaviorList(modelId: string) {
  const DatasetRankingList: { data: any; total: number } = {
    data: [],
    total: 0,
  };
  // modelId = "99";
  const modelNum = Number(modelId);
  let response = await axios.get<LLMListRes>(apiCat('/dataset/list'));
  for (let i = 0; i < response.data.data.length; i += 1) {
    const dataset = response.data.data[i] as {
      id: number;
      name: string;
      add_time: string;
      content_size: number;
      data_file: string;
      subjective: boolean;
    };
    const datasetType = dataset.subjective ? '主观题' : '客观题';
    DatasetRankingList.data.push({
      id: dataset.id,
      name: dataset.name,
      contentSize: dataset.content_size,
      contentType: datasetType,
      createdTime: dataset.add_time,
      score: modelNum,
    });
  }
  response = await axios.get<LLMListRes>(apiCat('/ranking/list'));
  for (let i = 0; i < response.data.data.length; i += 1) {
    const datasetScore = response.data.data[i] as {
      LLM: number;
      dataset: number;
      add_time: string;
      credit: number;
    };
    // DatasetRankingList.data[i].score = datasetScore.credit;
    if (datasetScore.LLM === modelNum) {
      DatasetRankingList.data[datasetScore.dataset - 1].score =
        datasetScore.credit;
    }
  }
  return DatasetRankingList;
}

export async function queryDatasetColumnList() {
  const datasetColumnList: Column[] = [];
  const response = await axios.get<LLMListRes>(apiCat('/dataset/list'));
  for (let i = 0; i < response.data.data.length; i += 1) {
    const dataset = response.data.data[i] as {
      id: number;
      name: string;
      add_time: string;
      data_file: string;
      author_id: number;
      subjective: boolean;
    };
    datasetColumnList.push({
      title: dataset.name,
      dataIndex: dataset.id.toString(),
      slotName: dataset.id.toString(),
      align: 'center',
      sortable: { sortDirections: ['ascend', 'descend'] },
    });
  }
  return datasetColumnList;
}

export async function GetModelInfo(modelID: number) {
  const res = await axios.get(apiCat(`/testing/retrieve/${modelID}`));
  return res.data;
}

export async function queryLLMBattleRecords(modelID: number) {
  const res = await axios.post<BattleRecords[]>(apiCat('/testing/battle_history'), {llm: modelID});
  return res.data;
}
