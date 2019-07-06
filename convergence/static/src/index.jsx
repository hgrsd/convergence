import React from "react";
import ReactDOM from "react-dom";
import { createStore, combineReducers, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import { Provider } from "react-redux";
import { Router, Route, Redirect, Switch } from "react-router-dom";
import { Login, loginReducer } from "./login";
import { Overview, overviewReducer } from "./overview";
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

class App extends React.Component {
	render() {
		this.isAuthenticated = true;
		return (
			<Provider store={appStore}>
				<Router history={history}>
					<Switch>
						<Route exact path="/login" component={Login} />
						<Route
							path="/"
							render={props => {
								return this.isAuthenticated ? (
									<Overview />
								) : (
									<Redirect to="/login" />
								);
							}}
						/>
						<Route path="/home" component={Overview} />
					</Switch>
				</Router>
			</Provider>
		);
	}
}

ReactDOM.render(<App />, document.getElementById("app-root"));
