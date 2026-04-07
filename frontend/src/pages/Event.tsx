import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Event: React.FC = () => {
  return (
    <div id="page-event-0">
    <div id="id2w9" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="iiimk" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="ikhxx" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="iw53i" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="i3dmn" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/event">{"Event"}</a>
          <a id="isb7g" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/session">{"Session"}</a>
          <a id="ivhqp" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/room">{"Room"}</a>
          <a id="igsrv" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/scheduleslot">{"ScheduleSlot"}</a>
          <a id="ig49q" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/speaker">{"Speaker"}</a>
        </div>
        <p id="i91a6" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i2tvf" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="i2vlp" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"Event"}</h1>
        <p id="i9a7w" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage Event data"}</p>
        <TableBlock id="table-event-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Event List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Name", "column_type": "field", "field": "name", "type": "str", "required": true}, {"label": "StartDate", "column_type": "field", "field": "startDate", "type": "date", "required": true}, {"label": "Location", "column_type": "field", "field": "location", "type": "str", "required": true}, {"label": "EndDate", "column_type": "field", "field": "endDate", "type": "date", "required": true}, {"label": "Session", "column_type": "lookup", "path": "session", "entity": "Session", "field": "title", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "name", "label": "name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "startDate", "label": "startDate", "type": "date", "required": true, "defaultValue": null}, {"column_type": "field", "field": "location", "label": "location", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "endDate", "label": "endDate", "type": "date", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "session", "field": "session", "lookup_field": "title", "entity": "Session", "type": "list", "required": false}]}} dataBinding={{"entity": "Event", "endpoint": "/event/"}} />
      </main>
    </div>    </div>
  );
};

export default Event;
