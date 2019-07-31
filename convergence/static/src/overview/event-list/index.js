/**
 * src/overview/event-list module contains components, actions and reducer
 * for the list of events, which is visible in overiew.
 * This mobule is included by src/overview.
 */

import { connect } from "react-redux";
import {
	eventListLoadStart,
	eventEditStart,
	eventEditEnd,
	eventSaveStart,
	eventSaveEnd,
	eventLeaveStart,
	eventDeleteStart
} from "./actions";
import { EventList } from "./list";

function mapStateToProps(state) {
	return state.overview.eventList;
}

function mapDispatchToProps(dispatch) {
	return {
		eventListLoadStart: (username, password) => {
			dispatch(eventListLoadStart(username, password));
		},
		eventLeaveStart: (eventId) => {
			dispatch(eventLeaveStart(eventId));
		},
		eventDeleteStart: (eventId) => {
			dispatch(eventDeleteStart(eventId));
		}
	};
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(EventList);

export { eventListReducer } from "./reducer";
