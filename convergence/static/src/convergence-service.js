import {
	ajax
} from "rxjs/ajax";

export class ConvergenceService {

	constructor() {
		this.username = "";
		this.password = "";
	}

	login(username, password) {
		return ajax({
			url: "/user/login",
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: {
				username,
				password
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