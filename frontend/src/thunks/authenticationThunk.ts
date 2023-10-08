import { createAsyncThunk, SerializedError } from '@reduxjs/toolkit';
import { postData } from '../helpers/fetchData';
import {removeAuthToken} from '../helpers/apiHelpers';

// Define the login data type
export type LoginData = {
    username: string;
    password: string;
    account_type: string;
};


export interface ApiResponse {
  access_token: string;
  id: string;
}

// Async thunk for login
export const loginAsync = createAsyncThunk<
  ApiResponse,
  LoginData,
  { rejectValue: SerializedError }
>('auth/loginAsync', async (credentials, thunkAPI) => {
  try {
    const response = await postData<{ access_token: string; id: string }>('/auths/account/login', credentials);
    const { access_token, id } = response.data; // Extract accessToken and id from the response data
    return { access_token, id } as ApiResponse; 
  } catch (error) {
    if (error instanceof Error) {
      return thunkAPI.rejectWithValue({ message: error.message });
    } else {
      return thunkAPI.rejectWithValue({ message: 'An unknown error occurred.' });
    }
  }
});

// Async thunk for logout
export const logoutAsync = createAsyncThunk<void, void>('auth/logoutAsync', async () => {
  try {
    // await postData('/auths/account/logout', {});
    removeAuthToken();   
  } catch (error) {
    throw { name: 'LogoutError', message: 'Failed to logout.', stack: '', code: '' };
  }// Perform any necessary cleanup or API calls for logout

});
