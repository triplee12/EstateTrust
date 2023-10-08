// import { AddMonetaryApiResponse } from './../thunks/monetaryThunk';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { fetchMonetaryAsync, Monetary, addMonetaryAsync } from '../thunks/monetaryThunk';

interface MonetaryState {
  monetary: Monetary;
  loading: boolean;
  add_status: 'idle' | 'success' | 'error';
  error: string | null;
}

const initialState: MonetaryState = {
  monetary: {} as Monetary,
  loading: false,
  add_status: 'idle',
  error: null,
};

const monetarySlice = createSlice({
  name: 'monetary',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchMonetaryAsync.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchMonetaryAsync.fulfilled, (state, action: PayloadAction<Monetary>) => {
        state.loading = false;
        state.monetary = action.payload;
      })
      .addCase(fetchMonetaryAsync.rejected, (state, action) => {
        // Handling the rejected action and setting the error accordingly
        state.loading = false;
        state.error = action.error?.message || 'Failed to fetch monetary.';
      })
      .addCase(addMonetaryAsync.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addMonetaryAsync.fulfilled, (state) => {
        state.loading = false;
        state.add_status = 'success';
        state.error = null;
      })
      .addCase(addMonetaryAsync.rejected, (state, action) => {
        // Handling the rejected action and setting the error accordingly
        state.loading = false;
        state.error = action.error?.message || 'Failed to fetch monetary.';
      })
  },
});

export default monetarySlice.reducer;
