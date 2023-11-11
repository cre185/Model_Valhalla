import axios from 'axios';

export async function getUsername(
  userId: string,
  jwt: string
): Promise<string> {
  try {
    const response = await axios.get(
      `http://localhost:8000/user/retrieve/${userId}`,
      {
        headers: {
          Authorization: jwt,
        },
      }
    );

    const responseJson = response.data;
    return responseJson.username;
  } catch (error) {
    console.error('Error fetching username:', error);
    throw error;
  }
}

export async function getRegisterTime(
  userId: string,
  jwt: string
): Promise<string> {
  try {
    const response = await axios.get(
      `http://localhost:8000/user/retrieve/${userId}`,
      {
        headers: {
          Authorization: jwt,
        },
      }
    );

    const responseJson = response.data;
    return responseJson.add_time;
  } catch (error) {
    console.error('Error fetching username:', error);
    throw error;
  }
}

export async function getAvatar(userId: string, jwt: string): Promise<string> {
  try {
    const response = await axios.get(
      `http://localhost:8000/user/retrieve/${userId}`,
      {
        headers: {
          Authorization: jwt,
        },
      }
    );

    const responseJson = response.data;
    return responseJson.avatar;
  } catch (error) {
    console.error('Error fetching username:', error);
    throw error;
  }
}

export async function getPhone(userId: string, jwt: string): Promise<string> {
  try {
    const response = await axios.get(
      `http://localhost:8000/user/retrieve/${userId}`,
      {
        headers: {
          Authorization: jwt,
        },
      }
    );

    const responseJson = response.data;
    return responseJson.mobile;
  } catch (error) {
    console.error('Error fetching username:', error);
    throw error;
  }
}

export async function getEmail(userId: string, jwt: string): Promise<string> {
  try {
    const response = await axios.get(
      `http://localhost:8000/user/retrieve/${userId}`,
      {
        headers: {
          Authorization: jwt,
        },
      }
    );

    const responseJson = response.data;
    return responseJson.email;
  } catch (error) {
    console.error('Error fetching username:', error);
    throw error;
  }
}
