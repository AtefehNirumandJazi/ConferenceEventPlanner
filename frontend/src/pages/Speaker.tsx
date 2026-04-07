import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Speaker: React.FC = () => {
  return (
    <div id="page-speaker-4">
    <div id="icpcj5" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="i7zt5n" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="inp2x6" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="imzpcl" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="i5uta4" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/event">{"Event"}</a>
          <a id="ilu80k" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/session">{"Session"}</a>
          <a id="ix22vb" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/room">{"Room"}</a>
          <a id="i6rmac" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/scheduleslot">{"ScheduleSlot"}</a>
          <a id="i3vdit" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/speaker">{"Speaker"}</a>
        </div>
        <p id="ioirs4" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i0xup3" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="i3vsnp" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"Speaker"}</h1>
        <p id="ialaqd" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage Speaker data"}</p>
        <TableBlock id="table-speaker-4" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Speaker List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "FullName", "column_type": "field", "field": "fullName", "type": "str", "required": true}, {"label": "Affiliation", "column_type": "field", "field": "affiliation", "type": "str", "required": true}, {"label": "Email", "column_type": "field", "field": "email", "type": "str", "required": true}, {"label": "Session", "column_type": "lookup", "path": "session", "entity": "Session", "field": "title", "type": "list", "required": true}], "formColumns": [{"column_type": "field", "field": "fullName", "label": "fullName", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "affiliation", "label": "affiliation", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "email", "label": "email", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "session", "field": "session", "lookup_field": "title", "entity": "Session", "type": "list", "required": true}]}} dataBinding={{"entity": "Speaker", "endpoint": "/speaker/"}} />
      </main>
    </div>    </div>
  );
};

export default Speaker;
