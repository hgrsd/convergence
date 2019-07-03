// src/login module contains actions, reducer and views
// responsible for sign in and sign up process

import { LoginView } from "./login";
import { connect } from "react-redux";
import { loginStart, registerStart } from "./actions";

function mapStateToProps(state) {
	return state.login;
}

function mapDispatchToProps(dispatch) {
	return {
		loginStart: (username, password) => {
			dispatch(loginStart(username, password));
		},
		registerStart: (username, password) => {
			dispatch(registerStart(username, password));
		}
	};
}

export const Login = connect(
	mapStateToProps,
	mapDispatchToProps
)(LoginView);

export { loginReducer } from "./reducer";
