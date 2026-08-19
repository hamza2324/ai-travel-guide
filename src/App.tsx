import { Navigate, Route, Routes } from "react-router-dom";
import { Nav } from "./components/Nav";
import { Landing } from "./pages/Landing";
import { MyTrips } from "./pages/MyTrips";
import { Planner } from "./pages/Planner";
import { TripDashboard } from "./pages/TripDashboard";

export default function App() {
  return (
    <>
      <Nav />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/plan" element={<Planner />} />
        <Route path="/trip/:id" element={<TripDashboard />} />
        <Route path="/trips" element={<MyTrips />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}
