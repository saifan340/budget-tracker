import { useState, useEffect } from "react";
import axios from "axios";

const CATEGORIES = ["Essen", "Miete", "Transport", "Freizeit", "Gehalt", "Sonstiges"];

const API = "http://localhost:8000";

function App() {
  const [transactions, setTransactions] = useState([]);
  const [form, setForm] = useState({
    type: "ausgabe",
    amount: "",
    category: "Essen",
    description: "",
  });

  // Alle Transaktionen laden
  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    const res = await axios.get(`${API}/transactions`);
    setTransactions(res.data);
  };

  // Neue Transaktion speichern
  const handleSubmit = async () => {
    if (!form.amount) return alert("Bitte Betrag eingeben!");
    await axios.post(`${API}/transactions`, form);
    setForm({ type: "ausgabe", amount: "", category: "Essen", description: "" });
    fetchTransactions();
  };

  // Transaktion löschen
  const handleDelete = async (id) => {
    await axios.delete(`${API}/transactions/${id}`);
    fetchTransactions();
  };

  // Bilanz berechnen
  const balance = transactions.reduce((sum, t) => {
    return t.type === "einnahme" ? sum + t.amount : sum - t.amount;
  }, 0);

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", fontFamily: "Arial" }}>
      <h1>💰 Budget Tracker</h1>

      {/* Bilanz */}
      <div style={{
        padding: "20px",
        background: balance >= 0 ? "#e6ffe6" : "#ffe6e6",
        borderRadius: "10px",
        marginBottom: "20px"
      }}>
        <h2>Bilanz: {balance.toFixed(2)} €</h2>
      </div>

      {/* Formular */}
      <div style={{ background: "#f5f5f5", padding: "20px", borderRadius: "10px", marginBottom: "20px" }}>
        <h3>Neue Transaktion</h3>

        <select value={form.type} onChange={e => setForm({...form, type: e.target.value})}>
          <option value="ausgabe">Ausgabe</option>
          <option value="einnahme">Einnahme</option>
        </select>

        <input
          type="number"
          placeholder="Betrag in €"
          value={form.amount}
          onChange={e => setForm({...form, amount: e.target.value})}
          style={{ margin: "10px", padding: "5px" }}
        />

        <select value={form.category} onChange={e => setForm({...form, category: e.target.value})}>
          {CATEGORIES.map(cat => <option key={cat}>{cat}</option>)}
        </select>

        <input
          type="text"
          placeholder="Beschreibung (optional)"
          value={form.description}
          onChange={e => setForm({...form, description: e.target.value})}
          style={{ margin: "10px", padding: "5px", width: "200px" }}
        />

        <br/>
        <button onClick={handleSubmit} style={{
          marginTop: "10px", padding: "10px 20px",
          background: "#4CAF50", color: "white", border: "none",
          borderRadius: "5px", cursor: "pointer"
        }}>
          Hinzufügen ✅
        </button>
      </div>

      {/* Transaktionsliste */}
      <h3>Transaktionen</h3>
      {transactions.length === 0 && <p>Noch keine Transaktionen.</p>}
      {transactions.map(t => (
        <div key={t.id} style={{
          display: "flex", justifyContent: "space-between",
          padding: "10px", marginBottom: "8px",
          background: t.type === "einnahme" ? "#e6ffe6" : "#ffe6e6",
          borderRadius: "8px"
        }}>
          <span>{t.category} — {t.description}</span>
          <span>{t.type === "einnahme" ? "+" : "-"}{t.amount} €</span>
          <button onClick={() => handleDelete(t.id)}
            style={{ background: "red", color: "white", border: "none", borderRadius: "5px", cursor: "pointer" }}>
            🗑️
          </button>
        </div>
      ))}
    </div>
  );
}

export default App;