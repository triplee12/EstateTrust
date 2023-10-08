import { createSlice } from '@reduxjs/toolkit';
import { RootState } from '../store'; // Assuming you have a RootState type
import { registerAsync } from '../thunks/registerThunks';

// Auth state type
export interface AuthState {
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error?: string;
}

// Initial state
const initialState: AuthState = {
  status: 'idle',
};

// Auth slice
const registerSlice = createSlice({
  name: 'register',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = undefined;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(registerAsync.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(registerAsync.fulfilled, (state) => {
        state.status = 'succeeded';
      })
      .addCase(registerAsync.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload?.message as string;
      })
  },
});

// Export actions and reducer
export const { clearError } = registerSlice.actions;
export const registerAuth = (state: RootState) => state.register;
export default registerSlice.reducer;
