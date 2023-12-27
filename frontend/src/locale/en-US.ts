import localeMessageBox from '@/components/navbar/locale/en-US';
import localeLogin from '@/views/login/locale/en-US';
import localeRegister from '@/views/register/locale/en-US';
import localeChange from '@/views/changeInfo/locale/en-US';

import localeRanking from '@/views/ranking/locale/en-US';

import localeDataset from '@/views/dataset/locale/en-US';

import localeSubjectiveEvaluation from '@/views/evaluate/subjective-evaluation/locale/en-US';
import localeAdversarialEvaluation from '@/views/evaluate/adversarial-evaluation/locale/en-US';

import localeStepForm from '@/views/form/step/locale/en-US';
import localeGroupForm from '@/views/form/group/locale/en-US';

import localeBasicProfile from '@/views/profile/basic/locale/en-US';

import localeDataAnalysis from '@/views/visualization/data-analysis/locale/en-US';
import localeMultiDAnalysis from '@/views/visualization/multi-dimension-data-analysis/locale/en-US';

import localeSuccess from '@/views/result/success/locale/en-US';
import localeError from '@/views/result/error/locale/en-US';

import locale403 from '@/views/exception/403/locale/en-US';
import locale404 from '@/views/exception/404/locale/en-US';
import locale500 from '@/views/exception/500/locale/en-US';

import localeUserInfo from '@/views/user/info/locale/en-US';
import localeUserSetting from '@/views/user/setting/locale/en-US';

import localeSettings from './en-US/settings';

export default {
  'menu.home': 'Homepage',
  'menu.home.profile': 'Homepage-Details',
  'menu.ranking': 'Leaderboard',
  'menu.ranking.profile': 'Leaderboard-Details',
  'menu.dataset': 'Dataset',
  'menu.dataset.details': 'Dataset-Details',
  'menu.server.monitor': 'Monitor-Server',
  'menu.evaluate': 'Evaluate',
  'menu.evaluate.adversarialEvaluation': 'Adversarial Evaluation',
  'menu.evaluate.subjectiveEvaluation': 'Subjective Evaluation',
  'menu.result': 'Result',
  'menu.exception': 'Exception',
  'menu.form': 'Form',
  'menu.profile': 'Profile',
  'menu.visualization': 'Data Visualization',
  'menu.user': 'User Center',
  'menu.arcoWebsite': 'Arco Design',
  'menu.faq': 'FAQ',
  'navbar.docs': 'Docs',
  'navbar.action.locale': 'Switch to English',
  'navbar.welcome': 'Welcome back, ',
  'navbar.quit': 'Log Out',
  'logout.success': 'Logout successfully',
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
