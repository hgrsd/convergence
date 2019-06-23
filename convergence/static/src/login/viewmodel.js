import {
	BehaviorSubject
} from "rxjs";

import {
	map
} from "rxjs/operators";

export class LoginViewModel {
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