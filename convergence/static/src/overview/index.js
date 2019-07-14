import { connect } from "react-redux";
import {
	overviewLoadStart,
	eventEditStart,
	eventEditSuccess,
	eventSaveStart,
	eventSaveSuccess,
	eventLeaveStart,
	eventDeleteStart
} from "./actions";
import { OverviewView } from "./overview";

function mapStateToProps(state) {
	return state.overview;
}

function mapDispatchToProps(dispatch) {
	return {
		overviewLoadStart: (username, password) => {
			dispatch(overviewLoadStart(username, password));
		},
		eventEditStart: () => {
			dispatch(eventEditStart());
		},
		eventEditSuccess: () => {
			dispatch(eventEditSuccess());
		},
		eventSaveStart: event => {
			dispatch(eventSaveStart(event));
		},
		eventSaveSuccess: () => {
			dispatch(eventSaveSuccess());
		},
		eventLeaveStart: (eventId) => {
			dispatch(eventLeaveStart(eventId));
		},
		eventDeleteStart: (eventId) => {
			dispatch(eventDeleteStart(eventId));
		}
	};
}

export const Overview = connect(
	mapStateToProps,
	mapDispatchToProps
)(OverviewView);

export { overviewReducer } from "./reducer";
export { NavbarView } from "./navbar";
export { EditEventView } from "./edit-event";
