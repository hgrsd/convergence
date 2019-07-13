import React from "react";
import { Link, Switch, Route } from "react-router-dom";
import { SmallSpinner } from "../common";
import { NavbarView, EditEventView } from "./index.js";

export class OverviewView extends React.Component {
	componentWillMount() {
		this.props.overviewLoadStart();
	}

	render() {
		return (
			<div>
				<NavbarView />
				<div className="container">
					<Switch>
						<Route
							exact
							path="/event/new"
							render={props => (
								<EditEventView
									eventSaveStart={this.props.eventSaveStart}
									eventEditSuccess={this.props.eventEditSuccess}
								/>
							)}
						/>
						<Route
							path="/"
							render={props => (
								<EventList
									isLoadingEvents={this.props.isLoadingEvents}
									pendingEvents={this.props.pendingEvents}
								/>
							)}
						/>
					</Switch>
				</div>
			</div>
		);
	}
}

export class EventCard extends React.Component {
	render() {
		const event = this.props.event;
		return (
			<div className="col-12 col-md-6 col-lg-4">
				<div className="card m-1 event-card">
					<img
						src={`//lorempixel.com/200/200/nightlife/${(event.id % 9) + 1}`}
						className="card-img-top"
					/>
					<div className="card-body">
						<div className="d-flex">
							<h5 className="flex-fill card-title">{event.event_name}</h5>
							<small className="text-muted">
								{formatRelativeDate(new Date(), new Date(event.creation_date))}
							</small>
						</div>
						<p className="card-text"></p>
						<p className="card-text text-right">
							<a className="card-link" href="#">
								Details
							</a>
						</p>
					</div>
				</div>
			</div>
		);
	}
}

// TODO: replace or remove placeholder images on each card
// TODO: format event date instead of creation date
// TODO: localize static strings
// TODO: display "no current events" label
// TODO: move "Events" title to the nav bar
// TODO: move event list classes into a separate file
export class EventList extends React.Component {
	render() {
		let content = null;

		if (this.props.isLoadingEvents) {
			content = (
				<div className="text-muted row justify-content-center">
					<div className="col-4">
						<SmallSpinner isVisible="true" /> Loading Events
					</div>
				</div>
			);
		} else {
			const listItems = this.props.pendingEvents.map((e, i) => {
				return <EventCard event={e} key={e.id}/>;
			});

			const newEventCard = (
				<div className="col-12 col-md-6 col-lg-4">
					<div className="card m-1 event-card">
						<img
							src={`//lorempixel.com/200/200/nightlife/1`}
							className="card-img-top"
						/>

						<div className="card-body">
							<div className="d-flex">
								<h5 className="flex-fill card-title text-center">
									Plan an Event
								</h5>
							</div>
							<h2 className="card-text text-center">
								<Link
									to="event/new"
									className="card-link btn btn-light btn-lg"
									href="#">
									<i className="far fa-calendar-plus"></i>
								</Link>
							</h2>
						</div>
					</div>
				</div>
			);

			content = (
				<div>
					<h4>Events:</h4>

					<div className="row no-gutters">
						{newEventCard}
						{listItems}
					</div>
				</div>
			);
		}

		return content;
	}
}

// formats a `date` relative to `now`
// depending on how distant `date` is from `now` will return
// more or less precise date strings
function formatRelativeDate(now, date) {
	const locale = navigator.language;
	if (now.getYear() !== date.getYear()) {
		return date.toLocaleDateString(locale, {
			year: "numeric",
			month: "short"
		});
	}

	if (now.getMonth() !== date.getMonth()) {
		return date.toLocaleDateString(locale, {
			month: "short",
			day: "numeric"
		});
	}

	if (now.getDay() === date.getDay()) {
		// TODO: localize "today"
		return (
			"Today, " +
			date.toLocaleTimeString(locale, {
				hour: "numeric",
				minute: "numeric"
			})
		);
	}

	if (now.getDay() !== date.getDay()) {
		return date.toLocaleDateString(locale, {
			month: "short",
			day: "numeric"
		});
	}

	return date.toDateString();
}
