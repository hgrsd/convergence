import React from "react";
import { Link } from "react-router-dom";
import { EventCard } from "./card";
import { SmallSpinner } from "../../common";

// TODO: replace or remove placeholder images on each card
// TODO: format event date instead of creation date
// TODO: localize static strings
// TODO: display "no current events" label
// TODO: move "Events" title to the nav bar
// TODO: move event list classes into a separate file
export class EventList extends React.Component {
	componentDidMount() {
		this.props.eventListLoadStart();
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
			const listItems = this.props.pendingEvents.map((e, i) => {
				return (
					<EventCard
						event={e}
						key={e.id}
						eventLeaveStart={this.props.eventLeaveStart}
						eventDeleteStart={this.props.eventDeleteStart}
					/>
				);
			});

			// TODO: turn this into a component
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
