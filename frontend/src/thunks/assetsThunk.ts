import { createAsyncThunk, SerializedError } from '@reduxjs/toolkit';
import { fetchData, postData, updateData, deleteData } from '../helpers/fetchData';

export interface Asset {
    name: string;
    location: string;
    will_to: string;
    // documents: File[];
    note: string;
}

export interface AddAssetsApiResponse {
    uuid_pk: string | '';
    name: string | '';
    location: string | '';
    owner_id: string | '';
    will_to: string | '';
    // documents: File[] | [];
    note: string | '';
    created_at: string | '';
}

//Get
export const fetchAssetsAsync = createAsyncThunk('assets/fetchAssets', async () => {
  try {
    // Simulating an API call to fetch assets
    const response = await fetchData(`/grantor/{grantor_id}/assets`);
    const data = response.data;
    return data as Asset[];
  } catch (error) {
    throw  { name: 'FetchError', message: 'Failed to fetch assets.', stack: '', code: '' };
  }
});

//Post
export const addAssetsAsync = createAsyncThunk<AddAssetsApiResponse, {userData: Asset, grantor_id: string}, { rejectValue: SerializedError }>(
  'assets/addAssets',
  async ({userData, grantor_id}, thunkAPI) => {
    try {
      const url = `assets/${grantor_id}/create/asset`
      const response = await postData<AddAssetsApiResponse>(url, userData);
      const {uuid_pk} =  response.data;
      return {uuid_pk} as AddAssetsApiResponse;
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
export const updateAssetsAsync = createAsyncThunk<AddAssetsApiResponse, {userData: Asset, grantor_id: string, asset_id: string}, { rejectValue: SerializedError }>(
  'assets/updateAssets',
  async ({userData, grantor_id, asset_id}, thunkAPI) => {
    try {
      const url = `assets/${grantor_id}/assets/${asset_id}/update`
      const response = await updateData<AddAssetsApiResponse>(url, userData);
      const {uuid_pk} =  response.data;
      return {uuid_pk} as AddAssetsApiResponse;
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
export const deleteAssetsAsync = createAsyncThunk<void, {grantor_id: string, asset_id: string}, { rejectValue: SerializedError }>(
  'assets/deleteAssets',
  async ({grantor_id, asset_id}, thunkAPI) => {
    const url = `assets/${grantor_id}/assets/${asset_id}/delete`
    try {
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