import { createAsyncThunk, SerializedError } from '@reduxjs/toolkit';
import { fetchData, postData, updateData, deleteData } from '../helpers/fetchData';

export interface Trustee {
    first_name: string;
    last_name: string;
    middle_name: string;
    username: string;
    email: string;
    phone_number: string;
    password: string;
    relation: string;
    added_by: string;
    note: string;
}

export interface AddTrusteeApiResponse {
    uuid_pk: string | '';
    username: string;
    first_name: string;
    middle_name: string;
    last_name: string;
    email: string;
    phone_number: string;
    relation: string;
    added_by: string;
    created_at: string;
}

//Get
export const fetchTrusteeAsync = createAsyncThunk('trustee/fetchTrustee', async () => {
  try {
    // Simulating an API call to fetch trustee
    const response = await fetchData('/api/trustee');
    const data = response.data;
    return data as Trustee;
  } catch (error) {
    throw  { name: 'FetchError', message: 'Failed to fetch trustee.', stack: '', code: '' };
  }
});

//Post
export const addTrusteeAsync = createAsyncThunk<AddTrusteeApiResponse, {userData: Trustee, grantorId: string}, { rejectValue: SerializedError }>(
  'trustee/addTrustee',
  async ({userData, grantorId}, thunkAPI) => {
    try {
      console.log(userData);
      const url = `trustees/account/${grantorId}/create/trustee`
      const response = await postData<AddTrusteeApiResponse>(url, userData);
      const {uuid_pk} =  response.data;
      return {uuid_pk} as AddTrusteeApiResponse;
    } catch (error) {
      if (error instanceof Error) {
        return thunkAPI.rejectWithValue({ message: error.message });
      } else {
        return thunkAPI.rejectWithValue({ message: 'An unknown error occurred.' });
      }
    }
  }
);

//Update
export const updateTrusteeAsync = createAsyncThunk<AddTrusteeApiResponse, Trustee, { rejectValue: SerializedError }>(
  'trustee/updateTrustee',
  async (userData, thunkAPI) => {
    try {
      const response = await updateData<AddTrusteeApiResponse>('/your-registration-endpoint', userData);
      const {uuid_pk} =  response.data;
      return {uuid_pk} as AddTrusteeApiResponse;
    } catch (error) {
      if (error instanceof Error) {
        return thunkAPI.rejectWithValue({ message: error.message });
      } else {
        return thunkAPI.rejectWithValue({ message: 'An unknown error occurred.' });
      }
    }
  }
);

//Delete
export const deleteTrusteeAsync = createAsyncThunk<void, {grantor_id: string, trustee_id: string}, { rejectValue: SerializedError }>(
  'trustee/deleteTrustee',
  async ({grantor_id, trustee_id}, thunkAPI) => {
    try {
      const url = `trustees/account/${grantor_id}/trustees/${trustee_id}/delete`;
      await deleteData(url);
    } catch (error) {
      if (error instanceof Error) {
        return thunkAPI.rejectWithValue({ message: error.message });
      } else {
        return thunkAPI.rejectWithValue({ message: 'An unknown error occurred.' });
      }
    }
  },
);