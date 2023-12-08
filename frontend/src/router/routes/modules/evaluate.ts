import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const Evaluate: AppRouteRecordRaw = {
  path: '/evaluate',
  name: 'evaluate',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.evaluate',
    requiresAuth: true,
    icon: 'icon-fire',
    order: 3,
  },
  children: [
    {
      path: 'subjective-evaluation',
      name: 'subjectiveEvaluation',
      component: () =>
        import('@/views/evaluate/subjective-evaluation/index.vue'),
      meta: {
        locale: 'menu.evaluate.subjectiveEvaluation',
        requiresAuth: true,
        roles: ['*'],
      },
    },
    {
      path: 'adversarial-evaluation',
      name: 'adversarialEvaluation',
      component: () =>
        import('@/views/evaluate/adversarial-evaluation/index.vue'),
      meta: {
        locale: 'menu.evaluate.adversarialEvaluation',
        requiresAuth: true,
        roles: ['*'],
      },
    },
  ],
};

export default Evaluate;
