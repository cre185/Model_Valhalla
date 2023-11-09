import axios from 'axios';
import type { RouteRecordNormalized } from 'vue-router';
import { UserState } from '@/store/modules/user/types';

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
  email: string
}

export interface LoginRes {
  jwt: string;
  message: string;
  userID: string;
}

export function login(data: LoginData) {
  return axios.post<LoginRes>('http://localhost:8000/user/login', data);
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

export function verifyPhone(data: {mobile: string}){
  return axios.post('http://localhost:8000/user/send_message', data);
}

export function verifyCode(data: phoneVerifyData){
  return axios.post("http://localhost:8000/user/verify_code", data);
}

export function register(data: any){
  return axios.post("http://localhost:8000/user/register", data);
}
