import React from "react";
import { SmallSpinner } from "../common";
import { NavbarView } from "./navbar";

// TODO: replace or remove placeholder images on each card
// TODO: format event date instead of creation date
// TODO: localize static strings
// TODO: display "no current events" label
// TODO: move "Events" title to the nav bar
export class OverviewView extends React.Component {
	componentWillMount() {
		this.props.overviewLoadStart();
	}

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
			const now = new Date();
			const listItems = this.props.pendingEvents.map((e, i) => {
				const size = Math.floor(Math.random() * 2 + 1);
				return (
					<div className="col-12 col-md-6 col-lg-4" key={e.id}>
						<div className="card m-1 event-card">
							<img
								src={`//lorempixel.com/200/200/nightlife/${(e.id % 9) + 1}`}
								className="card-img-top"
							/>
							<div className="card-body">
								<div className="d-flex">
									<h5 className="flex-fill card-title">{e.name}</h5>
									<small className="text-muted">
										{formatRelativeDate(now, new Date(e.creation_date))}
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
								<a className="card-link btn btn-light btn-lg" href="#">
									<i className="far fa-calendar-plus"></i>
								</a>
							</h2>
						</div>
					</div>
				</div>
			);

			content = (
				<div className="row justify-content-center">
					<div className="col-12 col-sm-10">
						<h4>Events:</h4>
						<div className="row no-gutters">
							{newEventCard}
							{listItems}
						</div>
					</div>
				</div>
			);
		}

		return (
			<div>
				<NavbarView />
				<div className="container my-1">{content}</div>
			</div>
		);
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
