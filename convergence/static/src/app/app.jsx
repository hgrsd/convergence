import React from "react";
import { Route, Redirect, Switch } from "react-router-dom";
import { Login } from "../login";
import { Overview } from "../overview";

export class App extends React.Component {
	render() {
		return (
			<Switch>
				<Route exact path="/login" component={Login} />
				<Route
					path="/"
					render={props => {
						return this.props.isLoggedIn ? (
							<Overview />
						) : (
							<Redirect to="/login" />
						);
					}}
				/>
				<Route path="/home" component={Overview} />
			</Switch>
		);
	}
}