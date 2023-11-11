export type RoleType = '' | '*' | 'admin' | 'user';
export interface UserState {
  accountId?: string,
  username?: string;
  avatar?: string;
  phone?: string;
  email?: string;
  registrationDate?: string;
  certification?: number;
  role: RoleType;
}
