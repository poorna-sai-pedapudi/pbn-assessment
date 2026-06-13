import { useEffect, useState } from "react";
import { getAppointments, getServices, getMechanics, cancelAppointment } from "./api/api";

function ProviderView() {
  const [appointments, setAppointments] = useState([]);
  const [services, setServices] = useState([]);
  const [mechanics, setMechanics] = useState([]);
  const [cancelMessage, setCancelMessage] = useState("");

  // filters
  const [nameFilter, setNameFilter] = useState("");
  const [serviceFilter, setServiceFilter] = useState("");
  const [dateFilter, setDateFilter] = useState("");

  async function loadAll() {
    const [appts, svcs, mechs] = await Promise.all([
      getAppointments(),
      getServices(),
      getMechanics(),
    ]);
    setAppointments(appts);
    setServices(svcs);
    setMechanics(mechs);
  }

  useEffect(() => {
    loadAll();
  }, []);

  function nameFor(list, id) {
    const found = list.find((x) => x.id === id);
    return found ? found.name : `#${id}`;
  }

  function formatDateTime(iso) {
    return new Date(iso).toLocaleString([], {
      weekday: "short",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

//   async function handleCancel(id) {
//     await cancelAppointment(id);
//     await loadAll();
//   }

  async function handleCancel(appt) {
    const svc = nameFor(services, appt.service_id);
    const mech = nameFor(mechanics, appt.mechanic_id);
    const when = formatDateTime(appt.start_time);

    const ok = window.confirm(
      `Cancel ${appt.customer_name}'s ${svc} with ${mech} at ${when}?`
    );
    if (!ok) return;

    await cancelAppointment(appt.id);
    setCancelMessage(`Cancelled ${appt.customer_name}'s ${svc} with ${mech} at ${when}.`);
    await loadAll();
  }

  // apply filters
  const filtered = appointments.filter((appt) => {
    const matchesName = appt.customer_name
      .toLowerCase()
      .includes(nameFilter.toLowerCase());
    const matchesService = serviceFilter
      ? appt.service_id === Number(serviceFilter)
      : true;
    const matchesDate = dateFilter
      ? appt.start_time.startsWith(dateFilter)
      : true;
    return matchesName && matchesService && matchesDate;
  });

  return (
    <div className="container">
      <h1>Booked Appointments</h1>
        {cancelMessage && <p className="message">{cancelMessage}</p>}
      <div className="form">
        <input
          placeholder="Filter by customer name"
          value={nameFilter}
          onChange={(e) => setNameFilter(e.target.value)}
        />
        <select value={serviceFilter} onChange={(e) => setServiceFilter(e.target.value)}>
          <option value="">All services</option>
          {services.map((s) => (
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}
        </select>
        <input
          type="date"
          value={dateFilter}
          onChange={(e) => setDateFilter(e.target.value)}
        />
        <button onClick={() => { setNameFilter(""); setServiceFilter(""); setDateFilter(""); }}>
          Clear
        </button>
      </div>

      {filtered.length === 0 ? (
        <p>No appointments match.</p>
      ) : (
        <div className="items">
          {filtered.map((appt) => (
            <div key={appt.id} className="item-card">
              <div>
                <strong>{appt.customer_name}</strong>
                <p>
                  {nameFor(services, appt.service_id)} with{" "}
                  {nameFor(mechanics, appt.mechanic_id)}
                </p>
                <p>{formatDateTime(appt.start_time)}</p>
              </div>
              <button onClick={() => handleCancel(appt)}>Cancel</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ProviderView;