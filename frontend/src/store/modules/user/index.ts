import { defineStore } from 'pinia';
import {
  login as userLogin,
  loginByPhone as userLoginByPhone,
  logout as userLogout,
  getUserInfo,
  verifyPhone as registerVerifyPhone,
  verifyCode as registerVerifyCode,
  verifyEmail as registerVerifyEmail,
  verifyEmailCode as registerVerifyEmailCode,
  LoginData,
  phoneVerifyData,
  registerData,
  register,
  emailVerifyData,
} from '@/api/user';
import { setToken, clearToken } from '@/utils/auth';
import { removeRouteListener } from '@/utils/route-listener';
import { UserState } from './types';
import useAppStore from '../app';

const useUserStore = defineStore('user', {
  state: (): UserState => ({
    accountId: undefined,
    username: undefined,
    avatar: undefined,
    phone: undefined,
    email: undefined,
    registrationDate: undefined,
    certification: undefined,
    role: '',
  }),

  getters: {
    userInfo(state: UserState): UserState {
      return { ...state };
    },
  },

  actions: {
    switchRoles() {
      return new Promise((resolve) => {
        this.role = this.role === 'user' ? 'admin' : 'user';
        resolve(this.role);
      });
    },

    // Set user's information
    setInfo(partial: Partial<UserState>) {
      this.$patch(partial);
    },

    // Reset user's information
    resetInfo() {
      this.$reset();
    },

    // Get user's information
    async info() {
      const res = await getUserInfo();

      this.setInfo(res.data);
    },

    // Login
    async login(loginForm: LoginData) {
      try {
        const res = await userLogin(loginForm);
        setToken(res.data.jwt);
        this.setInfo({ accountId: res.data.userId });
      } catch (err) {
        clearToken();
        throw err;
      }
    },
    async loginByPhone(loginForm: phoneVerifyData) {
      try {
        const res = await userLoginByPhone(loginForm);
        setToken(res.data.jwt);
        this.setInfo({ accountId: res.data.userId });
      } catch (err) {
        clearToken();
        throw err;
      }
    },
    logoutCallBack() {
      const appStore = useAppStore();
      this.resetInfo();
      clearToken();
      // removeRouteListener();
      appStore.clearServerMenu();
    },
    // Logout
    async logout() {
      try {
        // await userLogout();
      } finally {
        this.logoutCallBack();
      }
    },

    // Verify phone number
    async verifyPhone(phone: string) {
      const data = { mobile: phone };
      await registerVerifyPhone(data);
    },

    async verifyEmail(emailAddress: string) {
      const data = { email: emailAddress };
      await registerVerifyEmail(data);
    },

    async verifyCode(data: phoneVerifyData) {
      await registerVerifyCode(data);
    },

    async verifyEmailCode(data: emailVerifyData) {
      await registerVerifyEmailCode(data);
    },

    async register(data: registerData) {
      await register(data);
    },
  },
});

export default useUserStore;
