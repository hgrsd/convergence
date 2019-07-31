import React from "react";

/**
 * Renders a simple animated bootstrap spinner.
 */
export class SmallSpinner extends React.Component {
	render() {
		let className =
			"spinner-border spinner-border-sm" +
			(this.props.isVisible ? "" : " d-none");
		return <span className={className} role="status" aria-hidden="true" />;
	}
}