import { ConvergenceService } from "../convergence-service";

import history from "../history";

export const LOGIN_CHECK = "LOGIN_CHECK";
export const LOGIN_START = "LOGIN_START";
export const LOGIN_END = "LOGIN_END";
export const LOGIN_FAIL = "LOGIN_FAIL";

export const REGISTER_START = "REGISTER_START";
export const REGISTER_END = "REGISTER_END";
export const REGISTER_FAIL = "REGISTER_FAIL";

/**
 * Checks if user is logged in. Returns an action with
 * `isLoggedIn` set to true or false.
 * @return {Object} action
 */
export function loginCheck() {
	const service = new ConvergenceService();
	const userId = service.loginCheck();

	return {
		type: LOGIN_CHECK,
		isLoggedIn: userId !== null,
		userId
	};
}

/**
 * Kicks off a login action chain. Results in LOGIN_START,
 * and either LOGIN_END or LOGIN_FAIL to be dispatched.
 * @param  {string} username
 * @param  {string} password
 * @return {Function} thunk
 */
export function loginStart(username, password) {
	return dispatch => {
		dispatch({
			type: LOGIN_START,
			username,
			password
		});

		const service = new ConvergenceService();
		service.login(username, password).then(
			resp => {
				dispatch(loginEnd(resp.data.data.user_id));
				history.push("/home");
			},
			err => {
				dispatch(loginFail(err.response.data.error.message));
			}
		);
	};
}

/**
 * Creates LOGIN_END action with a given user ID.
 * @param  {Number} userId logged in user ID
 * @return {Object} action
 */
export function loginEnd(userId) {
	return {
		type: LOGIN_END,
		userId
	};
}

/**
 * Creates a LOGIN_FAIL action with a given optional error message.
 * @param  {string|null} errorMessage
 * @return {Object} action
 */
export function loginFail(errorMessage) {
	return {
		type: LOGIN_FAIL,
		errorMessage
	};
}

/**
 * Starts a chain of registration actions. Dispatches REGISTER_START,
 * and either REGISTER_END or REGISTER_FAIL.
 * @param  {string} username
 * @param  {string} password
 * @return {Function} thunk
 */
export function registerStart(username, password) {
	return dispatch => {
		dispatch({
			type: REGISTER_START,
			username,
			password
		});

		const service = new ConvergenceService();
		service.register(username, password).then(
			resp => {
				dispatch(registerEnd(resp.data.data.id));
				history.push("/home");
			},
			err => {
				dispatch(registerFail(err.response.data.error.message));
			}
		);
	};
}

/**
 * Creates a REGISTER_END action with a registered user ID.
 * @param  {Number} userId
 * @return {Object} action
 */
export function registerEnd(userId) {
	return {
		type: REGISTER_END,
		userId
	};
}

/**
 * Creates a REGISTER_FAIL action with an optional error message.
 * @param  {string|null} errorMessage
 * @return {Object} action
 */
export function registerFail(errorMessage) {
	return {
		type: REGISTER_FAIL,
		errorMessage
	};
}
