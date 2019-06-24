import {
	BehaviorSubject
} from "rxjs";

export class ToolbarViewModel {
	constructor() {
		this.isVisible$ = new BehaviorSubject(false);
	}
}