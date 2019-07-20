import {
	OVERVIEW_LOAD_START,
	OVERVIEW_LOAD_SUCCESS,
	OVERVIEW_LOAD_FAILURE,
	EVENT_EDIT_START,
	EVENT_EDIT_SUCCESS,
	EVENT_EDIT_ADD_USER,
	EVENT_SAVE_START,
	EVENT_SAVE_SUCCESS,
	EVENT_SAVE_FAILURE,
	EVENT_LEAVE_START,
	EVENT_LEAVE_SUCCESS,
	EVENT_LEAVE_FAILURE,
	EVENT_DELETE_START,
	EVENT_DELETE_SUCCESS,
	EVENT_DELETE_FAILURE
} from "./actions";

const initialState = {
	pendingEvents: [],
	isLoadingEvents: false,
	isSavingEvent: false,
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
		case OVERVIEW_LOAD_SUCCESS: {
			let result = {
				...state,
				isLoadingEvents: false,
				pendingEvents: action.events
			};
			// TODO: sort by and display event planned date instead of created date
			result.pendingEvents.sort((l, r) => {
				return new Date(l.creation_date) - new Date(r.creation_date);
			});

			for (let e of result.pendingEvents) {
				e.isOwned = e.event_owner_id === action.userId;
			}
			return result;
		}
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
		case EVENT_LEAVE_START: {
			let event = copyEvent(action.eventId, state);
			if (!event) {
				console.log("Attempt to leave a non-existing event.");
				return state;
			}
			event.isLeaving = true;
			return saveEvent(event, state);
		}
		case EVENT_DELETE_SUCCESS:
		case EVENT_LEAVE_SUCCESS: {
			let result = { ...state };
			result.pendingEvents = state.pendingEvents.filter(e => {
				return e.id !== action.eventId;
			});
			return result;
		}
		case EVENT_LEAVE_FAILURE: {
			let event = copyEvent(action.eventId, state);
			if (!event) {
				console.log("Attempt to leave a non-existing event.");
				return state;
			}
			event.isLeaving = false;
			return saveEvent(event, state);
		}
		case EVENT_DELETE_START: {
			let event = copyEvent(action.eventId, state);
			if (!event) {
				console.log("Attempt to delete a non-existing event.");
				return state;
			}
			event.isDeleting = true;
			return saveEvent(event, state);
		}
		case EVENT_DELETE_FAILURE: {
			let event = copyEvent(action.eventId, state);
			if (!event) {
				console.log("Attempt to delete a non-existing event.");
				return state;
			}
			event.isLeaving = false;
			return saveEvent(event, state);
		}
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

function copyEvent(eventId, state) {
	for (const e of state.pendingEvents) {
		if (e.id === eventId) {
			return { ...e };
		}
	}
	return null;
}

function saveEvent(event, state) {
	let result = { ...state };
	result.pendingEvents = state.pendingEvents.map(e => {
		if (e.id === event.id) {
			return event;
		}
		return e;
	});
	return result;
}
