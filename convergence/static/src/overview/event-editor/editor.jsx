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

						<UserList
							users={this.props.users}
							eventEditRemoveUser={this.props.eventEditRemoveUser}
							eventEditAddUser={this.props.eventEditAddUser}
						/>

						<div className="text-right">
							<a
								className="btn btn-light m-1"
								href="#"
								onClick={this.props.eventEditSuccess.bind(this)}>
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

class UserList extends React.Component {
	constructor() {
		super();
		this.usernameInput = React.createRef();
	}

	render() {
		const userItems = this.props.users.map(u => {
			return (
				<li className="list-group-item" key={u}>
					<div className="d-flex w-100 justify-content-between align-items-center">
						<span className="mx-2">{u}</span>
						<small>
							<button
								className="btn btn-danger"
								onClick={() => this.props.eventEditRemoveUser(u)}>
								<i className="fas fa-trash"></i>
							</button>
						</small>
					</div>
				</li>
			);
		});
		return (
			<div>
				<ul className="list-group">
					<li className="list-group-item">
						<h5>Invited Users</h5>
					</li>
					{userItems}
					<li className="list-group-item">
						<div
							className="d-flex w-100 justify-content-between
										align-items-center">
							<input
								placeholder="Username"
								type="email"
								className="form-control mr-2"
								ref={this.usernameInput}
							/>
							<small>
								<button
									className="btn btn-primary"
									onClick={() => {
										this.props.eventEditAddUser(
											this.usernameInput.current.value
										);
										this.usernameInput.current.value = "";
									}}>
									<i className="fas fa-plus"></i>
								</button>
							</small>
						</div>
					</li>
				</ul>
			</div>
		);
	}
}
