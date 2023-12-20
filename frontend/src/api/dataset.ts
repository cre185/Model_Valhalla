import axios from 'axios';
import apiCat from '@/api/main';
import * as Papa from 'papaparse';
import {ref} from "vue";
import {LLMListRes} from "@/api/model-list";
import {getAvatar, getUsername} from "@/api/user-info";

export class SubjectiveEvaluationData{
    readonly prompt: string;

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

export interface DatasetData {
    id: number;
    name: string;
    file: string;
    isSubjective: boolean;
    domain: string;
    contentSize: number;
    createdTime: string;
    description: string;
    authorId: number;
    tags: string[];
    showInput: boolean;
    newTag: string;
    inputRef: any;
    toDownload: boolean;
    uploadUserAvatar: string;
    uploadUsername: string;
}

export interface DatasetListRes {
    message: string;
    data: [];
}

export async function getDatasetFile(datasetID: number){
    return axios.get(apiCat(`/dataset/retrieve/${datasetID}`));
}

export async function downloadDataset(datasetID: number){
    return axios.get(apiCat(`/dataset/download/${datasetID}`));
}

export async function queryDatasetList() {
    const DatasetList: { data: any; total: number } = {data: [], total: 0};
    const response = await axios.get<DatasetListRes>(apiCat('/dataset/list'));
    DatasetList.total = response.data.data.length;
    for (let i = 0; i < response.data.data.length; i += 1) {
        const dataset = response.data.data[i] as {
            id: number;
            name: string;
            data_file: string;
            content_size: number;
            add_time: string;
            description: string;
            subjective: boolean;
            author: number;
            domain: number;
            tag: string[];
        };
        console.log(dataset);
        DatasetList.data.push({
            id: dataset.id,
            name: dataset.name,
            file: dataset.data_file,
            isSubjective: dataset.subjective,
            domain: dataset.domain,
            contentSize: dataset.content_size,
            createdTime: dataset.add_time,
            description: dataset.description,
            authorId: dataset.author,
            tags: dataset.tag,
            showInput: false,
            newTag: '',
            inputRef: ref(null),
            toDownload: false,
            uploadUserAvatar: '',
            uploadUsername: '',
        });
    }
    DatasetList.data.map(async (datasetData: DatasetData) => {
        datasetData.uploadUserAvatar = await getAvatar(datasetData.authorId.toString());
        datasetData.uploadUsername = await getUsername(datasetData.authorId.toString());
        console.log(datasetData.uploadUsername);
        return datasetData;
    })
    return DatasetList;
}

export async function updateDatasetTags (datasetID: number, tags: string[]) {
    return axios.post(apiCat(`/dataset/update_tag`), {id: datasetID, tag: tags});
}
export const generateSubEvalData = (datasetID: number): Promise<SubjectiveEvaluationData[]> => {
    return new Promise((resolve, reject) => {
        const dataList: SubjectiveEvaluationData[] = [];
        downloadDataset(datasetID).then(returnValue => {
            const parsedData = Papa.parse(returnValue.data.join(''), {
                header: true,
                dynamicTyping: true,
                skipEmptyLines: true,
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
    const response = await axios.post(apiCat(`ranking/list_selected_credit`), { datasetId: datasetID });
    return response.data;
}
