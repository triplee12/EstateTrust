import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunk, { ThunkMiddleware } from 'redux-thunk';
import authReducer, { AuthActionTypes}  from './reducers/authReducer'; // Import your auth reducer and types here
import assetReducer from './reducers/assetsReducer';

export type RootState = ReturnType<typeof rootReducer>;

const rootReducer = combineReducers({
  auth: authReducer,
  assets: assetReducer,
  // Add other reducers here
});

export const store = createStore(
  rootReducer,
  applyMiddleware(thunk as ThunkMiddleware<RootState, AuthActionTypes>)
);

// // Infer the `RootState` and `AppDispatch` types from the store itself
// export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch