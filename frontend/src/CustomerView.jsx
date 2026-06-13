import { useEffect, useState } from "react";
import {
  getServices,
  getMechanics,
  getAvailability,
  createAppointment,
} from "./api/api";

function CustomerView() {
  const [services, setServices] = useState([]);
  const [mechanics, setMechanics] = useState([]);

  const [serviceId, setServiceId] = useState("");
  const [mechanicId, setMechanicId] = useState("");
  const [date, setDate] = useState("");

  const [slots, setSlots] = useState([]);
  const [customerName, setCustomerName] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    getServices().then(setServices);
    getMechanics().then(setMechanics);
  }, []);

  useEffect(() => {
    if (serviceId && mechanicId && date) {
      getAvailability(mechanicId, serviceId, date)
        .then(setSlots)
        .catch(() => setSlots([]));
    } else {
      setSlots([]);
    }
  }, [serviceId, mechanicId, date]);

  async function handleBook(slot) {
    if (!customerName) {
      setMessage("Please enter your name before booking.");
      return;
    }

    const ok = window.confirm(
      `Confirm booking: ${serviceName()} with ${mechanicName()} at ${formatTime(slot.start_time)} on ${date}?`
    );
    if (!ok) return;

    try {
      await createAppointment({
        service_id: Number(serviceId),
        mechanic_id: Number(mechanicId),
        customer_name: customerName,
        start_time: slot.start_time,
      });
      setMessage(`Booking confirmed for ${customerName} at ${formatTime(slot.start_time)}.`);
      const updated = await getAvailability(mechanicId, serviceId, date);
      setSlots(updated);
    } catch {
      setMessage("Booking failed. The slot may have just been taken.");
    }
  }

  function serviceName() {
    const s = services.find((x) => x.id === Number(serviceId));
    return s ? s.name : "";
  }

  function mechanicName() {
    const m = mechanics.find((x) => x.id === Number(mechanicId));
    return m ? m.name : "";
  }

  function formatTime(iso) {
    return new Date(iso).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  return (
    <div className="container">
      <h1>Book an Appointment</h1>

      <div className="form">
        <select value={serviceId} onChange={(e) => setServiceId(e.target.value)}>
          <option value="">Select service</option>
          {services.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name} ({s.duration_minutes} min) — ${s.price}
            </option>
          ))}
        </select>

        <select value={mechanicId} onChange={(e) => setMechanicId(e.target.value)}>
          <option value="">Select mechanic</option>
          {mechanics.map((m) => (
            <option key={m.id} value={m.id}>{m.name}</option>
          ))}
        </select>

        <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
      </div>

      <input
        placeholder="Your name"
        value={customerName}
        onChange={(e) => setCustomerName(e.target.value)}
        style={{ marginBottom: "16px", width: "100%" }}
      />

      {message && <p className="message">{message}</p>}

      <h2>Available Slots</h2>
      {serviceId && mechanicId && date ? (
        slots.length > 0 ? (
          <div className="slots">
            {slots.map((slot, i) => (
              <button
                key={i}
                className="slot"
                onClick={() => handleBook(slot)}
              >
                {formatTime(slot.start_time)}
              </button>
            ))}
          </div>
        ) : (
          <p>No available slots for this selection.</p>
        )
      ) : (
        <p>Select a service, mechanic, and date to see slots.</p>
      )}

    </div>
  );
}

export default CustomerView;