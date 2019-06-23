export class MapView {
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