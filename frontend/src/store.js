import { configureStore, createSlice } from '@reduxjs/toolkit'
import accountReducer from './states/account/accountSlice'

const userSlice = createSlice({
  name: 'user',
  initialState: null,
  reducers: {
    setUser: (state, action) => action.payload,
  },
});

export const { setUser } = userSlice.actions;

const store = configureStore({
  reducer: {
    user: userSlice.reducer,
    account: accountReducer
  },
});

export default store;
