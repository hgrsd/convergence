import {
	BehaviorSubject
} from "rxjs";

export class MapViewModel {
	constructor() {
		this.mapViewPort$ = new BehaviorSubject({
			lat: 0,
			lon: 0,
			zoom: 3
		});
	}
}