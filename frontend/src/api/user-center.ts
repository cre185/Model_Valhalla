import axios from 'axios';
import apiCat from "@/api/main";
import {BattleRecords, GetModelInfo, queryLLMList, QuestionAndAnswer} from "@/api/model-list";

export interface SubscribedModelRecord{
  id: number;
  name: string;
  ranking: number;
}

export async function querySubscribedModels(userId: number) {
  const modelList: SubscribedModelRecord[] = [];
  const response = await axios.get(apiCat(`/user/list_llm_subscription/${userId}`));
  const modelRankings = await queryLLMList();
  for (let i = 0; i < response.data.llms.length; i += 1) {
    const model = response.data.llms[i] as {
      id: number;
      name: string;
    }
    modelRankings.data.forEach((item: any) => {
        if(item.id === model.id){
          modelList.push({id: model.id, name: model.name, ranking: item.ranking});
        }
    })
  }
  return modelList;
}

export interface SubscribedDatasetRecord{
  id: number;
  name: string;
  domain: string;
}

export async function querySubscribedDatasets(userId: number) {
  const datasetList: SubscribedDatasetRecord[] = [];
  const response = await axios.get(apiCat(`/user/list_dataset_subscription/${userId}`));
  for (let i = 0; i < response.data.datasets.length; i += 1) {
    const data = response.data.datasets[i] as {
      id: number;
      name: string;
      domain: string;
    }
    datasetList.push({id: data.id, name: data.name, domain: data.domain});
  }
  return datasetList;
}

export interface LatestActivity {
  id: number;
  title: string;
  description: string;
  avatar: string;
}
export function queryLatestActivity() {
  return axios.post<LatestActivity[]>('/api/user/latest-activity');
}

export function userUploadApi(data: FormData, jwt: string) {
  return axios.post(apiCat('/user/update_avatar'), data, {
    headers: {
      Authorization: jwt,
    },
  });
}

export interface BattleRecordsData {
  id: number;
  testUser: number;
  model: string;
  adversarialModel: string;
  battleTime: string;
  winner: string;
  QA: QuestionAndAnswer[];
}

export async function queryBattleRecordsData(userID: number){
  const modelList = await axios.get(apiCat('/testing/list'));
  const battleRecordsDatalist: BattleRecordsData[] = [];
  const currentRecordID = new Set();

  const promises = modelList.data.data.map(async (model: any) => {
    const returnValue = await axios.post(apiCat('/testing/battle_history'), { llm: model.id });
    await Promise.all(
        returnValue.data.data.map(async (record: any) => {
          if (!currentRecordID.has(record.id)) {
            currentRecordID.add(record.id);
            if (record.user_id === userID) {
              battleRecordsDatalist.push({
                id: record.id,
                testUser: record.user_id,
                model: (await GetModelInfo(record.llm1)).name,
                adversarialModel: (await GetModelInfo(record.llm2)).name,
                battleTime: record.add_time,
                winner: '',
                QA: record.result
              });
              if(record.winner === 1){
                battleRecordsDatalist[battleRecordsDatalist.length - 1].winner =
                    battleRecordsDatalist[battleRecordsDatalist.length - 1].model;
              }
              else if(record.winner === -1){
                battleRecordsDatalist[battleRecordsDatalist.length - 1].winner =
                    battleRecordsDatalist[battleRecordsDatalist.length - 1].adversarialModel;
              }
            }
          }
        })
    );
  });
  await Promise.all(promises);
  return battleRecordsDatalist;
}
