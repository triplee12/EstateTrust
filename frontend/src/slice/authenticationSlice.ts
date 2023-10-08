import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '../store'; // Assuming you have a RootState type
import { loginAsync, logoutAsync, ApiResponse } from '../thunks/authenticationThunk';

// Auth state type
export interface AuthState {
  status: 'loggedout' | 'loading' | 'succeeded' | 'failed';
  accessToken?: string;
  id?: string;
  authenticated: boolean;
  error?: string;
}

// Initial state
const initialState: AuthState = {
  status: 'loggedout',
  authenticated: false,
};

// Auth slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = undefined;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginAsync.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(loginAsync.fulfilled, (state, action: PayloadAction<ApiResponse>) => {
        state.status = 'succeeded';
        state.authenticated = true;
        state.accessToken = action.payload.access_token;
        state.id = action.payload.id;
      })
      .addCase(loginAsync.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload?.message as string;
      })
      .addCase(logoutAsync.fulfilled, (state) => {
        state.status = 'loggedout';
        state.authenticated = false;
        state.accessToken = undefined;
      });
  },
});

// Export actions and reducer
export const { clearError } = authSlice.actions;
export const selectAuth = (state: RootState) => state.auth;
export default authSlice.reducer;
