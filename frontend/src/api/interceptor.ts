import axios from 'axios';
import type { AxiosRequestConfig, AxiosResponse } from 'axios';
import { Router } from 'vue-router';
import { Message, Modal } from '@arco-design/web-vue';
import { useUserStore } from '@/store';
import { getToken, setToken } from '@/utils/auth';
import { LoginRes } from '@/api/user';
import eventBus from './event-bus';

export interface HttpResponse<T = unknown> {
  status: number;
  msg: string;
  code: number;
  data: T;
}

if (import.meta.env.VITE_API_BASE_URL) {
  axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL;
}

function setupInterceptors(router: Router) {
  axios.interceptors.request.use(
      (config: AxiosRequestConfig) => {
        // let each request carry token
        // this example using the JWT token
        // Authorization is a custom headers key
        // please modify it according to the actual situation
        const token = getToken();
        if (token) {
          if (!config.headers) {
            config.headers = {};
          }
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        // do something
        return Promise.reject(error);
      }
  );
// add response interceptors
  axios.interceptors.response.use(
      (response: AxiosResponse<LoginRes>) => {
        // if the custom code is not 200, it is judged as an error.
        if (response.status !== 200 && response.status !== 201) {
          Message.error({
            content: response.data.message || 'Error',
            duration: 5 * 1000,
          });
          // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
          if (
              [50008, 50012, 50014].includes(response.status)
          ) {
            Modal.error({
              title: 'Confirm logout',
              content:
                  'You have been logged out, you can cancel to stay on this page, or log in again',
              okText: 'Re-Login',
              async onOk() {
                const userStore = useUserStore();

                await userStore.logout();
                window.location.reload();
              },
            });
          }
          return Promise.reject(new Error(response.data.message || 'Error'));
        }
        if (response.data.jwt) {
          setToken(response.data.jwt);
        }
        return response;
      },
      (error) => {
        if (error.response && error.response.status === 408) {
          Message.error({
            content: 'Login Expired',
            duration: 5 * 1000,
          });
          useUserStore().logout();
          eventBus.emit('updateNavbar');
          router.push({
              name: 'Index',
          });
        }
        else {
          Message.error({
            content: error.msg || 'Request Error',
            duration: 5 * 1000,
          });
        }
        return Promise.reject(error);
      }
  );
}

export default function useAxiosInterceptor(router: Router) {
  return  setupInterceptors(router);
}
