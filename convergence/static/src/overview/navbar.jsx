import React from "react";

export class NavbarView extends React.Component {
	render() {
		return (
			<nav className="navbar navbar-expand-lg navbar-light bg-light">
				<div className="container">
					<a className="mr-auto btn btn-info btn-lg" href="#">
						C
					</a>
					<ul className="navbar-nav">
						<li className="nav-item">
							<a className="nav-link" href="#/settings">
								<i className="fas fa-cog"></i>
							</a>
						</li>
					</ul>
				</div>
			</nav>
		);
	}
}
