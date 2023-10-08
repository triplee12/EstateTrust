import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { fetchBeneficiaryAsync, Beneficiary, addBeneficiaryAsync } from '../thunks/beneficiaryThunk';

interface BeneficiaryState {
  beneficiary: Beneficiary;
  loading: boolean;
  add_status: 'idle' | 'success' | 'error';
  error: string | null;
}

const initialState: BeneficiaryState = {
  beneficiary: {} as Beneficiary,
  loading: false,
  add_status: 'idle',
  error: null,
};

const beneficiarySlice = createSlice({
  name: 'beneficiary',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchBeneficiaryAsync.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchBeneficiaryAsync.fulfilled, (state, action: PayloadAction<Beneficiary>) => {
        state.loading = false;
        state.beneficiary = action.payload;
      })
      .addCase(fetchBeneficiaryAsync.rejected, (state, action) => {
        // Handling the rejected action and setting the error accordingly
        state.loading = false;
        state.error = action.error?.message || 'Failed to fetch assets.';
      })
      .addCase(addBeneficiaryAsync.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addBeneficiaryAsync.fulfilled, (state) => {
        state.loading = false;
        state.add_status = 'success';
        state.error = null;
      })
      .addCase(addBeneficiaryAsync.rejected, (state, action) => {
        // Handling the rejected action and setting the error accordingly
        state.loading = false;
        state.error = action.error?.message || 'Failed to fetch assets.';
      })
  },
});

export default beneficiarySlice.reducer;
