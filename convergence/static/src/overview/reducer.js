import {
	OVERVIEW_LOAD_START,
	OVERVIEW_LOAD_SUCCESS,
	OVERVIEW_LOAD_FAILURE
} from "./actions";

const initialState = {
	pendingEvents: [],
	isLoadingEvents: false
};

export function overviewReducer(state = initialState, action) {
	switch (action.type) {
		case OVERVIEW_LOAD_START:
			return {
				...state,
				isLoadingEvents: true
			};
		case OVERVIEW_LOAD_FAILURE:
			return {
				...state,
				isLoadingEvents: false
			};
		case OVERVIEW_LOAD_SUCCESS:
			let result = {
				...state,
				isLoadingEvents: false,
				pendingEvents: action.events
			};
			// TODO: sort by and display event planned date instead of created date
			result.pendingEvents.sort((l, r) => {
				return new Date(l.created_date) - new Date(r.created_date);
			});
			return result;
	}

	return state;
}
