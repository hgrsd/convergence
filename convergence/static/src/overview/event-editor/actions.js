import { ConvergenceService } from "../../convergence-service";
import history from "../../history";

export const EVENT_EDIT_START = "EVENT_EDIT_START";
export const EVENT_EDIT_SUCCESS = "EVENT_EDIT_SUCCESS";
export const EVENT_SAVE_START = "EVENT_SAVE_START";
export const EVENT_SAVE_SUCCESS = "EVENT_SAVE_SUCCESS";
export const EVENT_SAVE_FAILURE = "EVENT_SAVE_FAILURE";

export function eventSaveStart(event) {
	return dispatch => {
		dispatch({
			type: EVENT_SAVE_START,
			event
		});

		let service = new ConvergenceService();
		service.createEvent(event).then(
			resp => {
				// TODO: push returned event into event list
				eventSaveSuccess();
			},
			err => {
				// TODO: display an actual error message
				eventSaveFailure("Can't save event.");
			}
		);
	};
}

export function eventSaveSuccess(event) {
	return {
		type: EVENT_SAVE_SUCCESS,
		event
	};
}

export function eventSaveFailure(errorMessage) {
	return {
		type: EVENT_SAVE_FAILURE,
		errorMessage
	};
}

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

export function eventEditSuccess() {
	return dispatch => {
		dispatch({
			type: EVENT_EDIT_SUCCESS
		});
		history.goBack();
	};
}