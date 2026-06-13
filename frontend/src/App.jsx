import { useEffect, useState } from "react";
import { createItem, deleteItem, getItems } from "./api/api";
import "./App.css";

function App() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  async function loadItems() {
    const data = await getItems();
    setItems(data);
  }

  useEffect(() => {
    loadItems();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();

    await createItem({
      name,
      description,
    });

    setName("");
    setDescription("");
    await loadItems();
  }

  async function handleDelete(id) {
    await deleteItem(id);
    await loadItems();
  }

  return (
    <div className="container">
      <h1>PBN Assessment Starter</h1>

      <form onSubmit={handleSubmit} className="form">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Item name"
          required
        />

        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description"
        />

        <button type="submit">Create Item</button>
      </form>

      <h2>Items</h2>

      <div className="items">
        {items.map((item) => (
          <div key={item.id} className="item-card">
            <div>
              <strong>{item.name}</strong>
              <p>{item.description}</p>
            </div>

            <button onClick={() => handleDelete(item.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;