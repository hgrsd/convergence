let {
	BehaviorSubject,
	Subject,
	Observable,
	fromEvent,
	combineLatest
} = rxjs;

let {
	map,
	startWith,
	filter,
	catchError
} = rxjs.operators;

let ajax = rxjs.ajax.ajax;

class ConvergenceService {

	constructor() {
		this.username = "";
		this.password = "";
	}

	login(username, password) {
		// temporary workaround for a lack of auth endpoint
		// TODO: switch to proper auth when #17 is done
		return ajax({
			url: "/groups",
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				"Authorization": "Basic " + btoa(username + ":" + password),
				"X-Requested-With": "XMLHttpRequest"
			}
		});
	}

	register(username, password) {
		return ajax({
			url: "/user",
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: {
				username,
				password
			}
		});
	}


	saveCredentials(username, password) {
		this.username = username;
		this.password = password;
	}
}

class Navigation {
	constructor(root, toolbar) {
		let views = {};
		let currentView = null;

		root.querySelectorAll(".view").forEach(e => {
			views[e.id] = e;
			e.addEventListener("transitionend", event => {
				if (!event.target.classList.contains("view")) {
					return;
				}
				if (!event.target.classList.contains("active")) {
					event.target.style.display = "none";
				} else {
					event.target.style.display = "initial";
				}
			});
		});

		this.push = function(viewId) {
			if (currentView) {
				currentView.classList.remove("active");
				currentView.classList.add("prev");
			}

			const view = views[viewId];
			view.classList.remove("prev");
			view.classList.remove("next");
			view.classList.add("active");
			currentView = view;

			toolbar.isVisible$.next(currentView.dataset.toolbar === "true");
		}
	}
}

class ToolbarViewModel {
	constructor() {
		this.isVisible$ = new BehaviorSubject(false);
	}
}

class ToolbarView {
	constructor(view) {
		this.view = view;
	}

	bind(viewModel) {
		viewModel.isVisible$.subscribe(isVisible => {
			if (isVisible) {
				this.view.classList.add("active");
			} else {
				this.view.classList.remove("active");
			}
		});
	}
}

class LoginViewModel {
	constructor(service, navigation) {
		this.navigation = navigation;
		this.service = service;
		this.username$ = new BehaviorSubject("");
		this.password$ = new BehaviorSubject("");
		this.isValid$ = new BehaviorSubject(false);
		this.isLoggingIn$ = new BehaviorSubject(false);
		this.isRegistering$ = new BehaviorSubject(false);
		this.isBusy$ = new BehaviorSubject(false);
		this.errorMessage$ = new BehaviorSubject("");

		this.startLogin$ = new Subject();
		this.startRegister$ = new Subject();
		this.endLogin$ = new Subject();

		// validation
		combineLatest(this.username$, this.password$)
			.pipe(map(vals => {
				return !!vals[0] && vals[0].length > 0 &&
					!!vals[1] && vals[1].length > 0;
			}))
			.subscribe(this.isValid$);

		// login
		this.startLogin$.subscribe(() => {
			var username = this.username$.value;
			var password = this.password$.value;
			this.isLoggingIn$.next(true);
			this.service.login(username, password)
				.subscribe(d => {
						this.service.saveCredentials(username, password);
						this.navigation.push("view-home");
						this.endLogin$.next(true);
					},
					e => {
						this.errorMessage$.next(e.response.error.message);
						this.isLoggingIn$.next(false);
					},
					() => this.isLoggingIn$.next(false));
		});

		// registration
		this.startRegister$.subscribe(() => {
			var username = this.username$.value;
			var password = this.password$.value;
			this.isRegistering$.next(true);
			this.service.register(username, password)
				.subscribe(() => {
						this.service.saveCredentials(username, password);
						this.navigation.push("view-home");
						this.endLogin$.next(true);
					},
					e => {
						this.errorMessage$.next(e.response.error.message);
						this.isRegistering$.next(false);
					},
					() => this.isRegistering$.next(false));
		});


		// activity
		combineLatest(this.isLoggingIn$.pipe(startWith(false)),
				this.isRegistering$.pipe(startWith(false)))
			.pipe(map(([loggingIn, registering]) =>
				loggingIn === true || registering === true))
			.subscribe(this.isBusy$);
	}
}

class LoginView {
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

class MapViewModel {
	constructor() {
		this.mapViewPort$ = new BehaviorSubject({
			lat: 0,
			lon: 0,
			zoom: 3
		});
	}
}

class MapView {
	constructor(view) {
		this.view = view;

		L.tileLayer("https://b.tile.openstreetmap.org/{z}/{x}/{y}.png", {
			attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>",
			maxZoom: 17,
			minZoom: 0,
			id: "osm.tiles"
		}).addTo(view);
		view.setView([0, 0], 3);
	}

	bind(viewModel) {
		viewModel.mapViewPort$.subscribe(port => {
			this.view.flyTo([
				port.lat,
				port.lon,
			], port.zoom, {
				animate: true
			})
		});
	}
}

(function() {
	const toolbarViewModel = new ToolbarViewModel();
	const toolbarView = new ToolbarView(document.getElementById("toolbar"));
	toolbarView.bind(toolbarViewModel);

	const service = new ConvergenceService();
	const navigation = new Navigation(document, toolbarViewModel);

	const mapView = new MapView(L.map("map-underlay", {}));
	const mapViewModel = new MapViewModel();
	mapView.bind(mapViewModel);

	const loginViewModel = new LoginViewModel(service, navigation);
	const loginView = new LoginView(document.getElementById("view-login"));
	loginView.bind(loginViewModel);

	loginViewModel.endLogin$.subscribe(() => {
		navigator.geolocation.getCurrentPosition(position => {
			mapViewModel.mapViewPort$.next({
				lat: position.coords.latitude,
				lon: position.coords.longitude,
				zoom: 17
			});
		});
	});

	navigation.push("view-login");
}());