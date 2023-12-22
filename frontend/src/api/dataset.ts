import axios from 'axios';
import apiCat from '@/api/main';
import * as Papa from 'papaparse';
import {ref} from "vue";
import {LLMListRes} from "@/api/model-list";
import {getAvatar, getUsername} from "@/api/user-info";
import { FileItem } from '@arco-design/web-vue';
import * as fs from 'fs';

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

export async function getModelScore(datasetID: number) {
    const response = await axios.post(apiCat(`ranking/list_selected_credit`), {datasetId: datasetID});
    return response.data;
}
export interface SelectedDataset {
    id: string;
    name: string;
}

export async function simplifiedQueryDatasetList()
{
    const LLMList: {data: any, total: number} = { data:[], total: 0};
    const response = await axios.get<LLMListRes>(apiCat('/dataset/list'));
    for(let i = 0; i < response.data.data.length; i += 1)
    {
        const dataset = response.data.data[i] as {id: string, name: string};
        LLMList.data.push({id: dataset.id.toString(), name: dataset.name});
    }
    return LLMList;
}

interface FormDatasetData {
    datasetName: string;
    feedbackType: string;
    feedbackContent: string;
    reportReason: string;
    reportContent: string;
    annex: FileItem[];
    file: File[];
  }

  /* export async function sendFeedback(jwt: string, formData: FormDatasetData) {
    const response = await fetch(apiCat('/user/create_message_to_admin'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: jwt,
      },
      body: JSON.stringify({
        msg: formData.feedbackType,
        msg_type: 'feedback',
        msg_content : {
          'datasetID': formData.datasetName,
          'feedbackType': formData.feedbackType,
          'feedbackContent': formData.feedbackContent,
        },
        // msg_file: formData.file,
        // msg_file: formData.annex || [],
      }),
    });
} */

   export async function sendFeedback(jwt: string, formData: FormDatasetData) {

    const formDataObject = new FormData();

    formDataObject.append('msg', formData.feedbackType);
    formDataObject.append('msg_type', 'feedback');
    formDataObject.append('msg_content', JSON.stringify({
        'datasetID': formData.datasetName,
        'feedbackType': formData.feedbackType,
        'feedbackContent': formData.feedbackContent,
    }));

    if (formData.file) {
        formDataObject.append('msg_file', formData.file[0], formData.file[0].name);
    }
    // console.log(formData.file[0].stream());
    // const request = new XMLHttpRequest();
    // request.open("POST", "http://localhost:8000/user/create_message_to_admin");
    // request.setRequestHeader('Authorization', jwt);
    // request.send(formDataObject);

    const response = await fetch('http://localhost:8000/user/create_message_to_admin',{
    method: 'POST',
        headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': jwt,
        },
        body: formDataObject,
     });
} 

export async function sendReport(jwt: string, formData: FormDatasetData) {
    const response = await fetch(apiCat('/user/create_message_to_admin'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: jwt,
      },
      body: JSON.stringify({
        msg: formData.reportReason,
        msg_type: 'report',
        msg_content: {
            'datasetID': formData.datasetName,
            'reportReason': formData.reportReason,
            'reportContent': formData.reportContent,
          }
      }),
    });
}


interface FormDataset {
    datasetName: string,
    datasetIntroduction: string,
    datasetApplication: string,
    datasetTags: string[],
    annex: FileItem[],
    files: File[],
}
export async function sendDataset(jwt: string, formData: FormDataset) {
    await fetch(apiCat('/dataset/create'), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: jwt,
        },
        body: JSON.stringify({
            name: formData.datasetName,
            domain: formData.datasetApplication,
            tag: formData.datasetTags,
            
            // author: formData.datasetPublisher
        }),
    });

    const DatasetFile = new FormData();
    DatasetFile.append('name', formData.datasetName);
    // DatasetFile.append('domain', formData.datasetApplication);
    // DatasetFile.append('tag', formData.datasetTags);
    // DatasetFile.append('msg_file', formData.files[0]);
    console.log(formData.files[0]);
    DatasetFile.append('file', formData.files[0]);
    await fetch(apiCat('/dataset/create'),{
    method: 'POST',
        headers: {
            // 'Content-Type': 'multipart/form-data',
            'Authorization': jwt,
        },
        body: DatasetFile,
     });


}
