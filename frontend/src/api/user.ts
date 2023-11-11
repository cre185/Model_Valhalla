import axios from 'axios';
import type { RouteRecordNormalized } from 'vue-router';
import { UserState } from '@/store/modules/user/types';
import apiCat from '@/api/main';

export interface LoginData {
  username: string;
  password: string;
}

export interface phoneVerifyData {
  mobile: string;
  code: string;
}

export interface registerData {
  username: string;
  password: string;
  mobile: string;
  email: string;
  is_admin: boolean
}

export interface LoginRes {
  jwt: string;
  message: string;
  userId: string;
}

export function login(data: LoginData) {
  return axios.post<LoginRes>(apiCat('/user/login'), data);
}

export function loginByPhone(data: phoneVerifyData) {
  return axios.post<LoginRes>(apiCat('/user/login_with_verify_code'), data);
}

export function logout() {
  return axios.post<LoginRes>('/api/user/logout');
}

export function getUserInfo() {
  return axios.post<UserState>('/api/user/info');
}

export function getMenuList() {
  return axios.post<RouteRecordNormalized[]>('/api/user/menu');
}

export function verifyPhone(data: { mobile: string }) {
  return axios.post(apiCat('/user/send_message'), data);
}

export function verifyCode(data: phoneVerifyData) {
  return axios.post(apiCat('/user/verify_code'), data);
}

export function register(data: any) {
  return axios.post(apiCat('/user/register'), data);
}
