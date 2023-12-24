import axios from 'axios';
import apiCat from "@/api/main";

// 评论，反馈意见，点赞，上传数据集
export interface userToUser {
    src_UserID: string;
    dst_UserID: string;
    msg_type: string;
    msg_content: string;
    add_time: string;
    read: boolean;
};

export interface userToDataset {
    src_UserID: string;
    dst_DatasetID: string;
    msg_type: string;
    msg_content: string;
    add_time: string;
    read: boolean;
};

export async function getMessage(jwt: string, formData: userToDataset[]) {
    console.log("66666");
    const response = await axios.get(apiCat('/user/list_message'), {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            Authorization: jwt,
        }
    })
    console.log("666", response.data.msgs[0]);
    formData = response.data;
    
}