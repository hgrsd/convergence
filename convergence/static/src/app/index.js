/**
 * src/app module contains a wrapper App component,
 * which is responsible for general app layout.
 */


import { App } from "./app";
import { connect } from "react-redux";
import { loginCheck } from "../login/actions";

function mapStateToProps(state) {
	return state.login;
}

function mapDispatchToProps(dispatch) {
	return {
		loginCheck: () => {
			dispatch(loginCheck());
		}
	};
}

export { App };

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(App);