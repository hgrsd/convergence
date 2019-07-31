import React from "react";
import { loginStart } from "./actions";
import { SmallSpinner } from "../common";

/**
 * LoginView displays a login/signup form,
 * available at "/login" path.
 */
export class LoginView extends React.Component {
	constructor(props) {
		super(props);
		this.usernameInput = React.createRef();
		this.passwordInput = React.createRef();
	}

	render() {
		const hasErrorMessage =
			this.props.errorMessage && this.props.errorMessage.length;
		return (
			<LoginLayout>
				<div className="card view-content">
					<form className="card-body">
						<h1 className="h3 mb-3 font-weight-normal">Convergence</h1>
						<div className="form-group">
							<label htmlFor="username" className="sr-only">
								Username
							</label>
							<input
								disabled={this.props.isBusy}
								type="email"
								id="username"
								className="form-control"
								placeholder="Username"
								required=""
								autoFocus={true}
								ref={this.usernameInput}
							/>
						</div>
						<div className="form-group">
							<label htmlFor="password" className="sr-only">
								Password
							</label>
							<input
								disabled={this.props.isBusy}
								type="password"
								id="password"
								className="form-control"
								placeholder="Password"
								required={true}
								ref={this.passwordInput}
							/>
						</div>
						<div
							className={
								"alert alert-warning alert-dismissible " +
								(hasErrorMessage ? "" : "fade")
							}
							role="alert">
							<span>{this.props.errorMessage}</span>
							<button type="button" className="close" aria-label="Close">
								<span aria-hidden="true">&times;</span>
							</button>
						</div>
						<button
							disabled={this.props.isBusy}
							className="btn btn-lg btn-primary"
							href="#"
							onClick={e => {
								e.preventDefault();
								this.props.loginStart(
									this.usernameInput.current.value,
									this.passwordInput.current.value
								);
							}}>
							<SmallSpinner isVisible={this.props.isLoggingIn} />
							Sign in
						</button>

						<button
							disabled={this.props.isBusy}
							className="btn btn-lg btn-light"
							href="#"
							onClick={e => {
								e.preventDefault();
								this.props.registerStart(
									this.usernameInput.current.value,
									this.passwordInput.current.value
								);
							}}>
							<SmallSpinner isVisible={this.props.isRegistering} />
							Register
						</button>
					</form>
				</div>
			</LoginLayout>
		);
	}
}

export class LoginLayout extends React.Component {
	render() {
		return (
			<div
				className="view container absolute-fill active"
				id="view-login"
				data-toolbar="false">
				<div className="row justify-content-center align-items-center h-100 w-100">
					<div className="col-12 col-md-6 col-lg-5 text-center">
						{this.props.children}
					</div>
				</div>
			</div>
		);
	}
}
