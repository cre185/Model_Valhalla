import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const HOME: AppRouteRecordRaw = {
  path: '/home',
  name: 'home',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.home',
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
        locale: 'menu.home.profile',
        requiresAuth: true,
        roles: ['*'],
      },
    },
  ],
};

export default HOME;
