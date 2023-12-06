import axios from 'axios';
import apiCat from '@/api/main';

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
}

async function getDatasetFile(datasetID: number){
    return axios.get(apiCat(`/dataset/retrieve/${datasetID}`));
}

export const generateSubEvalData = (datasetID: number): Promise<SubjectiveEvaluationData[]> => {
    return new Promise((resolve, reject) => {
        let dataList: SubjectiveEvaluationData[];
        let filePath: string;
        getDatasetFile(datasetID).then(returnValue => {
            filePath = returnValue.data.data_file;
            let count = 0;
            for(let i = 0; i < filePath.length; i += 1){
                if(filePath[i] === '/'){
                    count += 1;
                    if(count === 3)
                    {
                        filePath = filePath.substring(i);
                        break;
                    }
                }
            }
            axios.get(apiCat(filePath), {responseType: 'blob'}).then(response => {
                const blob = response.data;
                const fileObject = new File([blob], 'file.txt', {type: 'application/octet-stream'});
                console.log(fileObject);
                return dataList;
            })
        })
    })
}
