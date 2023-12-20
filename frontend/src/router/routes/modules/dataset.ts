import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

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
      path: 'details',
      name: 'datasetDetails',
      component: () => import('@/views/dataset/components/dataset-performance.vue'),
      meta: {
        locale: 'menu.dataset.details',
        requiresAuth: true,
        roles: ['*'],
      },
    },
  ],
};

export default DATASET;
