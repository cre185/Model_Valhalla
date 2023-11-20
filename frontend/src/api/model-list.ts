import axios from 'axios';
import qs from 'query-string';
import type { DescData } from '@arco-design/web-vue/es/descriptions/interface';
import {PolicyListRes, PolicyParams, PolicyRecord} from "@/api/list";
import apiCat from '@/api/main';
import {newArray} from "@arco-design/web-vue/es/date-picker/utils";

export interface LLMRankingData{
    id: number;
    ranking: number;
    name: string;
    datasetScore: number;
    eloScore: number;
    datasetDetails: number[];
    license: string;
}

export interface DatasetRankingData{
    num: number;
    name: string;
    contentType: string;
    contentSize: number;
    createdTime: string;
    score: number;
}

export interface DatasetSearchRecord{
    ID: number;
    number: number;
    name: string;
    contentType: 'book' | 'imageCut' | 'imageClassify';
    contentSize: number;
    createdTime: string;
    score: number;
}

export interface DatasetSelectParams extends Partial<DatasetSearchRecord> {
    current: number;
    pageSize: number;
}

export interface LLMListRes {
    message: string;
    data: [];
}

export async function queryLLMList() {
    const LLMRankingList: {data: any, total: number} = { data:[], total: 0};
    const totalDatasetNum = 5;
    let response = await axios.get<LLMListRes>(apiCat('/testing/list'));
    const averageScore = await axios.get<LLMListRes>(apiCat('/ranking/average_list'));
    LLMRankingList.total = response.data.data.length;
    for(let i = 0; i <response.data.data.length; i += 1){
        const model = response.data.data[i] as { id: number, name: string, add_time: string, api_url: string, api_data:string,
                                                api_headers: string, author_id: number, description: string, api_RPM: string, elo_credit: number };
        LLMRankingList.data.push({id: model.id, name: model.name, ranking: 0, datasetScore: averageScore.data.data[model.id], eloScore: model.elo_credit,
                                    license: '', datasetDetails: new Array(totalDatasetNum).fill(0)})
    }

    // 获取排名
    LLMRankingList.data.sort((a: any, b: any) =>{
        return b.datasetScore - a.datasetScore;
    })
    for(let i = 0; i < LLMRankingList.data.length; i += 1){
        LLMRankingList.data[i].ranking = i + 1;
    }

    // 获取数据集具体评分
    response = await axios.get<LLMListRes>(apiCat('/ranking/list'));
    for(let i = 0; i < response.data.data.length; i += 1){
        const score = response.data.data[i] as {LLM: number, dataset: number, add_time: string, credit: number};
        LLMRankingList.data[score.LLM].datasetDetails[score.dataset] = score.credit;
    }
    return LLMRankingList;
}
