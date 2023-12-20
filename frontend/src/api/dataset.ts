import axios from 'axios';
import apiCat from '@/api/main';
import * as Papa from 'papaparse';

export class SubjectiveEvaluationData{
    private prompt: string;

    private subjects: string[];

    private answer: string | undefined;

    private score: number | undefined;

    private answerGenerated: boolean;

    private scored: boolean;

    constructor(prompt: string, subjects: string[], answer: string, score: number) {
        this.prompt = prompt;
        this.subjects = subjects;
        this.answer = answer;
        this.score = score;
        this.answerGenerated = false;
        this.scored = false;
    }

    appendSubject(subject: string){
        this.subjects.push(subject);
    }

    getPrompt(){
        return this.prompt;
    }

    setAnswer(answer: string){
        this.answer = answer;
    }

    getAnswer(){
        return this.answer;
    }

    setScore(score: number){
        this.score = score;
    }

    getScore(){
        return this.score;
    }

    getScored(){
        return this.scored;
    }

    setScored(){
        this.scored = true;
    }

    getAnswerGenerated(){
        return this.answerGenerated;
    }

    setAnswerGenerated(){
        this.answerGenerated = true;
    }
}

async function getDatasetFile(datasetID: number){
    return axios.get(apiCat(`/dataset/retrieve/${datasetID}`));
}

async function downloadDataset(datasetID: number){
    return axios.get(apiCat(`/dataset/download/${datasetID}`));
}

export const generateSubEvalData = (datasetID: number): Promise<SubjectiveEvaluationData[]> => {
    return new Promise((resolve, reject) => {
        const dataList: SubjectiveEvaluationData[] = [];
        downloadDataset(datasetID).then(returnValue => {
            const parsedData = Papa.parse(returnValue.data.join(''), {
                header: true,  // 设置为 true 表示第一行是标题行
                dynamicTyping: true,  // 根据内容自动转换为数字等类型
                skipEmptyLines: true,  // 跳过空行
            })
            for(let i = 0; i < parsedData.data.length; i += 1){
                const data = parsedData.data[i] as {Prompt: string; subject: string}
                const subjects = data.subject.split('`');
                dataList.push(new SubjectiveEvaluationData(data.Prompt, [], '', 0));
                for(let j = 0; j < subjects.length; j+= 1){
                    if(subjects[j] !== '' && subjects[j] !== ' ')
                    dataList[i].appendSubject(subjects[j]);
                }
            }
            resolve(dataList);
        })
    })
}

export async function getModelDetails(){
    const response = await axios.get(apiCat(`/testing/list`));
    return response.data.data;
}

export async function getModelScore(datasetID: number){
    const response = await axios.post(apiCat(`/ranking/list_selected_credit`), { datasetId: datasetID });
    return response.data.data;
}