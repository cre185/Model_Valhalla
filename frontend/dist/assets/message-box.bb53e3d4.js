import{g as x,d as k,e as C,N as q,_ as N,v as H}from"./index.35e9d874.js";/* empty css               *//* empty css              *//* empty css                */import{d as E,C as l,aE as p,aH as r,D as I,aK as R,aJ as M,F as T,aM as f,aN as _,aF as w,G as $,aI as h,bL as J,bM as O,br as Q,bN as Y,ba as W,bO as X,bP as Z,bQ as ee,bR as te,r as se,j as ae,t as ne,c as F,u as oe,aY as re,bd as ie,bS as le,bT as ce,bc as ue}from"./arco.a9e9ea8e.js";import{u as de}from"./loading.992f9f87.js";import{f as me}from"./vue.6f0b04ed.js";/* empty css              *//* empty css               *//* empty css               *//* empty css              *//* empty css               *//* empty css               *//* empty css               */async function ge(o){return await k.get(C("/user/list_message"),{method:"GET",headers:{"Content-Type":"application/json",Authorization:o}})}function _e(o){return k.post("/api/message/read",o)}async function pe(o,d){try{return(await k.get(C(`/user/retrieve/${d}`),{method:"GET",headers:{"Content-Type":"application/json",Authorization:o}})).data.avatar}catch(u){console.error(u);return}}async function ye(o,d){const{data:u}=await ge(x()),y=[];for(let m=0;m<u.msgs.length;m+=1){const e=u.msgs[m],n={msg_id:e.id,msg_type:e.msg_type,src_UserID:e.author,msg_text:"Unknown",msg_content:e.msg_content,msg_title:"Unknown",add_time:e.add_time,read:e.read,avatar:"Unknown",messageType:"0"},c=await k.get(C(`/user/retrieve/${e.author}`),{headers:{Authorization:x()}});e.msg_type==="Upload"?(n.msg_title=d("messageBox.upload.title"),o==="zh-CN"?n.msg_text=`${c.data.username}\u4E0A\u4F20\u4E86\u6570\u636E\u96C6:${e.msg_content.datasetName}`:n.msg_text=`${c.data.username} uploaded the dataset ${e.msg_content.datasetName}`):e.msg_type==="Reply"?(o==="zh-CN"?n.msg_title=`${c.data.username}\u56DE\u590D\u4E86\u4F60\u7684\u8BC4\u8BBA`:n.msg_title=`${c.data.username} replied to your comment`,n.msg_text=e.msg_content.childContent):e.msg_type==="Like"?(n.msg_title=d("messageBox.like.title"),o==="zh-CN"?n.msg_text=`${c.data.username}\u70B9\u8D5E\u4E86\u4F60\u7684\u8BC4\u8BBA\u201C${e.msg_content.likeContent}\u201D`:n.msg_text=`${c.data.username} liked your comment "${e.msg_content.likeContent}"`):e.msg_type==="Feedback"?(n.msg_title=d("messageBox.feedback.title"),await k.get(C(`/dataset/retrieve/${e.msg_content.datasetID}`),{headers:{Authorization:x()}}),o==="zh-CN"?n.msg_text=`\u539F\u56E0:${e.msg_content.feedbackType}\uFF0C\u5177\u4F53\u63CF\u8FF0:${e.msg_content.feedbackContent}`:n.msg_text=`Reason: ${e.msg_content.feedbackType}, Detailed description: ${e.msg_content.feedbackContent}`):e.msg_type==="Report"?(n.msg_title=d("messageBox.report.title"),await k.get(C(`/dataset/retrieve/${e.msg_content.datasetID}`),{headers:{Authorization:x()}}),o==="zh-CN"?n.msg_text=`\u539F\u56E0:${e.msg_content.reportReason}\uFF0C\u5177\u4F53\u63CF\u8FF0:${e.msg_content.reportContent}`:n.msg_text=`Reason: ${e.msg_content.reportReason}, Detailed description: ${e.msg_content.reportContent}`):e.msg_type==="Advice"&&(o==="zh-CN"?(n.msg_title=`${c.data.username}\u63D0\u51FA\u8BC4\u6D4B\u5EFA\u8BAE`,n.msg_text=`\u5177\u4F53\u5185\u5BB9:${e.msg_content.adviceContent}`):(n.msg_title=`${c.data.username} proposed suggestions`,n.msg_text=`Detailed content: ${e.msg_content.adviceContent}`)),n.avatar=await pe(x(),e.author),y.push(n)}return y}const he=["onClick"],fe=["src"],ke={style:{"font-size":"90%"}},De=3,ve=E({__name:"list",props:{renderList:{type:Array,required:!0},unreadCount:{type:Number,default:0},size:{type:String,default:"small"}},emits:["itemClick"],setup(o,{emit:d}){const u=d,y=m=>{u("itemClick",[m])};return(m,e)=>{const n=O,c=q,D=Q,g=Y,L=W,v=X,B=Z,S=ee,z=te;return l(),p(z,{bordered:!1,id:"message-list"},{default:r(()=>[(l(!0),I(R,null,M(o.renderList,i=>(l(),p(S,{key:i.msg_id,"action-layout":"vertical",style:T({opacity:i.read?.5:1})},{extra:r(()=>[i.read===!1?(l(),p(n,{key:0,color:"gray"},{default:r(()=>[f(_(m.$t("messageBox.message.unread")),1)]),_:1})):i.read===!0?(l(),p(n,{key:1,color:"green"},{default:r(()=>[f(_(m.$t("messageBox.message.read")),1)]),_:1})):w("",!0)]),default:r(()=>[$("div",{class:"item-wrap",onClick:A=>y(i)},[h(B,null,J({title:r(()=>[h(L,{size:4,direction:o.size==="small"?"vertical":"horizontal"},{default:r(()=>[$("span",ke,_(i.msg_title),1),h(g,{type:"secondary",style:{fontSize:"80%"}},{default:r(()=>[f(_(i.add_time),1)]),_:2},1024)]),_:2},1032,["direction"])]),description:r(()=>[$("div",null,[h(v,{ellipsis:{rows:1},style:{"font-size":"90%"}},{default:r(()=>[f(_(i.msg_text),1)]),_:2},1024),i.msg_type==="message"?(l(),p(g,{key:0,class:"time-text"},{default:r(()=>[f(_(i.add_time),1)]),_:2},1024)):w("",!0)])]),_:2},[i.avatar?{name:"avatar",fn:r(()=>[h(D,{shape:"circle"},{default:r(()=>[i.avatar?(l(),I("img",{key:0,src:i.avatar},null,8,fe)):(l(),p(c,{key:1}))]),_:2},1024)]),key:"0"}:void 0]),1024)],8,he)]),_:2},1032,["style"]))),128)),o.renderList.length&&o.renderList.length<3?(l(),I("div",{key:0,style:T({height:(De-o.renderList.length)*86+"px"})},null,4)):w("",!0)]),_:1})}}});const xe=N(ve,[["__scopeId","data-v-ebf37e14"]]),Ce={class:"demo-basic",style:{"background-color":"white",width:"100%",height:"100%"}},be=E({__name:"message-box",props:["currentLocale","size"],emits:["changeShowingStatus"],setup(o,{emit:d}){const{t:u}=H.exports.useI18n(),y=o,m=d,e=me(),{loading:n,setLoading:c}=de(!0),D=se("like"),g=ae({renderList:[],messageList:[]});ne(g);const L=F(()=>[{key:"like",title:u("messageBox.tab.title.one")},{key:"comment",title:u("messageBox.tab.title.two")},{key:"system",title:u("messageBox.tab.title.three")}]),v=F(()=>{const t=y.size==="small"?4:3;return D.value==="like"?g.messageList.filter(a=>a.msg_type==="Like").slice(0,t).sort((a,s)=>a.read&&!s.read?-1:1):D.value==="comment"?g.messageList.filter(a=>a.msg_type==="Reply").slice(0,t).sort((a,s)=>a.read&&!s.read?-1:1):g.messageList.filter(a=>a.msg_type!=="Reply"&&a.msg_type!=="Like").slice(0,t).sort((a,s)=>a.read&&!s.read?-1:1)}),B=F(()=>v.value.filter(t=>!t.read).length);async function S(){c(!0),g.messageList=[];try{g.messageList=await ye(y.currentLocale,u)}catch{}finally{c(!1)}}async function z(t){const a=t.map(s=>s.msg_id);await _e({ids:a})}const i=t=>g.messageList.filter(s=>s.msg_type===t&&!s.read),A=t=>{const a=i(t);return a.length?`(${a.length})`:""},U=t=>{m("changeShowingStatus",!1),v.value.length&&z([...t]),k.post(C("/user/check_message"),{id:t[0].msg_id},{headers:{Authorization:x()}});const a=t[0].msg_type;if(a==="Upload"){let s;"targetID"in t[0].msg_content&&(s=t[0].msg_content.targetID),e.push({name:"datasetDetails",params:{toShowDetailsID:s,toShowPanelIndex:1}})}else if(a==="Reply"){let s;"targetID"in t[0].msg_content&&(s=t[0].msg_content.targetID),"contentFlag"in t[0].msg_content&&!t[0].msg_content.contentFlag?e.push({name:"datasetDetails",params:{toShowDetailsID:s,toShowPanelIndex:4}}):e.push({name:"leaderboardDetails",params:{toShowDetailsID:s,toShowPanelIndex:4}})}else if(a==="Like"){let s;"targetID"in t[0].msg_content&&(s=t[0].msg_content.targetID),"likeFlag"in t[0].msg_content&&!t[0].msg_content.likeFlag?e.push({name:"datasetDetails",params:{toShowDetailsID:s,toShowPanelIndex:4}}):e.push({name:"leaderboardDetails",params:{toShowDetailsID:s,toShowPanelIndex:4}})}else if(a==="Feedback"){if("datasetID"in t[0].msg_content){const s=t[0].msg_content.datasetID;e.push({name:"datasetDetails",params:{toShowDetailsID:s,toShowPanelIndex:1}})}}else if(a==="Report"&&"datasetID"in t[0].msg_content){const s=t[0].msg_content.datasetID;console.log(s),e.push({name:"datasetDetails",params:{toShowDetailsID:s,toShowPanelIndex:1}})}},P=()=>{e.push({path:"/user/info"}),m("changeShowingStatus",!1)};return S(),(t,a)=>{const s=ce,V=ue,j=re,K=ie,G=le;return l(),I("div",Ce,[h(G,{style:{display:"block"},loading:oe(n)},{default:r(()=>[h(K,{activeKey:D.value,"onUpdate:activeKey":a[0]||(a[0]=b=>D.value=b),type:"rounded",size:"mini","destroy-on-hide":""},{extra:r(()=>[o.size==="small"?(l(),p(j,{key:0,type:"text",onClick:P},{default:r(()=>[f(_(t.$t("messageBox.viewMore")),1)]),_:1})):w("",!0)]),default:r(()=>[(l(!0),I(R,null,M(L.value,b=>(l(),p(V,{key:b.key},{title:r(()=>[$("span",null,_(b.title)+_(A(b.key)),1)]),default:r(()=>[v.value.length?w("",!0):(l(),p(s,{key:0,status:"404",style:T({marginTop:o.size==="small"?"15%":"18%"})},{subtitle:r(()=>[f(_(t.$t("messageBox.noContent")),1)]),_:1},8,["style"])),h(xe,{"render-list":v.value,"unread-count":B.value,onItemClick:U,size:y.size},null,8,["render-list","unread-count","size"])]),_:2},1024))),128))]),_:1},8,["activeKey"])]),_:1},8,["loading"])])}}});const Ue=N(be,[["__scopeId","data-v-4edd76ca"]]);export{Ue as M,ye as g};
