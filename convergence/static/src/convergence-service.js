import axios from "axios";

const CSRF_COOKIE_NAME = "csrf_access_token";
const CSRF_HEADER_NAME = "X-CSRF-TOKEN";
const USER_ID_KEY = "login.userId";

// Gets value of a cookie with a given name.
// Returns null if there's no such cookie.
function getCookie(name) {
	var value = "; " + document.cookie;
	var parts = value.split("; " + name + "=");
	if (parts.length == 2) {
		return parts
			.pop()
			.split(";")
			.shift();
	}
	return null;
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

	// Checks if the user was logged in before.
	// If a user id and CSRF cookie are present then we,
	// most likely, can skip the login.
	// 401 can still be returned by the server if data expired
	// or is invalid.
	loginCheck() {
		const cookie = getCookie(CSRF_COOKIE_NAME);
		const userId = parseInt(localStorage.getItem(USER_ID_KEY));
		if(cookie && !isNaN(userId)) {
			setCsrfToken(cookie);
			return userId;
		}
		return null;
	}

	login(username, password) {
		return axios
			.post("/user/login", { email: username, password })
			.then(resp => {
				setCsrfToken(getCookie(CSRF_COOKIE_NAME));
				localStorage.setItem(USER_ID_KEY, resp.data.data.user_id);
				return resp;
			});
	}

	register(username, password) {
		return axios
			.post("/user", { email: username, screen_name: username, password })
			.then(resp => {
				setCsrfToken(getCookie(CSRF_COOKIE_NAME));
				localStorage.setItem(USER_ID_KEY, resp.data.data.id);
				return resp;
			});
	}

	getEvents() {
		return axios.get("/events");
	}

	createEvent(event) {
		return axios.post(`/events/${event.name}`);
	}

	deleteEvent(eventId) {
		return axios.delete(`/events/${eventId}`);
	}

	leaveEvent(eventId, userId) {
		return axios.delete(`/events/user_event/${eventId}:${userId}`);
	}

	inviteUsers(eventId, usernames) {
		return axios.post(`/events/invite/${eventId}`, {
			emails: usernames
		});
	}
}
