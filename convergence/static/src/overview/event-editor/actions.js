import { ConvergenceService } from "../../convergence-service";
import history from "../../history";

export const EVENT_EDIT_START = "EVENT_EDIT_START";
export const EVENT_EDIT_END = "EVENT_EDIT_END";
export const EVENT_EDIT_ADD_USER = "EVENT_EDIT_ADD_USER";
export const EVENT_EDIT_REMOVE_USER = "EVENT_EDIT_REMOVE_USER";
export const EVENT_SAVE_START = "EVENT_SAVE_START";
export const EVENT_SAVE_END = "EVENT_SAVE_END";
export const EVENT_SAVE_FAIL = "EVENT_SAVE_FAIL";

/**
 * Starts an event save action chain. Dispatches EVENT_SAVE_START,
 * and either EVENT_SAVE_END or EVENT_SAVE_FAIL.
 * Upon success an event will be created on the service side.
 * @param  {Object} event an event object
 * @return {Function} thunk
 */
export function eventSaveStart(event) {
	return (dispatch, getState) => {
		dispatch({
			type: EVENT_SAVE_START,
			event
		});

		let service = new ConvergenceService();
		service
			.createEvent(event)
			.then(resp => {
				return service.inviteUsers(
					resp.data.data.id,
					getState().overview.eventEditor.users
				);
			})
			.then(
				resp => {
					dispatch(eventSaveEnd(event));
				},
				err => {
					// TODO: display an actual error message
					eventSaveFail("Can't save event.");
				}
			);
	};
}

/**
 * Creates an EVENT_SAVE_END action.
 * @param  {Object} event
 * @return {Object} action
 */
export function eventSaveEnd(event) {
	return {
		type: EVENT_SAVE_END,
		event
	};
}

/**
 * Creates an EVENT_SAVE_FAIL action.
 * @param  {String} errorMessage
 * @return {Object} action
 */
export function eventSaveFail(errorMessage) {
	return {
		type: EVENT_SAVE_FAIL,
		errorMessage
	};
}

/**
 * Dispatches EVENT_EDIT_START action. As a result,
 * event editor screen will be presented.
 * @param  {Number|null} id an event ID
 * @return {Function} thunk
 */
export function eventEditStart(id) {
	return dispatch => {
		dispatch({
			type: EVENT_EDIT_START
		});
		if (id) {
			history.push(`/event/edit/${id}`);
			return;
		}

		history.push("event/new");
	};
}

/**
 * Dispatches EVENT_EDIT_END, which closes event editor screen.
 * @return {Function} thunk
 */
export function eventEditEnd() {
	return dispatch => {
		dispatch({
			type: EVENT_EDIT_END
		});
		history.goBack();
	};
}

/**
 * Dispatches EVENT_EDIT_ADD_USER action. This will add a user (if valid) to
 * the currently edited invitee list.
 * @param  {String} username
 * @return {Function} thunk
 */
export function eventEditAddUser(username) {
	return (dispatch, getState) => {
		if (!shouldAddUser(username, getState().overview.eventEditor.users)) {
			return;
		}
		dispatch({
			type: EVENT_EDIT_ADD_USER,
			username
		});
	};
}

/**
 * Creates an EVENT_EDIT_REMOVE_USER action. This will remove
 * a user with a given name from a currently edited invitee list.
 * @param  {String} username
 * @return {Object} action
 */
export function eventEditRemoveUser(username) {
	return {
		type: EVENT_EDIT_REMOVE_USER,
		username
	};
}

function shouldAddUser(username, users) {
	return (
		username &&
		username.length &&
		users.every(u => u.toLowerCase() !== username.toLowerCase())
	);
}
