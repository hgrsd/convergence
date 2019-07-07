import {
	OVERVIEW_LOAD_START,
	OVERVIEW_LOAD_SUCCESS,
	OVERVIEW_LOAD_FAILURE,
	EVENT_EDIT_START,
	EVENT_EDIT_SUCCESS,
	EVENT_SAVE_START,
	EVENT_SAVE_SUCCESS,
	EVENT_SAVE_FAILURE
} from "./actions";

const initialState = {
	pendingEvents: [],
	isLoadingEvents: false,
	isSavingEvent: false,
	eventId: null,
	eventName: null,
	eventDate: null,
	errorMessage: null
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
		case EVENT_EDIT_START:
			return resetEditedEvent({ ...state });
		case EVENT_EDIT_SUCCESS:
			return resetEditedEvent({ ...state });
		case EVENT_SAVE_START:
			return {
				...state,
				isSavingEvent: true
			};
		case EVENT_SAVE_SUCCESS:
			return {
				...state,
				isSavingEvent: false
			};
		case EVENT_SAVE_FAILURE:
			return {
				...state,
				isSavingEvent: false,
				errorMessage: action.errorMessage
			};
	}

	return state;
}

// mutates `state`, resets properties related to the
// add/edit event screen
function resetEditedEvent(state) {
	state.isSavingEvent = false;
	state.eventId = null;
	state.eventName = null;
	state.eventDate = null;
	state.errorMessage = null;
}
