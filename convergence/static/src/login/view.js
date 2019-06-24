import {
	fromEvent,
	combineLatest
} from "rxjs";

import {
	map,
	startWith
} from "rxjs/operators";

export class LoginView {
	constructor(view) {
		this.view = view;
	}

	bind(viewModel) {
		const usernameField = this.view.querySelector("#username");
		const passwordField = this.view.querySelector("#password");
		const loginButton = this.view.querySelector(".btn-primary");
		const registerButton = this.view.querySelector(".btn-light");
		const loginSpinner = loginButton.querySelector(".spinner-border");
		const registerSpinner = registerButton.querySelector(".spinner-border");
		const errorAlert = this.view.querySelector(".alert");
		const errorMessage = errorAlert.querySelector("span");
		const errorCloseButton = errorAlert.querySelector("button");

		// bind events to source
		const username$ = fromEvent(usernameField, "input", e => e.target.value)
			.pipe(startWith(""))
			.subscribe(viewModel.username$);
		const password$ = fromEvent(passwordField, "input", e => e.target.value)
			.pipe(startWith(""))
			.subscribe(viewModel.password$);
		fromEvent(loginButton, "click")
			.subscribe(viewModel.startLogin$);
		fromEvent(registerButton, "click")
			.subscribe(viewModel.startRegister$);
		fromEvent(errorCloseButton, "click")
			.pipe(map(() => ""))
			.subscribe(viewModel.errorMessage$);

		// bind GUI state from source
		combineLatest(viewModel.isValid$.pipe(startWith(false)),
				viewModel.isLoggingIn$.pipe(startWith(false)),
				viewModel.isRegistering$.pipe(startWith(false)))
			.pipe(map(([valid, loggingIn, registering]) => {
				return valid === false ||
					loggingIn === true ||
					registering === true;
			}))
			.subscribe(shouldDisable => {
				if (shouldDisable) {
					loginButton.classList.add("disabled");
					registerButton.classList.add("disabled");
				} else {
					loginButton.classList.remove("disabled");
					registerButton.classList.remove("disabled");
				}
			});

		viewModel.isLoggingIn$.subscribe(shouldShow => {
			if (shouldShow) {
				loginSpinner.classList.remove("d-none");
			} else {
				loginSpinner.classList.add("d-none");
			}
		});

		viewModel.isRegistering$.subscribe(shouldShow => {
			if (shouldShow) {
				registerSpinner.classList.remove("d-none");
			} else {
				registerSpinner.classList.add("d-none");
			}
		});

		viewModel.isBusy$.subscribe(isBusy => {
			if (isBusy) {
				usernameField.disabled = true;
				passwordField.disabled = true;
			} else {
				usernameField.disabled = false;
				passwordField.disabled = false;
			}
		});

		viewModel.errorMessage$
			.pipe(map(msg => !!msg && msg.length > 0))
			.subscribe(showAlert => {
				if (showAlert) {
					errorAlert.classList.add("show");
				} else {
					errorAlert.classList.remove("show");
				}
			});

		viewModel.errorMessage$
			.subscribe(msg => {
				errorMessage.innerText = msg;
			});
	}
}