import { ConvergenceService } from "../../convergence-service";

export const EVENT_LIST_LOAD_START = "EVENT_LIST_LOAD_START";
export const EVENT_LIST_LOAD_END = "EVENT_LIST_LOAD_END";
export const EVENT_LIST_LOAD_FAIL = "EVENT_LIST_LOAD_FAIL";

export const EVENT_LEAVE_START = "EVENT_LEAVE_START";
export const EVENT_LEAVE_END = "EVENT_LEAVE_END";
export const EVENT_LEAVE_FAIL = "EVENT_LEAVE_FAIL";
export const EVENT_DELETE_START = "EVENT_DELETE_START";
export const EVENT_DELETE_END = "EVENT_DELETE_END";
export const EVENT_DELETE_FAIL = "EVENT_DELETE_FAIL";

/**
 * Kicks off an action chain, which loads contents of the event list.
 * Upon success will add an array of user's current 
 * events (owned and participated) to the state.
 * @return {Function} thunk
 */
export function eventListLoadStart() {
	return (dispatch, getState) => {
		dispatch({
			type: EVENT_LIST_LOAD_START
		});

		let service = new ConvergenceService();

		service.getEvents().then(
			resp => {
				dispatch(eventListLoadEnd(resp.data.data, getState().login.userId));
				return resp;
			},
			err => {
				dispatch(eventListLoadFail());
			}
		);
	};
}

/**
 * Creates an EVENT_LIST_LOAD_END action with given events and current user ID.
 * TODO: consider removing userID, since it should be known by this point.
 * @param  {Array} events
 * @param  {Number} userId
 * @return {Object} action
 */
export function eventListLoadEnd(events, userId) {
	return {
		type: EVENT_LIST_LOAD_END,
		events,
		userId
	};
}

/**
 * Creates an EVENT_LIST_LOAD_FAIL action.
 * TODO: add error message
 * @return {Object} action
 */
export function eventListLoadFail() {
	return {
		type: EVENT_LIST_LOAD_FAIL
	};
}

/**
 * Starts an event leaving action chain. Dispatches EVENT_LEAVE_START,
 * and either EVENT_LEAVE_END or EVENT_LEAVE_FAIL.
 * @param  {Number} eventId
 * @return {Function} thunk
 */
export function eventLeaveStart(eventId) {
	return (dispatch, getState) => {
		dispatch({
			type: EVENT_LEAVE_START,
			eventId
		});

		let service = new ConvergenceService();
		service.leaveEvent(eventId, getState().login.userId).then(
			resp => {
				dispatch(eventLeaveEnd(eventId));
			},
			err => {
				dispatch(eventLeaveFail(eventId));
			}
		);
	};
}

/**
 * Creates an EVENT_LEAVE_END action for a given event ID.
 * @param  {Number} eventId
 * @return {Object} action
 */
export function eventLeaveEnd(eventId) {
	return {
		type: EVENT_LEAVE_END,
		eventId
	};
}

/**
 * Creates an EVENT_LEAVE_FAIL action for a given event ID.
 * TODO: add error message
 * @param  {Number} eventId
 * @return {Object} action
 */
export function eventLeaveFail(eventId) {
	return {
		type: EVENT_LEAVE_FAIL,
		eventId
	};
}

/**
 * Starts an event delte action chain. Dispatches EVENT_DELETE_START,
 * and either EVENT_DELETE_END or EVENT_DELETE_FAIL.
 * @param  {Number} eventId
 * @return {Function} thunk
 */
export function eventDeleteStart(eventId) {
	return (dispatch, getState) => {
		dispatch({
			type: EVENT_DELETE_START,
			eventId
		});

		let service = new ConvergenceService();
		service.deleteEvent(eventId, getState().login.userId).then(
			resp => {
				dispatch(eventDeleteEnd(eventId));
			},
			err => {
				dispatch(eventDeleteFail(eventId));
			}
		);
	};
}

/**
 * Creates an EVENT_DELETE_END action for an event with a given ID.
 * @param  {Number} eventId
 * @return {Object} action
 */
export function eventDeleteEnd(eventId) {
	return {
		type: EVENT_DELETE_END,
		eventId
	};
}

/**
 * Creates an EVENT_DELETE_FAIL action for an event with a given ID.
 * TODO: add error message.
 * @param  {Number} eventId
 * @return {Object} action
 */
export function eventDeleteFail(eventId) {
	return {
		type: EVENT_DELETE_FAIL,
		eventId
	};
}
