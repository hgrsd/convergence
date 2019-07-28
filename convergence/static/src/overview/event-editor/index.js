import { connect } from "react-redux";
import {
	eventEditSuccess,
	eventSaveStart,
	eventEditAddUser,
	eventEditRemoveUser
} from "./actions";
import { EventEditor } from "./editor";

function mapStateToProps(state) {
	return state.overview.eventEditor;
}

function mapDispatchToProps(dispatch) {
	return {
		eventEditSuccess: () => {
			dispatch(eventEditSuccess());
		},
		eventEditAddUser: username => {
			dispatch(eventEditAddUser(username));
		},
		eventEditRemoveUser: username => {
			dispatch(eventEditRemoveUser(username));
		},
		eventSaveStart: event => {
			dispatch(eventSaveStart(event));
		}
	};
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(EventEditor);

export { eventEditorReducer } from "./reducer";
