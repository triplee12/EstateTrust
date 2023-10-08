import { createStore, applyMiddleware, combineReducers } from 'redux';
import { persistReducer, persistStore } from 'redux-persist';
import storage from 'redux-persist/lib/storage' // defaults to localStorage for web
import thunk, { ThunkMiddleware } from 'redux-thunk';
import authReducer from './slice/authenticationSlice';
import assetReducer from './slice/assetsSlice';
import registerReducer from './slice/registerSlice';
import profileReducer from './slice/profileSlice';
import beneficiaryReducer from './slice/beneficiarySlice';
import monetaryReducer from './slice/monetarySlice';
import trusteeReducer from './slice/trusteeSlice';

export type RootState = ReturnType<typeof rootReducer>;


const persistConfig = {
  key: 'root',
  storage,
}
 

const rootReducer = combineReducers({
  auth: authReducer,
  register: registerReducer,
  assets: assetReducer,
  profile: profileReducer,
  beneficiary: beneficiaryReducer,
  monetary: monetaryReducer,
  trustee: trusteeReducer,
  // Add other reducers here
});

const persistedReducer = persistReducer(persistConfig, rootReducer)
 
export const store = createStore(
  persistedReducer,
  applyMiddleware(thunk as ThunkMiddleware<RootState>)
);

export const persistor = persistStore(store)
// // Infer the `RootState` and `AppDispatch` types from the store itself
// export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch