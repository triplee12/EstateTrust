import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { fetchProfileData, ProfileData } from '../thunks/profileThunk';
import { RootState } from '../store';

interface ProfileState {
  data: ProfileData | null;
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}


const initialState: ProfileState = {
  data: null,
  status: 'idle',
  error: null,
};

// Slice for managing profile state
const profileSlice = createSlice({
  name: 'profile',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProfileData.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchProfileData.fulfilled, (state, action: PayloadAction<ProfileData>) => {
        state.status = 'succeeded';
        state.data = action.payload;
      })
      .addCase(fetchProfileData.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload as string;
      });
  },
});

export const { clearError } = profileSlice.actions;
export const selectProfile = (state:  RootState) => state.profile;
export default profileSlice.reducer;




