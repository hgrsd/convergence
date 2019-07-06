import { connect } from "react-redux";
import { overviewLoadStart } from "./actions";
import { OverviewView } from "./overview";

function mapStateToProps(state) {
	return state.overview;
}

function mapDispatchToProps(dispatch) {
	return {
		overviewLoadStart: (username, password) => {
			dispatch(overviewLoadStart(username, password));
		}
	};
}

export const Overview = connect(
	mapStateToProps,
	mapDispatchToProps
)(OverviewView);

export { overviewReducer } from "./reducer";
