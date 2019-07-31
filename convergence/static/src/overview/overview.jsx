import React from "react";
import { Link, Switch, Route } from "react-router-dom";
import EventEditor from "./event-editor";
import EventList from "./event-list";
import { NavbarView } from "./navbar";

/**
 * Overview component renders main overview screen.
 */
export class Overview extends React.Component {
	render() {
		return (
			<div>
				<NavbarView />
				<div className="container">
					<Switch>
						<Route exact path="/event/new" component={EventEditor} />
						<Route path="/" component={EventList} />
					</Switch>
				</div>
			</div>
		);
	}
}
