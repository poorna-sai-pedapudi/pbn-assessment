import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from "recharts";
import { getDashboardStats } from "./api/api";

function DashboardView() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    getDashboardStats().then(setStats).catch(() => setStats(null));
  }, []);

  if (!stats) return <div className="container"><p>Loading insights…</p></div>;

  return (
    <div className="container">
      <h1>Booking Insights</h1>

      <h2>Most Booked Services</h2>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={stats.services}>
          <XAxis dataKey="name" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#4a90d9" />
        </BarChart>
      </ResponsiveContainer>

      <h2>Bookings by Day of Week</h2>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={stats.days}>
          <XAxis dataKey="day" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#5cb88a" />
        </BarChart>
      </ResponsiveContainer>

      <h2>Bookings by Hour</h2>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={stats.hours}>
          <XAxis dataKey="hour" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#e29a3c" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default DashboardView;