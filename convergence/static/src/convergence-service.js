import axios from "axios";

const CSRF_COOKIE_NAME = "csrf_access_token";
const CSRF_HEADER_NAME = "X-CSRF-TOKEN";

function getCookie(name) {
	var value = "; " + document.cookie;
	var parts = value.split("; " + name + "=");
	if (parts.length == 2) {
		return parts
			.pop()
			.split(";")
			.shift();
	}
}

// Sets a global CSRF header to be sent with every
// subsequent non-GET request
function setCsrfToken(csrfToken) {
	let csrfMethods = ["post", "put", "delete", "patch"];
	for (let method of csrfMethods) {
		axios.defaults.headers[method][CSRF_HEADER_NAME] = csrfToken;
	}
}

// ConvergenceService is responsible for providing a way to talk
// to convergence API. Each method is supposed to return a promise,
// which resolves once API returns a result, or fails if any non 20x HTTP
// code is returned.

// TODO: create a catch for 401 code,
// which will log the user out gracefully or refresh the token
export class ConvergenceService {
	constructor() {
		this.username = null;
		this.password = null;
	}

	login(username, password) {
		return axios.post("/user/login", { email: username, password }).then(resp => {
			setCsrfToken(getCookie(CSRF_COOKIE_NAME));
		});
	}

	register(username, password) {
		return axios.post("/user", { username, password }).then(resp => {
			setCsrfToken(getCookie(CSRF_COOKIE_NAME));
		});
	}

	getEvents() {
		return axios.get("/events");
	}

	createEvent(event) {
		return axios.post(`/events/${event.name}`);
	}
}
