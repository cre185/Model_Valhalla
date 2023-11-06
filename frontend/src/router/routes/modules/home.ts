import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const HOME: AppRouteRecordRaw = {
  path: '/home',
  name: 'home',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: '主页',
    requiresAuth: true,
    icon: 'icon-home',
    order: 0,
  },
  children: [
    {
      path: 'index',
      name: 'Index',
      component: () => import('@/views/home/index.vue'),
      meta: {
        locale: '主页详情',
        requiresAuth: true,
        roles: ['*'],
      },
    },
  ],
};

export default HOME;
