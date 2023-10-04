// authActions.ts

import { ThunkAction } from 'redux-thunk';
import { RootState } from '../store'; // Import your RootState
import { AuthActionTypes } from './authReducer';
import axios from 'axios';

function authenticateUser(username: string, password: string) {
  // Make an API call here to authenticate the user
  axios.post('/api/login', { username, password });
  // Assuming the credentials are valid
  return Promise.resolve({ username });
}

async function setupProfile(data: object) {
  if (localStorage.getItem('authToken'))
    localStorage.setItem('username', data.username);
}

export const login = (
  username: string,
  password: string
): ThunkAction<void, RootState, null, AuthActionTypes> => async (dispatch) => {
  try {
    // Make an API call to authenticate the user
    // Assuming you have an async function for this
    const user = await authenticateUser(username, password);
    dispatch({ type: 'LOGIN_SUCCESS', payload: user });
    await setupProfile(user);
  } catch (error) {
    if (error instanceof Error) {
      dispatch({ type: 'LOGIN_FAILURE', payload: error.message });
    } else {
      dispatch({ type: 'LOGIN_FAILURE', payload: 'An unknown error occurred.' });
    }
  }
};

export const logout = (): AuthActionTypes => ({
  type: 'LOGOUT',
});
