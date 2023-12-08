import Mock from 'mockjs';

import './user';
import './message-box';

import '@/views/evaluate/adversarial-evaluation/mock';
import '@/views/evaluate/subjective-evaluation/mock';

import '@/views/form/step/mock';

import '@/views/profile/basic/mock';

import '@/views/visualization/data-analysis/mock';
import '@/views/visualization/multi-dimension-data-analysis/mock';

import '@/views/user/info/mock';
import '@/views/user/setting/mock';

Mock.setup({
  timeout: '600-1000',
});
