/* eslint-disable */
import axios from 'axios';
import apiCat from '@/api/main';
import { LLMListRes } from './model-list';
import { updateComment } from "@/api/comment";

export interface SelectedModel {
    id: string;
    name: string;
}

export async function queryLLMevaluateList()
{
    const LLMList: {data: any, total: number} = { data:[], total: 0};
    const response = await axios.get<LLMListRes>(apiCat('/testing/list'));
    for(let i = 0; i < response.data.data.length; i += 1)
    {
        const model = response.data.data[i] as {id: string, name: string};
        LLMList.data.push({id: model.id.toString(), name: model.name});
    }
    return LLMList;
}

class QuestionAndAnswer {
    question:string
    answerA:string
    answerB:string

    constructor(question:string, answerA:string, answerB:string) {
        this.question = question;
        this.answerA = answerA;
        this.answerB = answerB;
    }
}

class EvaluateRound {
    modelA:number
    modelB:number
    QA:QuestionAndAnswer[]
    result:number
    date:string

    constructor(modelA:number) {
        this.modelA = modelA;
        this.modelB = -1;
        this.QA = [] as QuestionAndAnswer[];
        this.result = 0;
        this.date = '';
    }

    async getModelB() {
        const response = await axios.post(apiCat('/testing/battle_match'), {
            llmId: this.modelA,
        });
        this.modelB = response.data.llmId;
    }

    async getResponse() {
        let response = await axios.post(apiCat('/testing/generate'), {
            llmId: this.modelA,
            prompt: this.QA[this.QA.length-1].question
        });
        this.QA[this.QA.length-1].answerA = response.data.content;
        response = await axios.post(apiCat('/testing/generate'), {
            llmId: this.modelB,
            prompt: this.QA[this.QA.length-1].question
        });
        this.QA[this.QA.length-1].answerB = response.data.content;
    }

    async updateEloResult() {
        await axios.post(apiCat('/testing/battle_result'), {
            llm1: this.modelA,
            llm2: this.modelB,
            result: this.QA,
            winner: this.result,
            add_time: this.date,
        });
    }
}

export default EvaluateRound;
export { QuestionAndAnswer };