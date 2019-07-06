import { ConvergenceService } from "../convergence-service";

import history from "../history";

export const LOGIN_START = "LOGIN_START";
export const LOGIN_SUCCESS = "LOGIN_SUCCESS";
export const LOGIN_FAILURE = "LOGIN_FAILURE";

export const REGISTER_START = "REGISTER_START";
export const REGISTER_SUCCESS = "REGISTER_SUCCESS";
export const REGISTER_FAILURE = "REGISTER_FAILURE";

export function loginStart(username, password) {
	return dispatch => {
		dispatch({
			type: LOGIN_START,
			username,
			password
		});

		let service = new ConvergenceService();
		service.login(username, password).then(
			() => {
				dispatch(loginSuccess());
				history.push("/home");
			},
			err => {
				dispatch(loginFailure(err.response.data.error.message));
			}
		);
	};
}

export function loginSuccess() {
	return {
		type: LOGIN_SUCCESS
	};
}

export function loginFailure(errorMessage) {
	return {
		type: LOGIN_FAILURE,
		errorMessage
	};
}

export function registerStart(username, password) {
	return dispatch => {
		dispatch({
			type: REGISTER_START,
			username,
			password
		});

		let service = new ConvergenceService();
		service.register(username, password).then(
			() => {
				dispatch(registerSuccess());
				history.push("/home");
			},
			err => {
				dispatch(loginFailure(err.response.data.error.message));
			}
		);
	};
}

export function registerSuccess() {
	return {
		type: REGISTER_SUCCESS
	};
}

export function registerFailure(errorMessage) {
	return {
		type: REGISTER_FAILURE,
		errorMessage
	};
}
