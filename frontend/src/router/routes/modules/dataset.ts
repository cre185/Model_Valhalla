import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

// @ts-ignore
const DATASET: AppRouteRecordRaw = {
  path: '/dataset',
  name: 'dataset',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.dataset',
    requiresAuth: true,
    icon: 'icon-layers',
    order: 2,
  },
  children: [
    {
      path: 'details/:toShowDetailsID?/:toShowPanelIndex?',
      props: (route: any) => ({
        toShowDetailsID: route.params.toShowDetailsID,
        toShowPanelIndex: route.params.toShowPanelIndex
      }),
      name: 'datasetDetails',
      component: () => import('@/views/dataset/index.vue'),
      meta: {
        locale: 'menu.dataset.details',
        requiresAuth: true,
        roles: ['*'],
      },
    },
  ]
};

export default DATASET;
