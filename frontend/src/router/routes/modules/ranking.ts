import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const HOME: AppRouteRecordRaw = {
  path: '/leaderboard',
  name: 'Leaderboard',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.ranking',
    requiresAuth: true,
    icon: 'icon-bar-chart',
    order: 0,
  },
  children: [
    {
      path: 'details',
      name: 'leaderboardDetails',
      component: () => import('@/views/ranking/index.vue'),
      meta: {
        locale: 'menu.ranking.profile',
        requiresAuth: true,
        roles: ['*'],
      },
    },
  ],
};

export default HOME;
