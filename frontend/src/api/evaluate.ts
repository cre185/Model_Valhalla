/* eslint-disable */
import axios from 'axios';
import apiCat from '@/api/main';
import { LLMListRes } from './model-list';
import { updateComment } from "@/api/comment";

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
    user:number
    QA:QuestionAndAnswer[]
    result:number
    date:string

    constructor(modelA:number, modelB:number, user:number) {
        this.modelA = modelA;
        this.modelB = modelB;
        this.user = user;
        this.QA = [] as QuestionAndAnswer[];
        this.result = -1;
        this.date = '';
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
}

export default EvaluateRound;