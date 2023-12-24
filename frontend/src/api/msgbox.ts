import axios from 'axios';
import apiCat from "@/api/main";

// 评论，反馈意见，点赞，上传数据集
export interface User_to_user {
    src_UserID: string;
    dst_UserID: string;
    msg_type: string;
    msg_content: string;
    add_time: string;
    read: boolean;
};

export interface User_to_dataset {
    src_UserID: string;
    dst_DatasetID: string;
    msg_type: string;
    msg_content: string;
    add_time: string;
    read: boolean;
};