export class Navigation {
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
};