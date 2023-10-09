// registrationThunks.ts
import { createAsyncThunk, SerializedError } from '@reduxjs/toolkit';
import { postData } from '../helpers/fetchData';

// Define your API response type here
export interface ApiResponse {
  message: string;
}

// Define your registration data type here
export interface RegistrationData {
    first_name: string | '';
    last_name: string | '';
    middle_name: string | '';
    username: string | '';
    email: string | '';
    phone_number: string | '';
    date_of_birth: string | '';
    gender: string | '';
    password: string | '';
}

// Async thunk for registration
export const registerAsync = createAsyncThunk<ApiResponse, RegistrationData, { rejectValue: SerializedError }>(
  'registration/registerAsync',
  async (userData, thunkAPI) => {
    try {
      const response = await postData<ApiResponse>('/grantors/account/create', userData);
      const {message} =  response.data;
      return {message} as ApiResponse;
    } catch (error) {
      if (error instanceof Error) {
        return thunkAPI.rejectWithValue({ message: error.message });
      } else {
        return thunkAPI.rejectWithValue({ message: 'An unknown error occurred.' });
      }
    }
  }
);
