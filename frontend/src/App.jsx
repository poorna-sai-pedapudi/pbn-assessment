import { useState } from "react";
import CustomerView from "./CustomerView";
import ProviderView from "./ProviderView";
import DashboardView from "./DashboardView";
import "./App.css";

function App() {
  const [view, setView] = useState("customer");

  return (
    <div>
      <nav className="nav">
        <button className={view === "customer" ? "active" : ""} onClick={() => setView("customer")}>Customer</button>
        <button className={view === "provider" ? "active" : ""} onClick={() => setView("provider")}>Provider</button>
        <button className={view === "dashboard" ? "active" : ""} onClick={() => setView("dashboard")}>Dashboard</button>
      </nav>

      <div className="page-center">
        {view === "customer" && <CustomerView />}
        {view === "provider" && <ProviderView />}
        {view === "dashboard" && <DashboardView />}
      </div>
    </div>
  );
}

export default App;