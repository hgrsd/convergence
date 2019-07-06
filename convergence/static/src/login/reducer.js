import {
	LOGIN_START,
	LOGIN_SUCCESS,
	LOGIN_FAILURE,
	REGISTER_START,
	REGISTER_SUCCESS,
	REGISTER_FAILURE
} from "./actions";

const initialState = {
	isLoggedIn: false,
	isLoggingIn: false,
	isRegistering: false,
	isBusy: false,
	username: "",
	errorMessage: null
};

export function loginReducer(state = initialState, action) {
	switch (action.type) {
		case LOGIN_START:
			return { ...state,
				isLoggingIn: true,
				isBusy: true,
				username: action.username
			};
		case LOGIN_FAILURE:
			return { ...state,
				isLoggingIn: false,
				isLoggedIn: false,
				isBusy: false,
				errorMessage: action.errorMessage
			};
		case LOGIN_SUCCESS:
			return { ...state,
				isLoggingIn: false,
				isLoggedIn: true,
				isBusy: false
			};
		case REGISTER_START:
			return { ...state,
				isRegistering: true,
				isBusy: true,
				username: action.username
			};
		case REGISTER_FAILURE:
			return { ...state,
				isRegistering: false,
				isLoggedIn: false,
				isBusy: false,
				errorMessage: action.errorMessage
			};
		case REGISTER_SUCCESS:
			return { ...state,
				isRegistering: false,
				isLoggedIn: true,
				isBusy: false
			};
	}

	return state;
}