import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Scheduleslot: React.FC = () => {
  return (
    <div id="page-scheduleslot-3">
    <div id="if948" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="in8yj" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="ibnxe" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i8gr8f" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="incn6i" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/event">{"Event"}</a>
          <a id="i2uou6" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/session">{"Session"}</a>
          <a id="i2gz3u" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/room">{"Room"}</a>
          <a id="inbcjf" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/scheduleslot">{"ScheduleSlot"}</a>
          <a id="i2kn17" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/speaker">{"Speaker"}</a>
        </div>
        <p id="ix52of" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="isekp3" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="izkb76" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"ScheduleSlot"}</h1>
        <p id="iefkyr" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage ScheduleSlot data"}</p>
        <TableBlock id="table-scheduleslot-3" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="ScheduleSlot List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "StartTime", "column_type": "field", "field": "startTime", "type": "datetime", "required": true}, {"label": "EndTime", "column_type": "field", "field": "endTime", "type": "datetime", "required": true}, {"label": "Session", "column_type": "lookup", "path": "session", "entity": "Session", "field": "title", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "startTime", "label": "startTime", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "field", "field": "endTime", "label": "endTime", "type": "datetime", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "session", "field": "session", "lookup_field": "title", "entity": "Session", "type": "str", "required": true}]}} dataBinding={{"entity": "ScheduleSlot", "endpoint": "/scheduleslot/"}} />
      </main>
    </div>    </div>
  );
};

export default Scheduleslot;
