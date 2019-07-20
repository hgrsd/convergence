import { connect } from "react-redux";
import {
	eventListLoadStart,
	eventEditStart,
	eventEditSuccess,
	eventSaveStart,
	eventSaveSuccess,
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
