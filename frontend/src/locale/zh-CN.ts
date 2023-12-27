import localeMessageBox from '@/components/navbar/locale/zh-CN';
import localeLogin from '@/views/login/locale/zh-CN';
import localeRegister from '@/views/register/locale/zh-CN';
import localeChange from '@/views/changeInfo/locale/zh-CN';

import localeRanking from '@/views/ranking/locale/zh-CN';

import localeDataset from '@/views/dataset/locale/zh-CN';

import localeSubjectiveEvaluation from '@/views/evaluate/subjective-evaluation/locale/zh-CN';
import localeAdversarialEvaluation from '@/views/evaluate/adversarial-evaluation/locale/zh-CN';

import localeStepForm from '@/views/form/step/locale/zh-CN';
import localeGroupForm from '@/views/form/group/locale/zh-CN';

import localeBasicProfile from '@/views/profile/basic/locale/zh-CN';

import localeDataAnalysis from '@/views/visualization/data-analysis/locale/zh-CN';
import localeMultiDAnalysis from '@/views/visualization/multi-dimension-data-analysis/locale/zh-CN';

import localeSuccess from '@/views/result/success/locale/zh-CN';
import localeError from '@/views/result/error/locale/zh-CN';

import locale403 from '@/views/exception/403/locale/zh-CN';
import locale404 from '@/views/exception/404/locale/zh-CN';
import locale500 from '@/views/exception/500/locale/zh-CN';

import localeUserInfo from '@/views/user/info/locale/zh-CN';
import localeUserSetting from '@/views/user/setting/locale/zh-CN';

import localeSettings from './zh-CN/settings';

export default {
  'menu.home': '主页',
  'menu.home.profile': '主页详情',
  'menu.ranking': '排行榜',
  'menu.ranking.profile': '排行榜详情',
  'menu.dataset': '数据集',
  'menu.dataset.details': '数据集详情',
  'menu.evaluate': '评测',
  'menu.evaluate.adversarialEvaluation': '对抗评测',
  'menu.evaluate.subjectiveEvaluation': '主观评测',
  'menu.result': '结果页',
  'menu.exception': '异常页',
  'menu.form': '表单页',
  'menu.profile': '详情页',
  'menu.visualization': '数据可视化',
  'menu.user': '个人中心',
  'menu.arcoWebsite': 'Arco Design',
  'menu.faq': '常见问题',
  'navbar.docs': '文档中心',
  'navbar.action.locale': '切换为中文',
  'navbar.welcome': '欢迎回来，',
  'navbar.quit': '退出登录',
  'logout.success': '登出成功',
  ...localeSettings,
  ...localeMessageBox,
  ...localeLogin,
  ...localeRegister,
  ...localeChange,
  ...localeRanking,
  ...localeDataset,

  ...localeSubjectiveEvaluation,
  ...localeAdversarialEvaluation,
  ...localeStepForm,
  ...localeGroupForm,
  ...localeBasicProfile,
  ...localeDataAnalysis,
  ...localeMultiDAnalysis,
  ...localeSuccess,
  ...localeError,
  ...locale403,
  ...locale404,
  ...locale500,
  ...localeUserInfo,
  ...localeUserSetting,
};
