import {
	ajax
} from "rxjs/ajax";

export class ConvergenceService {

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