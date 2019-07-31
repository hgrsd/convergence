import {
	LOGIN_START,
	LOGIN_END,
	LOGIN_FAIL,
	LOGIN_CHECK,
	REGISTER_START,
	REGISTER_END,
	REGISTER_FAIL
} from "./actions";

const initialState = {
	isLoggedIn: false,
	isLoggingIn: false,
	isRegistering: false,
	isBusy: false,
	username: "",
	userId: null,
	errorMessage: null
};

export function loginReducer(state = initialState, action) {
	switch (action.type) {
		case LOGIN_CHECK:
			return {
				...state,
				isLoggedIn: action.isLoggedIn,
				userId: action.userId
			};
		case LOGIN_START:
			return {
				...state,
				isLoggingIn: true,
				isBusy: true,
				username: action.username
			};
		case LOGIN_FAIL:
			return {
				...state,
				isLoggingIn: false,
				isLoggedIn: false,
				isBusy: false,
				errorMessage: action.errorMessage
			};
		case LOGIN_END:
			return {
				...state,
				userId: action.userId,
				isLoggingIn: false,
				isLoggedIn: true,
				isBusy: false
			};
		case REGISTER_START:
			return {
				...state,
				isRegistering: true,
				isBusy: true,
				username: action.username
			};
		case REGISTER_FAIL:
			return {
				...state,
				isRegistering: false,
				isLoggedIn: false,
				isBusy: false,
				errorMessage: action.errorMessage
			};
		case REGISTER_END:
			return {
				...state,
				userId: action.userId,
				isRegistering: false,
				isLoggedIn: true,
				isBusy: false
			};
	}

	return state;
}
