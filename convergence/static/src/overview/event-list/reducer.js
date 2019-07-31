import {
	EVENT_LIST_LOAD_START,
	EVENT_LIST_LOAD_FAIL,
	EVENT_LIST_LOAD_END,
	EVENT_LEAVE_START,
	EVENT_LEAVE_END,
	EVENT_LEAVE_FAIL,
	EVENT_DELETE_START,
	EVENT_DELETE_END,
	EVENT_DELETE_FAIL
} from "./actions";

const initialState = {
	pendingEvents: [],
	isLoadingEvents: false,
	isSavingEvent: false
};

export function eventListReducer(state = initialState, action) {
	switch (action.type) {
		case EVENT_LIST_LOAD_START:
			return {
				...state,
				isLoadingEvents: true
			};
		case EVENT_LIST_LOAD_FAIL:
			return {
				...state,
				isLoadingEvents: false
			};
		case EVENT_LIST_LOAD_END: {
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
		case EVENT_LEAVE_START: {
			let event = copyEvent(action.eventId, state);
			if (!event) {
				console.log("Attempt to leave a non-existing event.");
				return state;
			}
			event.isLeaving = true;
			return saveEvent(event, state);
		}
		case EVENT_DELETE_END:
		case EVENT_LEAVE_END: {
			let result = { ...state };
			result.pendingEvents = state.pendingEvents.filter(e => {
				return e.id !== action.eventId;
			});
			return result;
		}
		case EVENT_LEAVE_FAIL: {
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
		case EVENT_DELETE_FAIL: {
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
