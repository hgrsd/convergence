import React from "react";

/**
 * Component, which renders a single event card with
 * available actions (leave, delete, details).
 */
export class EventCard extends React.Component {
	render() {
		const event = this.props.event;
		let leaveButton = null;

		if (event.isOwned) {
			leaveButton = (
				<button
					disabled={event.isDeleting}
					className="card-link btn btn-light text-danger"
					href="#"
					onClick={() => this.props.eventDeleteStart(event.id)}>
					Delete
				</button>
			);
		} else {
			leaveButton = (
				<button
					disabled={event.isLeaving}
					className="card-link btn btn-light text-danger"
					href="#"
					onClick={() => this.props.eventLeaveStart(event.id)}>
					Leave
				</button>
			);
		}

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
							{leaveButton}
							<a className="card-link btn btn-light" href="#">
								Details
							</a>
						</p>
					</div>
				</div>
			</div>
		);
	}
}

/**
 * Formats a `date` relative to `now`.
 * Depending on how distant `date` is from `now` will return
 * more or less precise date strings.
 * @param {Date} now current date
 * @param {Date} date a timestamp to format
 * @return {String} date string
 */
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
