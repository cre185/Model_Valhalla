class MyComment {
    public author:string

    public toAuthor:string

    public avatar:string

    public content:string

    public datetime:string

    public like:number

    public ifLike:boolean

    public ifHate:boolean

    public ifReply:boolean

    public lastClicked:number

    public children:any[]

    constructor(author:string, toAuthor:string, avatar:string, content:string, datetime:string, like:number, ifLike:boolean, ifHate:boolean, ifReply:boolean, children:any[]) {
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

    increaseLike() {
        this.like += 1
    }

    decreaseLike() {
        this.like -= 1
    }

    changeLikeState() {
        this.ifLike = !this.ifLike
        if (this.ifLike) {
            this.increaseLike()
        }
        else {
            this.decreaseLike()
        }
        if (this.ifHate) {
            this.ifHate = false;
        }
    }

    changeHateState() {
        this.ifHate = !this.ifHate
        if (this.ifLike) {
            this.ifLike = false;
        }
    }

    changeReplyState(newComment:MyComment, whoClicked:number) {
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

    addComment(item:MyComment, newComment:MyComment) {
        this.ifReply = false
        const tmp = new MyComment('', '', '', '', '', 0, false, false, false, []);
        const date = new Date();
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        tmp.datetime = `${year}-${month}-${day} ${hours}:${minutes}`;
        tmp.content = `回复 @ ${newComment.toAuthor} :${newComment.content}`;
        tmp.avatar = newComment.avatar;
        tmp.author = newComment.author;
        item.children.push(tmp)
        newComment.content = ''
    }
}

export default MyComment;