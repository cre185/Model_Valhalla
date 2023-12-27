import axios from 'axios';
import apiCat from "@/api/main";
import {queryLLMList} from "@/api/model-list";

export interface MyProjectRecord {
  id: number;
  name: string;
  description: string;
  peopleNumber: number;
  contributors: {
    name: string;
    email: string;
    avatar: string;
  }[];
}
export function queryMyProjectList() {
  return axios.post('/api/user/my-project/list');
}

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

export interface MyTeamRecord {
  id: number;
  avatar: string;
  name: string;
  peopleNumber: number;
}
export function queryMyTeamList() {
  return axios.post('/api/user/my-team/list');
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

export function saveUserInfo() {
  return axios.post('/api/user/save-info');
}

export interface BasicInfoModel {
  username: string;
  profile: string;
}

export interface EnterpriseCertificationModel {
  accountType: number;
  status: number;
  time: string;
  legalPerson: string;
  certificateType: string;
  authenticationNumber: string;
  enterpriseName: string;
  enterpriseCertificateType: string;
  organizationCode: string;
}

export type CertificationRecord = Array<{
  certificationType: number;
  certificationContent: string;
  status: number;
  time: string;
}>;

export interface UnitCertification {
  enterpriseInfo: EnterpriseCertificationModel;
  record: CertificationRecord;
}

export function queryCertification() {
  return axios.post<UnitCertification>('/api/user/certification');
}

export function userUploadApi(data: FormData, jwt: string) {
  return axios.post(apiCat('/user/update_avatar'), data, {
    headers: {
      Authorization: jwt,
    },
  });
}
