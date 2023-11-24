import axios from 'axios';
import apiCat from '@/api/main';
import { LLMListRes } from './model-list';

export interface SelectedModel {
    id: number;
    name: string;
}
export async function queryLLMevaluateList()
{
    const LLMList: {data: any, total: number} = { data:[], total: 0};
    const response = await axios.get<LLMListRes>(apiCat('/testing/list'));
    for(let i = 0; i < response.data.data.length; i += 1)
    {
        const model = response.data.data[i] as {id: number, name: string};
        LLMList.data.push({id: model.id, name: model.name});
    }
    return LLMList;
}