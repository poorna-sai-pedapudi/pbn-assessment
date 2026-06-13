const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// ---------- Services ----------
export async function getServices() {
  const res = await fetch(`${API_BASE_URL}/services/`);
  if (!res.ok) throw new Error("Failed to fetch services");
  return res.json();
}

// ---------- Mechanics ----------
export async function getMechanics() {
  const res = await fetch(`${API_BASE_URL}/mechanics/`);
  if (!res.ok) throw new Error("Failed to fetch mechanics");
  return res.json();
}

// ---------- Availability ----------
export async function getAvailability(mechanicId, serviceId, date) {
  const params = new URLSearchParams({
    mechanic_id: mechanicId,
    service_id: serviceId,
    date: date,
  });
  const res = await fetch(`${API_BASE_URL}/appointments/availability/?${params}`);
  if (!res.ok) throw new Error("Failed to fetch availability");
  return res.json();
}

// ---------- Appointments ----------
export async function getAppointments() {
  const res = await fetch(`${API_BASE_URL}/appointments/`);
  if (!res.ok) throw new Error("Failed to fetch appointments");
  return res.json();
}

export async function createAppointment(appointment) {
  const res = await fetch(`${API_BASE_URL}/appointments/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(appointment),
  });
  if (!res.ok) throw new Error("Failed to create appointment");
  return res.json();
}

export async function cancelAppointment(id) {
  const res = await fetch(`${API_BASE_URL}/appointments/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to cancel appointment");
  return res.json();
}


export async function getDashboardStats() {
  const res = await fetch(`${API_BASE_URL}/stats/dashboard`);
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
}