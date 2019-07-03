import { ConvergenceService } from "../convergence-service";

export const OVERVIEW_LOAD_START = "OVERVIEW_LOAD_START";
export const OVERVIEW_LOAD_SUCCESS = "OVERVIEW_LOAD_SUCCESS";
export const OVERVIEW_LOAD_FAILURE = "OVERVIEW_LOAD_FAILURE";

export function overviewLoadStart() {
	return dispatch => {
		dispatch({
			type: OVERVIEW_LOAD_START
		});

		let service = new ConvergenceService();

		service
			.getEvents()
			.then(resp => {
				dispatch(overviewLoadSuccess(resp.data.data));
				return resp;
			}, err => {
				dispatch(overviewLoadFailure());
			});
	};
}

export function overviewLoadSuccess(events) {
	return {
		type: OVERVIEW_LOAD_SUCCESS,
		events
	};
}

export function overviewLoadFailure() {
	return {
		type: OVERVIEW_LOAD_FAILURE
	};
}
