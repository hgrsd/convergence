export class ToolbarView {
	constructor(view) {
		this.view = view;
	}

	bind(viewModel) {
		viewModel.isVisible$.subscribe(isVisible => {
			if (isVisible) {
				this.view.classList.add("active");
			} else {
				this.view.classList.remove("active");
			}
		});
	}
}