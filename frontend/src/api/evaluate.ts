/* eslint-disable */
import axios from 'axios';
import apiCat from '@/api/main';
import { LLMListRes } from './model-list';
import { updateComment } from "@/api/comment";
import { Button } from '@arco-design/web-vue';

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

export async function getLLMName(modelID: string)
{
    const response = await axios.get(apiCat(`/testing/retrieve/${modelID}`))
    const modelName = response.data.name;
    return modelName;
}

export async function sendAdvise(jwt:string, userAdvise:string)
{
    const response = await axios.post(apiCat('/user/create_message_to_admin'), {
        body: {
            target: "2",
            msg: userAdvise,
            msg_type: "advice",
        },
        headers: {
            'Content-Type': 'application/json',
            Authorization: jwt
        },
    });
    return response;
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

    constructor(modelA:number) {
        this.modelA = modelA;
        this.modelB = -1;
        this.QA = [] as QuestionAndAnswer[];
        this.result = 0;
    }

    async getModelB() {
        const response = await axios.post(apiCat('/testing/battle_match'), {
            llmId: this.modelA,
        });
        this.modelB = response.data.llmId;
    }

    async getStreamResponse(jwt:string, RefA:any, RefB:any) {
        fetch(apiCat('/testing/stream_generate'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: jwt
            },
            body: JSON.stringify({
                llmId: this.modelA,
                prompt: this.QA[this.QA.length-1].question
            }),
        })
            .then(response => {
                const reader = response.body!.getReader();
                function read(target: EvaluateRound) {
                    return reader.read().then(({ done, value }) => {
                        if (done) {
                            RefA.scrollTop = RefA.scrollHeight;
                            return;
                        }
                        target.QA[target.QA.length-1].answerA += new TextDecoder('utf-8').decode(value);
                        RefA.scrollTop = RefA.scrollHeight;
                        read(target);
                    });
                }
                this.QA[this.QA.length-1].answerA = '';
                read(this);
            })
            .catch(error => {
                console.error('Error fetching stream:', error);
            });

        fetch(apiCat('/testing/stream_generate'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: jwt
            },
            body: JSON.stringify({
                llmId: this.modelB,
                prompt: this.QA[this.QA.length-1].question
            }),
        })
            .then(response => {
                const reader = response.body!.getReader();
                function read(target: EvaluateRound) {
                    return reader.read().then(({ done, value }) => {
                        if (done) {
                            RefB.scrollTop = RefB.scrollHeight;
                            return;
                        }
                        target.QA[target.QA.length-1].answerB += new TextDecoder('utf-8').decode(value);
                        RefB.scrollTop = RefB.scrollHeight;
                        read(target);
                    });
                }
                this.QA[this.QA.length-1].answerB = '';
                read(this);
            })
            .catch(error => {
                console.error('Error fetching stream:', error);
            });
    }

    async updateEloResult() {
        await axios.post(apiCat('/testing/battle_result'), {
            llm1: this.modelA,
            llm2: this.modelB,
            result: this.QA,
            winner: this.result,
            round: this.QA.length
        });
    }
}

export default EvaluateRound;
export { QuestionAndAnswer };
