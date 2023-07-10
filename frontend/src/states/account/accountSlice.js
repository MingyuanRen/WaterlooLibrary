import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import accountService from './accountService'

// get user from local storage
const userEmail = localStorage.getItem('email')

const initialState = {
    name: "",
    email: '',
    phone: null,
    uid: null,
    isError: false,
    isSuccess: false,
    isLoading: false,
    message: '',
    bookRecords: []
}
// Register new user
export const accountInfo = createAsyncThunk(
    'userinfo/account',
    async (userEmail, thunkAPI) => {
        try {
            return await accountService.findUserInfo(userEmail)
        } catch (error) {
            const message =
                (error.response &&
                error.response.data &&
                error.response.data.message) ||
                error.message ||
                error.toString()

            return thunkAPI.rejectWithValue(message)
        }
    }
)

export const getBooksRecords = createAsyncThunk(
    'userinfo/bookstatus',
    async (userEmail, thunkAPI) => {
        try {
            return await accountService.getBooksRecords(userEmail)
        } catch (error) {
            const message =
                (error.response &&
                error.response.data &&
                error.response.data.message) ||
                error.message ||
                error.toString()

            return thunkAPI.rejectWithValue(message)
        }
    }
)

export const accountSlice = createSlice({
    name: 'accountInfo',
    initialState,
    reducers: {
      reset: (state) => {
        state.isLoading = false
        state.isError = false
        state.isSuccess = false
        state.message = ''
        state.bookRecords = []
        state.uid = null
      },
    },
    extraReducers: (builder) => {
      builder
        .addCase(accountInfo.pending, (state) => {
          state.isLoading = true
        })
        .addCase(accountInfo.fulfilled, (state, action) => {
          state.isLoading = false
          state.isSuccess = true
          state.name = action.payload.name
          state.email = action.payload.email
          state.phone = action.payload.phone
          state.uid = action.payload.uid
        })
        .addCase(accountInfo.rejected, (state, action) => {
          state.isLoading = false
          state.isError = true
          state.message = action.payload
          state.name = null
          state.email = null
          state.phone = null
          state.uid = null
        })
        .addCase(getBooksRecords.pending, (state) => {
          state.isLoading = true
        })
        .addCase(getBooksRecords.fulfilled, (state, action) => {
          state.isLoading = false
          state.isSuccess = true
          state.bookRecords = action.payload
        })
        .addCase(getBooksRecords.rejected, (state, action) => {
          state.isLoading = false
          state.isError = true
          state.message = action.payload
          state.bookRecords = []
        })
    },
})

export const { reset } = accountSlice.actions
export default accountSlice.reducer