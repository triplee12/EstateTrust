// profileSlice.ts
import { createAsyncThunk, SerializedError } from '@reduxjs/toolkit';
import { fetchData } from '../helpers/fetchData';


export interface ProfileData {
  uuid_pk: string,
  username: string,
  first_name: string,
  middle_name: string,
  last_name: string,
  email: string,
  phone_number: string,
  date_of_birth: string,
  gender: string,
  created_at: string,
  beneficiaries: [],
  executors: [],
  assets: [],
  monetaries: []
}

// Async thunk for fetching profile data
export const fetchProfileData = createAsyncThunk<ProfileData, string, { rejectValue: SerializedError }>(
  'profile/fetchProfileData',
  async (id, thunkAPI) => {
    try {
      // Modify the URL based on the provided id
      const response = await fetchData(`grantors/account/dashboard/${id}`);
      return response.data as ProfileData;
    } catch (error) {
        if (error instanceof Error) {
        return thunkAPI.rejectWithValue({ message: error.message });
      } else {
        return thunkAPI.rejectWithValue({ message: 'An unknown error occurred.' });
      }
    }
  }
);
