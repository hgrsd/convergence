import { combineReducers } from "redux";
import { eventEditorReducer } from "./event-editor";
import { eventListReducer } from "./event-list";

export const overviewReducer = combineReducers({
	eventEditor: eventEditorReducer,
	eventList: eventListReducer
});

export { Overview } from "./overview";
