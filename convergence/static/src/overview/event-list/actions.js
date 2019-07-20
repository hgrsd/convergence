import { ConvergenceService } from "../../convergence-service";

export const EVENT_LIST_LOAD_START = "EVENT_LIST_LOAD_START";
export const EVENT_LIST_LOAD_SUCCESS = "EVENT_LIST_LOAD_SUCCESS";
export const EVENT_LIST_LOAD_FAILURE = "EVENT_LIST_LOAD_FAILURE";

export const EVENT_LEAVE_START = "EVENT_LEAVE_START";
export const EVENT_LEAVE_SUCCESS = "EVENT_LEAVE_SUCCESS";
export const EVENT_LEAVE_FAILURE = "EVENT_LEAVE_FAILURE";
export const EVENT_DELETE_START = "EVENT_DELETE_START";
export const EVENT_DELETE_SUCCESS = "EVENT_DELETE_SUCCESS";
export const EVENT_DELETE_FAILURE = "EVENT_DELETE_FAILURE";

export function eventListLoadStart() {
	return (dispatch, getState) => {
		dispatch({
			type: EVENT_LIST_LOAD_START
		});

		let service = new ConvergenceService();

		service.getEvents().then(
			resp => {
				dispatch(eventListLoadSuccess(resp.data.data, getState().login.userId));
				return resp;
			},
			err => {
				dispatch(eventListLoadFailure());
			}
		);
	};
}

export function eventListLoadSuccess(events, userId) {
	return {
		type: EVENT_LIST_LOAD_SUCCESS,
		events,
		userId
	};
}

export function eventListLoadFailure() {
	return {
		type: EVENT_LIST_LOAD_FAILURE
	};
}

export function eventLeaveStart(eventId) {
	return (dispatch, getState) => {
		dispatch({
			type: EVENT_LEAVE_START,
			eventId
		});

		let service = new ConvergenceService();
		service.leaveEvent(eventId, getState().login.userId).then(
			resp => {
				dispatch(eventLeaveSuccess(eventId));
			},
			err => {
				dispatch(eventLeaveFailure(eventId));
			}
		);
	};
}

export function eventLeaveSuccess(eventId) {
	return {
		type: EVENT_LEAVE_SUCCESS,
		eventId
	};
}

export function eventLeaveFailure(eventId) {
	return {
		type: EVENT_LEAVE_FAILURE,
		eventId
	};
}

export function eventDeleteStart(eventId) {
	return (dispatch, getState) => {
		dispatch({
			type: EVENT_DELETE_START,
			eventId
		});

		let service = new ConvergenceService();
		service.deleteEvent(eventId, getState().login.userId).then(
			resp => {
				dispatch(eventDeleteSuccess(eventId));
			},
			err => {
				dispatch(eventDeleteFailure(eventId));
			}
		);
	};
}

export function eventDeleteSuccess(eventId) {
	return {
		type: EVENT_DELETE_SUCCESS,
		eventId
	};
}

export function eventDeleteFailure(eventId) {
	return {
		type: EVENT_DELETE_FAILURE,
		eventId
	};
}
