import React from "react";
import ReactDOM from "react-dom";
import { createStore, combineReducers, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import { Provider } from "react-redux";
import { Router } from "react-router-dom";
import { loginReducer } from "./login";
import { loginCheck } from "./login/actions";
import { overviewReducer } from "./overview";
import App from "./app";
import history from "./history";

const appReducers = combineReducers({
	login: loginReducer,
	overview: overviewReducer
});

const logger = store => next => action => {
	console.log("dispatching", action);
	let result = next(action);
	console.log("next state", store.getState());
	return result;
};

const appStore = createStore(appReducers, {}, applyMiddleware(logger, thunk));
appStore.dispatch(loginCheck());
ReactDOM.render(
	<Provider store={appStore}>
		<Router history={history}>
			<App />
		</Router>
	</Provider>,
	document.getElementById("app-root")
);
