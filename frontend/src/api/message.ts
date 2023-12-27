import axios from 'axios';
import apiCat from "@/api/main";

export interface userToDataset {
  msg_id: number;
  msg_type: string; // 消息类型，对应六种
  src_UserID: string; // 发送此消息的人ID，如上传数据集的用户，点赞你的人
  msg_text: string; // 消息的内容，用于存储加工后的内容
  msg_title: string; // 消息的标题，和上面的字段共同呈现消息框中消息样式
  msg_content: JSON; // 存储各种需要的字段，不同消息类型字段不同，具体参考数据库
  add_time: string;
  read: boolean; // 是否读取
  avatar?: string;
  messageType: "0"; // 后续会删除
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