import {
	Navigation
} from "./navigation.js";

import {
	ConvergenceService
}
from "./convergence-service.js";

import {
	MapView
} from "./map/view";

import {
	MapViewModel
} from "./map/viewmodel";

import {
	ToolbarView
} from "./toolbar/view";

import {
	ToolbarViewModel
} from "./toolbar/viewmodel.js";

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