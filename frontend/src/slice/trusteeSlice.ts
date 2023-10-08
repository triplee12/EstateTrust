// import { AddTrusteeApiResponse } from './../thunks/trusteesThunk';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { fetchTrusteeAsync, Trustee, addTrusteeAsync } from '../thunks/trusteeThunk';

interface TrusteeState {
  trustee: Trustee;
  loading: boolean;
  add_status: 'idle' | 'success' | 'error';
  error: string | null;
}

const initialState: TrusteeState = {
  trustee: {} as Trustee,
  loading: false,
  add_status: 'idle',
  error: null,
};

const trusteeSlice = createSlice({
  name: 'trustees',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchTrusteeAsync.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTrusteeAsync.fulfilled, (state, action: PayloadAction<Trustee>) => {
        state.loading = false;
        state.trustee = action.payload;
      })
      .addCase(fetchTrusteeAsync.rejected, (state, action) => {
        // Handling the rejected action and setting the error accordingly
        state.loading = false;
        state.error = action.error?.message || 'Failed to fetch trustees.';
      })
      .addCase(addTrusteeAsync.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addTrusteeAsync.fulfilled, (state) => {
        state.loading = false;
        state.add_status = 'success';
        state.error = null;
      })
      .addCase(addTrusteeAsync.rejected, (state, action) => {
        // Handling the rejected action and setting the error accordingly
        state.loading = false;
        state.error = action.error?.message || 'Failed to fetch trustees.';
      })
  },
});

export default trusteeSlice.reducer;
