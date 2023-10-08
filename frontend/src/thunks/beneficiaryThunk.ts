import { createAsyncThunk, SerializedError } from '@reduxjs/toolkit';
import { fetchData, postData, updateData, deleteData } from '../helpers/fetchData';

export interface Beneficiary {
    first_name: string;
    last_name: string;
    middle_name: string;
    relation: string;
}

export interface AddBeneficiaryApiResponse {
    uuid_pk: string | '';
    first_name: string;
    middle_name: string;
    last_name: string;
    relation: string;
    added_by: string;
    created_at: string;
}

//Get
export const fetchBeneficiaryAsync = createAsyncThunk('beneficiary/fetchBeneficiary', async () => {
  try {
    // Simulating an API call to fetch beneficiary
    const response = await fetchData('/api/beneficiary');
    const data = response.data;
    return data as Beneficiary;
  } catch (error) {
    throw  { name: 'FetchError', message: 'Failed to fetch beneficiary.', stack: '', code: '' };
  }
});

//Post
export const addBeneficiaryAsync = createAsyncThunk<AddBeneficiaryApiResponse, {userData: Beneficiary, grantor_id: string}, { rejectValue: SerializedError }>(
  'beneficiary/addBeneficiary',
  async ({userData, grantor_id}, thunkAPI) => {
    console.log(userData);
    try {
      const url = `/beneficiaries/account/${grantor_id}/create/beneficiary`
      const response = await postData<AddBeneficiaryApiResponse>(url, userData);
      const {uuid_pk} =  response.data;
      return {uuid_pk} as AddBeneficiaryApiResponse;
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
export const updateBeneficiaryAsync = createAsyncThunk<AddBeneficiaryApiResponse, Beneficiary, { rejectValue: SerializedError }>(
  'beneficiary/updateBeneficiary',
  async (userData, thunkAPI) => {
    try {
      const response = await updateData<AddBeneficiaryApiResponse>('/your-registration-endpoint', userData);
      const {uuid_pk} =  response.data;
      return {uuid_pk} as AddBeneficiaryApiResponse;
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
export const deleteBeneficiaryAsync = createAsyncThunk<void, {grantor_id: string, bene_id: string}, { rejectValue: SerializedError }>(
  'beneficiary/deleteBeneficiary',
  async ({grantor_id, bene_id}, thunkAPI) => {
    try {
      const url = `/beneficiaries/account/${grantor_id}/beneficiary/${bene_id}/delete`
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