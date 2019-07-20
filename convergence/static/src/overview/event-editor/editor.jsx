import React from "react";

// A form, which allows creating a new event or editing 
// an existing one.
// TODO: localize static strings
export class EventEditor extends React.Component {
	constructor() {
		super();
		this.eventNameInput = React.createRef();
		this.eventDateTimeInput = React.createRef();
	}

	render() {
		return (
			<div className="row justify-content-center m-2">
				<h4 className="col-12 text-center">New Event:</h4>
				<div className="card col-12 col-sm-10 col-md-6">
					<form className="card-body">
						<div className="form-group">
							<label className="d-block">
								Event Name:
								<input
									className="form-control"
									placeholder="For example: dinner with friends"
									ref={this.eventNameInput}
								/>
							</label>
						</div>
						<div className="form-group">
							<label className="d-block">
								Event Date:
								<input
									type="datetime-local"
									className="form-control"
									ref={this.eventDateTimeInput}
								/>
							</label>
						</div>

						<div className="text-right">
							<a
								className="btn btn-light m-1"
								href="#"
								onClick={this.props.eventEditSuccess}>
								Cancel
							</a>
							<a
								className="btn btn-primary m-1"
								href="#"
								onClick={this.eventSaveStart.bind(this)}>
								Save
							</a>
						</div>
					</form>
				</div>
			</div>
		);
	}

	eventSaveStart() {
		this.props.eventSaveStart({
			name: this.eventNameInput.current.value,
			dateTime: this.eventDateTimeInput.current.value
		});
	}
}
