import { connect } from "react-redux";
import { eventEditSuccess, eventSaveStart } from "./actions";
import { EventEditor } from "./editor";

function mapStateToProps(state) {
	return state.overview.eventEditor;
}

function mapDispatchToProps(dispatch) {
	return {
		eventEditSuccess: () => {
			dispatch(eventEditSuccess());
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
