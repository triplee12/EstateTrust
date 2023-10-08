import { createAsyncThunk, SerializedError } from '@reduxjs/toolkit';
import { fetchData, postData, updateData, deleteData } from '../helpers/fetchData';

export interface Monetary {
    acc_name: string;
    acc_number: string;
    amount: string;
    bank_name: string;
    will_to: string;
    note: string;
}

export interface AddMonetaryApiResponse {
    uuid_pk: string;
    acc_name: string;
    acc_number: string;
    amount: string;
    bank_name: string;
    owner_id: string;
    will_to: string;
    note: string;
}

//Get
export const fetchMonetaryAsync = createAsyncThunk('monetary/fetchMonetary', async () => {
  try {
    // Simulating an API call to fetch monetary
    const response = await fetchData('/api/monetary');
    const data = response.data;
    return data as Monetary;
  } catch (error) {
    throw  { name: 'FetchError', message: 'Failed to fetch monetary.', stack: '', code: '' };
  }
});

//Post
export const addMonetaryAsync = createAsyncThunk<AddMonetaryApiResponse, { userData: Monetary, grantorId: string }, { rejectValue: SerializedError }>(
  'monetary/addMonetary',
  async ({ userData, grantorId }, thunkAPI) => {
    try {
        console.log(userData);
      const url = `/monetaries/asset/${grantorId}/create/monetary`;
      const response = await postData<AddMonetaryApiResponse>(url, userData);
      const { uuid_pk } = response.data;
      return { uuid_pk } as AddMonetaryApiResponse;
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
export const updateMonetaryAsync = createAsyncThunk<AddMonetaryApiResponse,{userData: Monetary, grantor_id: string, asset_id: string}, { rejectValue: SerializedError }>(
  'monetary/updateMonetary',
  async ({userData, grantor_id ,asset_id}, thunkAPI) => {
    try {
      const url = `/monetaries/asset/grantor/${grantor_id}/assets/${asset_id}/update`
      const response = await updateData<AddMonetaryApiResponse>(url, userData);
      const {uuid_pk} =  response.data;
      return {uuid_pk} as AddMonetaryApiResponse;
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
export const deleteMonetaryAsync = createAsyncThunk<void, {grantor_id: string, asset_id: string}, { rejectValue: SerializedError }>(
  'monetary/deleteMonetary',
  async ({grantor_id, asset_id}, thunkAPI) => {
    try {
      const url = `/monetaries/asset/grantor/${grantor_id}/assets/${asset_id}/delete`
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