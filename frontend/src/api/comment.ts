/* eslint-disable */
import axios from 'axios';
import apiCat from "@/api/main";
import {getAvatar, getUsername} from "@/api/user-info";
import {useI18n} from "vue-i18n";
import useLocale from "@/hooks/locale";
import { useUserStore } from '@/store';

const userStore = useUserStore();
class MyComment {
    public author: string

    public toAuthor: string

    public commentId: number = -1

    public toId: undefined | number

    public avatar: string

    public content: string

    public datetime: string

    public like: number

    public ifLike: boolean

    public ifHate: boolean

    public ifReply: boolean

    public lastClicked: number

    public children: any[]

    constructor(author: string, toAuthor: string, avatar: string, content: string, datetime: string, like: number, ifLike: boolean, ifHate: boolean, ifReply: boolean, children: any[]) {
        this.author = author
        this.toAuthor = toAuthor
        this.avatar = avatar
        this.content = content
        this.datetime = datetime
        this.like = like
        this.ifLike = ifLike
        this.ifHate = ifHate
        this.ifReply = ifReply
        this.lastClicked = -2
        this.children = children
    }

    async increaseLike(jwt: string, toAuthorName: string, targetID: string, flag: boolean) {
        this.like += 1;
        const response = await axios.post(apiCat('/user/find_user_by_name'), { username: toAuthorName }, {
            headers: {
                Authorization: jwt,
            },
        });
        if (userStore.accountId !== response.data.id) {
            await axios.post(apiCat('/user/create_message'), {
                msg_type: "Like",
                msg: "Unknown",
                target: [response.data.id],
                msg_content: {
                    'likeContent': this.content,
                    'likeFlag': flag,
                    'targetID': targetID,
                }
            }, {
                headers: {
                    Authorization: jwt,
                },
            })
        }
    }

    decreaseLike() {
        this.like -= 1
    }

    async changeLikeState(jwt: string, toAuthorName: string, modelId: string, flag = true) {
        this.ifLike = !this.ifLike
        if (this.ifLike) {
            this.increaseLike(jwt, toAuthorName, modelId, flag)
        } else {
            this.decreaseLike()
        }
        if (flag) {
            await axios.post(apiCat('/ranking/like_llm_comment'), {
                id: this.commentId
            }, {
                headers: {
                    Authorization: jwt,
                },
            });
        }
        else {
            await axios.post(apiCat('/ranking/like_dataset_comment'), {
                id: this.commentId
            }, {
                headers: {
                    Authorization: jwt,
                },
            });
        }
        if (this.ifHate) {
            this.ifHate = false;
        }
    }

    async changeHateState(jwt: string, flag = true) {
        this.ifHate = !this.ifHate
        if (flag) {
            await axios.post(apiCat('/ranking/like_llm_comment'), {
                id: this.commentId,
                dislike: true
            }, {
                headers: {
                    Authorization: jwt,
                },
            });
        }
        else {
            await axios.post(apiCat('/ranking/like_dataset_comment'), {
                id: this.commentId,
                dislike: true
            }, {
                headers: {
                    Authorization: jwt,
                },
            });
        }
        if (this.ifLike) {
            this.ifLike = false;
            this.decreaseLike();
        }
    }

    changeReplyState(newComment: MyComment, whoClicked: number) {
        if (this.lastClicked === -2) {
            this.ifReply = true
            this.lastClicked = whoClicked
        } else if (!this.ifReply) {
            this.ifReply = true
            this.lastClicked = whoClicked
        } else if (this.lastClicked === whoClicked) {
            this.ifReply = false
            this.lastClicked = -2
        } else if (this.lastClicked !== whoClicked) {
            this.lastClicked = whoClicked
        }
        newComment.content = ''
    }

    async addComment(item: MyComment, newComment: MyComment, modelId: string, jwt: string, flag = true) {
        this.ifReply = false
        const tmp = new MyComment('', '', '', '', '', 0, false, false, false, []);
        const date = new Date();
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        tmp.datetime = `${year}-${month}-${day} ${hours}:${minutes}`;
        if (newComment.toAuthor === '') {
            tmp.content = `${newComment.content}`;
        } else {
            tmp.content = `@ ${newComment.toAuthor} :${newComment.content}`;
        }
        tmp.avatar = newComment.avatar;
        tmp.author = newComment.author;
        tmp.toAuthor = newComment.toAuthor;
        tmp.toId = newComment.toId;
        await updateComment(modelId, tmp, jwt, flag);
        item.children.push(tmp)
        newComment.content = ''
        newComment.toId = undefined;
    }
}

export default MyComment;

export async function getComment(ModelID: string, commentDetails: any, jwt: string, flag = true) {
    let response;
    if (flag) {
        response = await axios.get(apiCat(`/ranking/llm_comment/${ModelID}`), {
            headers: {
                Authorization: jwt,
            },
        });
    }
    else {
        response = await axios.get(apiCat(`/ranking/dataset_comment/${ModelID}`), {
            headers: {
                Authorization: jwt,
            },
        });
    }
    commentDetails.value = [];
    for (const item of response.data.data) {
        const id = item.user;
        let username: string;
        let avatar: string;

        await getUsername(id).then((returnValue) => {
            username = returnValue;
        });

        await getAvatar(id).then((returnValue) => {
            avatar = returnValue;
        });

        if (item.respond_to === null) {
            const tmp = new MyComment(username!, '', avatar!, item.comment, item.add_time, item.like, item.if_like, item.if_dislike, false, []);
            tmp.commentId = item.id;
            commentDetails.value.push(tmp);
        } else {
            let index = item.respond_to;
            for (let i = 0; i < response.data.data.length; i += 1) {
                if (response.data.data[i].id === index) {
                    index = i;
                    break;
                }
            }
            let target = response.data.data[index];
            const targetId = target.user;
            let targetName = '';
            await getUsername(targetId).then((returnValue) => {
                targetName = returnValue;
            });
            const tmp = new MyComment(username!, targetName!, avatar!, item.comment, item.add_time, item.like, item.if_like, item.if_dislike, false, []);
            tmp.commentId = item.id;
            tmp.toId = target.commentId;
            while (target.respond_to !== null) {
                index = target.respond_to;
                for (let i = 0; i < response.data.data.length; i += 1) {
                    if (response.data.data[i].id === index) {
                        index = i;
                        break;
                    }
                }
                target = response.data.data[index];
            }
            for (let i = 0; i < commentDetails.value.length; i += 1) {
                if (commentDetails.value[i].commentId === target.id) {
                    commentDetails.value[i].children.push(tmp);
                    break;
                }
            }
        }
    }
}

export async function updateComment(
    modelId: string,
    newComment: any,
    jwt: string,
    flag = true
) {
    let responseTwo;
    if (flag) {
        const response = await axios.post(apiCat('/ranking/comment'), { llm: modelId, comment: newComment.content, respond_to: newComment.toId }, {
            headers: {
                Authorization: jwt,
            },
        });
        newComment.commentId = response.data.id;
        responseTwo = await axios.get(apiCat(`/ranking/llm_comment/${modelId}`), {
            headers: {
                Authorization: jwt,
            },
        });
    }
    else {
        const response = await axios.post(apiCat('/ranking/comment'), { dataset: modelId, comment: newComment.content, respond_to: newComment.toId }, {
            headers: {
                Authorization: jwt,
            },
        });
        newComment.commentId = response.data.id;
        responseTwo = await axios.get(apiCat(`/ranking/dataset_comment/${modelId}`), {
            headers: {
                Authorization: jwt,
            },
        });
    }
    let srcCommentID;
    let srcUserID;
    let parentContent;
    let childContent;
    let userID;
    for (let i = responseTwo.data.data.length - 1; i >= 0; i--) {
        if (responseTwo.data.data[i].id === newComment.commentId) {
            userID = responseTwo.data.data[i].user;
            srcCommentID = responseTwo.data.data[i].respond_to;
            childContent = responseTwo.data.data[i].comment;
            break;
        }
    }
    if (srcCommentID) {
        for (let i = 0; i < responseTwo.data.data.length; i++) {
            if (responseTwo.data.data[i].id === srcCommentID) {
                srcUserID = responseTwo.data.data[i].user;
                parentContent = responseTwo.data.data[i].comment;
                break;
            }
        }
        if (userID !== srcUserID) {
            await axios.post(apiCat('/user/create_message'),
                {
                    msg_type: "Reply",
                    msg: "Unknown",
                    target: [srcUserID],
                    msg_content: {
                        'parentContent': parentContent,
                        'childContent': childContent,
                        'contentFlag': flag,
                        'targetID': modelId,
                    }

                },
                {
                    headers: {
                        Authorization: jwt,
                    },
                }
            )
        }
    }
}
