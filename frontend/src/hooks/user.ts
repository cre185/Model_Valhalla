import { useRouter } from 'vue-router';
import { Message } from '@arco-design/web-vue';

import { useUserStore } from '@/store';

export default function useUser() {
  const router = useRouter();
  const userStore = useUserStore();
  const logout = async () => {
    await userStore.logout();
    await router.push({
      name: 'Index',
    });
  };
  return {
    logout,
  };
}
