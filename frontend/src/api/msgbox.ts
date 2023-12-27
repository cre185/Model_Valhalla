import axios from 'axios';
import apiCat from "@/api/main";
import {getUserAvatar, queryMessageList} from "@/api/message";
import {getToken} from "@/utils/auth";
import {useI18n} from "vue-i18n";

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
    const response = await axios.get(apiCat('/user/list_message'), {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            Authorization: jwt,
        }
    })
    formData = response.data;
}
