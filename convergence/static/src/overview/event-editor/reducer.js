import {
	EVENT_EDIT_START,
	EVENT_EDIT_SUCCESS,
	EVENT_SAVE_START,
	EVENT_SAVE_SUCCESS,
	EVENT_SAVE_FAILURE,
	EVENT_EDIT_ADD_USER,
	EVENT_EDIT_REMOVE_USER
} from "./actions";

const initialState = {
	eventId: null,
	eventName: null,
	eventDate: null,
	errorMessage: null,
	users: []
};

export function eventEditorReducer(state = initialState, action) {
	switch (action.type) {
		case EVENT_EDIT_START:
			return { ...initialState };
		case EVENT_EDIT_SUCCESS:
			return { ...initialState };
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
		case EVENT_EDIT_ADD_USER:
			return {
				...state,
				users: [...state.users, action.username]
			};
		case EVENT_EDIT_REMOVE_USER:
			// TODO: consider removing by index
			return {
				...state,
				users: state.users.filter(u => u !== action.username)
			};
	}

	return state;
}
