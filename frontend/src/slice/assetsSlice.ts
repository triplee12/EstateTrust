// import { AddAssetsApiResponse } from './../thunks/assetsThunk';
import { createSlice, PayloadAction, SerializedError } from '@reduxjs/toolkit';
import { fetchAssetsAsync, Asset, addAssetsAsync } from '../thunks/assetsThunk';

interface AssetState {
  assets: Asset[];
  loading: boolean;
  add_status: 'idle' | 'success' | 'error';
  error: string | null;
}

const initialState: AssetState = {
  assets: [],
  loading: false,
  add_status: 'idle',
  error: null,
};

const assetSlice = createSlice({
  name: 'assets',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchAssetsAsync.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAssetsAsync.fulfilled, (state, action: PayloadAction<Asset[]>) => {
        state.loading = false;
        state.assets = action.payload;
      })
      .addCase(fetchAssetsAsync.rejected, (state, action) => {
        // Handling the rejected action and setting the error accordingly
        state.loading = false;
        state.error = action.error?.message || 'Failed to fetch assets.';
      })
      .addCase(addAssetsAsync.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addAssetsAsync.fulfilled, (state) => {
        state.loading = false;
        state.add_status = 'success';
        state.error = null;
      })
      .addCase(addAssetsAsync.rejected, (state, action) => {
        // Handling the rejected action and setting the error accordingly
        state.loading = false;
        state.error = action.error?.message || 'Failed to fetch assets.';
      })
      // .addCase(fetchAssetsAsync.pending, (state) => {
      //   state.loading = true;
      //   state.error = null;
      // })
      // .addCase(fetchAssetsAsync.fulfilled, (state, action: PayloadAction<Asset[]>) => {
      //   state.loading = false;
      //   state.assets = action.payload;
      // })
      // .addCase(fetchAssetsAsync.rejected, (state, action) => {
      //   // Handling the rejected action and setting the error accordingly
      //   state.loading = false;
      //   state.error = action.error?.message || 'Failed to fetch assets.';
      // });
  },
});

export default assetSlice.reducer;
