import axios from 'axios';
import qs from 'query-string';
import type { DescData } from '@arco-design/web-vue/es/descriptions/interface';
export interface LLMRankingData{
    ranking: number;
    name: string;
    averageMsgLength: number;
    datasetScore: number;
    eloScore: number;
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
