import axios from 'axios';
import apiCat from '@/api/main';

export async function getUsername(userId: string): Promise<string> {
  try {
    const response = await axios.get(apiCat(`/user/retrieve/${userId}`));
    const responseJson = response.data;
    return responseJson.username;
  } catch (error) {
    console.error('Error fetching username:', error);
    throw error;
  }
}

export async function getRegisterTime(userId: string): Promise<string> {
  try {
    const response = await axios.get(apiCat(`/user/retrieve/${userId}`));
    const responseJson = response.data;
    return responseJson.add_time;
  } catch (error) {
    console.error('Error fetching register time:', error);
    throw error;
  }
}

export async function getAvatar(userId: string): Promise<string> {
  try {
    const response = await axios.get(apiCat(`/user/retrieve/${userId}`));

    const responseJson = response.data;
    return responseJson.avatar;
  } catch (error) {
    console.error('Error fetching avatar:', error);
    throw error;
  }
}

export async function getPhone(userId: string): Promise<string> {
  try {
    const response = await axios.get(apiCat(`/user/retrieve/${userId}`));
    const responseJson = response.data;
    return responseJson.mobile;
  } catch (error) {
    console.error('Error fetching phone number:', error);
    throw error;
  }
}

export async function getEmail(userId: string): Promise<string> {
  try {
    const response = await axios.get(apiCat(`/user/retrieve/${userId}`));
    const responseJson = response.data;
    return responseJson.email;
  } catch (error) {
    console.error('Error fetching email address:', error);
    throw error;
  }
}

export async function getPassword(
  userId: string,
  jwt: string
): Promise<string> {
  try {
    const response = await axios.get(apiCat(`/user/retrieve/${userId}`), {
      headers: {
        Authorization: jwt,
      },
    });

    const responseJson = response.data;
    return responseJson.password;
  } catch (error) {
    console.error('Error fetching password:', error);
    throw error;
  }
}

export async function getUserType(
    userId: string,
    jwt: string
): Promise<string> {
  try {
    const response = await axios.get(apiCat(`/user/retrieve/${userId}`), {
      headers: {
        Authorization: jwt,
      },
    });

    const responseJson = response.data;
    return responseJson.is_admin ? 'admin' : 'user';
  } catch (error) {
    console.error('Error fetching password:', error);
    throw error;
  }
}

interface updateRequest {
  key: string;
}

export async function updateInfo(
  userId: string,
  jwt: string,
  Data: updateRequest,
  key: string
) {
  try {
    const data = { [key]: Data.key };
    const response = await axios.patch(apiCat(`/user/update/${userId}`), data, {
      headers: {
        Authorization: jwt,
      },
    });
  } catch (error) {
    console.error('Error updating information:', error);
    throw error;
  }
}
