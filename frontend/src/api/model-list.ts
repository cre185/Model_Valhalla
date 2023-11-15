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
