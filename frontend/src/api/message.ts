import axios from 'axios';
import apiCat from "@/api/main";
import {getToken} from "@/utils/auth";
import {useI18n} from "vue-i18n";

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

export async function getMessageData(lan: string, t: any){
  const { data } = await queryMessageList(getToken()!);
  const returnValue: userToDataset[] = [];
  // messageData.messageList = data;
  for (let i = 0; i < data.msgs.length; i += 1) {
    const item: any = data.msgs[i];
    const newUserToDataset: userToDataset = {
      msg_id: item.id,
      msg_type: item.msg_type,
      src_UserID: item.author,
      msg_text: "Unknown",
      msg_content: item.msg_content,
      msg_title: "Unknown",
      add_time: item.add_time,
      read: item.read,
      avatar: "Unknown",
      messageType: "0",
    };

    // eslint-disable-next-line
    const responseUser = await axios.get(apiCat(`/user/retrieve/${item.author}`), {
      headers: {
        Authorization: getToken()!,
      },
    });
    if (item.msg_type === "Upload") { // 上传数据集
      newUserToDataset.msg_title = t('messageBox.upload.title');
      if (lan === "zh-CN") {
        newUserToDataset.msg_text = `${responseUser.data.username}上传了数据集:${item.msg_content.datasetName}`;
      }
      else {
        newUserToDataset.msg_text = `${responseUser.data.username} uploaded the dataset ${item.msg_content.datasetName}`;
      }
    }
    else if (item.msg_type === "Reply") { // 回复了评论
      if (lan === "zh-CN") {
        newUserToDataset.msg_title = `${responseUser.data.username}回复了你的评论`;
      }
      else {
        newUserToDataset.msg_title = `${responseUser.data.username} replied to your comment`;
      }
      newUserToDataset.msg_text = item.msg_content.childContent;
    }
    else if (item.msg_type === "Like") { // 点赞消息
      newUserToDataset.msg_title = t('messageBox.like.title');
      if (lan === "zh-CN") {
        newUserToDataset.msg_text = `${responseUser.data.username}点赞了你的评论“${item.msg_content.likeContent}”`;
      }
      else {
        newUserToDataset.msg_text = `${responseUser.data.username} liked your comment "${item.msg_content.likeContent}"`;
      }
    }
    else if (item.msg_type === "Feedback") { // 数据集反馈意见
      newUserToDataset.msg_title = t('messageBox.feedback.title');
      // eslint-disable-next-line
      const responseDataset = await axios.get(apiCat(`/dataset/retrieve/${item.msg_content.datasetID}`), {
        headers: {
          Authorization: getToken()!,
        },
      });
      if (lan === "zh-CN") {
        newUserToDataset.msg_text = `原因:${item.msg_content.feedbackType}，具体描述:${item.msg_content.feedbackContent}`;
      }
      else {
        newUserToDataset.msg_text = `Reason: ${item.msg_content.feedbackType}, Detailed description: ${item.msg_content.feedbackContent}`;
      }
    }
    else if (item.msg_type === "Report") { // 数据集举报
      newUserToDataset.msg_title = t('messageBox.report.title');
      // eslint-disable-next-line
      const responseDataset = await axios.get(apiCat(`/dataset/retrieve/${item.msg_content.datasetID}`), {
        headers: {
          Authorization: getToken()!,
        },
      });
      if (lan === "zh-CN") {
        newUserToDataset.msg_text = `原因:${item.msg_content.reportReason}，具体描述:${item.msg_content.reportContent}`;
      }
      else {
        newUserToDataset.msg_text = `Reason: ${item.msg_content.reportReason}, Detailed description: ${item.msg_content.reportContent}`;
      }
    }
    else if (item.msg_type === "Advice") { // 对抗评测意见
      if (lan === "zh-CN") {
        newUserToDataset.msg_title = `${responseUser.data.username}提出评测建议`;
        newUserToDataset.msg_text = `具体内容:${item.msg_content.adviceContent}`;
      }
      else {
        newUserToDataset.msg_title = `${responseUser.data.username} proposed suggestions`
        newUserToDataset.msg_text = `Detailed content: ${item.msg_content.adviceContent}`;
      }
    }
    // eslint-disable-next-line
    newUserToDataset.avatar = await getUserAvatar(getToken()!, item.author);
    returnValue.push(newUserToDataset);
  }
  return returnValue;
}
