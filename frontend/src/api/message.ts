import axios from 'axios';
import apiCat from "@/api/main";

export interface userToDataset {
  msg_id: number;
  msg_type: string;
  src_UserID: string;
  dst_DatasetID: string;
  msg_title: string;
  msg_content: string;
  add_time: string;
  read: boolean;
  avatar?: string;
  messageType: "0";
}
export type MessageListType = userToDataset[];

export async function queryMessageList(jwt: string) {
  const response = await axios.get(apiCat('/user/list_message'), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: jwt,
    }
  })
  return response;
}

interface MessageStatus {
  ids: number[];
}

export function setMessageStatus(data: MessageStatus) {
  return axios.post<MessageListType>('/api/message/read', data);
}

export interface ChatRecord {
  id: number;
  username: string;
  content: string;
  time: string;
  isCollect: boolean;
}

export function queryChatList() {
  return axios.post<ChatRecord[]>('/api/chat/list');
}

export interface userToUser {
  src_UserID: string;
  dst_UserID: string;
  msg_type: string;
  msg_content: string;
  add_time: string;
  read: boolean;
};


export async function getUserAvatar(jwt: string, userID: string): Promise<string | undefined> {
  try {
    const response = await axios.get(apiCat(`/user/retrieve/${userID}`), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: jwt,
      }
    });
    return response.data.avatar;
  } catch (error) {
    console.error(error);
    return undefined;
  }
}