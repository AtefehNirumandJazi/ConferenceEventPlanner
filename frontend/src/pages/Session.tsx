import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Session: React.FC = () => {
  return (
    <div id="page-session-1">
    <div id="ish98" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="iyc7v" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="ih0jr" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i38e2" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="i6pnv" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/event">{"Event"}</a>
          <a id="ih7p5" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/session">{"Session"}</a>
          <a id="ig7ak" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/room">{"Room"}</a>
          <a id="iqcjk" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/scheduleslot">{"ScheduleSlot"}</a>
          <a id="iu5jk" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/speaker">{"Speaker"}</a>
        </div>
        <p id="if1qh" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i9nh8" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="i3xus" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"Session"}</h1>
        <p id="iuzkm" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage Session data"}</p>
        <TableBlock id="table-session-1" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Session List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Title", "column_type": "field", "field": "title", "type": "str", "required": true}, {"label": "Description", "column_type": "field", "field": "description", "type": "str", "required": true}, {"label": "SessionType", "column_type": "field", "field": "sessionType", "type": "str", "required": true}, {"label": "Event", "column_type": "lookup", "path": "event", "entity": "Event", "field": "name", "type": "str", "required": true}, {"label": "Speaker", "column_type": "lookup", "path": "speaker", "entity": "Speaker", "field": "fullName", "type": "list", "required": false}, {"label": "Room", "column_type": "lookup", "path": "room", "entity": "Room", "field": "name", "type": "str", "required": true}, {"label": "ScheduleSlot", "column_type": "lookup", "path": "scheduleSlot", "entity": "ScheduleSlot", "field": "startTime", "type": "datetime", "required": false}], "formColumns": [{"column_type": "field", "field": "title", "label": "title", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "description", "label": "description", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "sessionType", "label": "sessionType", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "speaker", "field": "speaker", "lookup_field": "fullName", "entity": "Speaker", "type": "list", "required": false}, {"column_type": "lookup", "path": "room", "field": "room", "lookup_field": "name", "entity": "Room", "type": "str", "required": true}, {"column_type": "lookup", "path": "scheduleSlot", "field": "scheduleSlot", "lookup_field": "startTime", "entity": "ScheduleSlot", "type": "str", "required": false}, {"column_type": "lookup", "path": "event", "field": "event", "lookup_field": "name", "entity": "Event", "type": "str", "required": true}]}} dataBinding={{"entity": "Session", "endpoint": "/session/"}} />
      </main>
    </div>    </div>
  );
};

export default Session;
