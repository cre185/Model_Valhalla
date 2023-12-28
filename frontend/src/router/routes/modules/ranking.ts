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
    order: 1,
  },
  children: [
    {
      path: 'details/:toShowDetailsID?/:toShowPanelIndex?',
      props: (route: any) => ({
        toShowDetailsID: route.params.toShowDetailsID,
        toShowPanelIndex: route.params.toShowPanelIndex
      }),
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
