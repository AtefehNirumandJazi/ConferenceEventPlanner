import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Event from "./pages/Event";
import Session from "./pages/Session";
import Room from "./pages/Room";
import Scheduleslot from "./pages/Scheduleslot";
import Speaker from "./pages/Speaker";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/event" element={<Event />} />
            <Route path="/session" element={<Session />} />
            <Route path="/room" element={<Room />} />
            <Route path="/scheduleslot" element={<Scheduleslot />} />
            <Route path="/speaker" element={<Speaker />} />
            <Route path="/" element={<Navigate to="/event" replace />} />
            <Route path="*" element={<Navigate to="/event" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
