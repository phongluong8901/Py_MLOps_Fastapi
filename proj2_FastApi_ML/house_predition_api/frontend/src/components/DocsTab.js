"use client";

import React from "react";
import { BookOpen, Code, Cpu, ShieldCheck } from "lucide-react";

export default function DocsTab({ backendUrl }) {
  const features = [
    { name: "MedInc", type: "float", desc: "Median income of block group in $10,000s (e.g., 8.32 = $83,200/yr)." },
    { name: "HouseAge", type: "float", desc: "Median age of houses in block group (1 to 52 years)." },
    { name: "AveRooms", type: "float", desc: "Average total rooms per household (e.g. 6.98)." },
    { name: "AveBedrms", type: "float", desc: "Average bedrooms per household (e.g. 1.02)." },
    { name: "Population", type: "float", desc: "Total population living within block group." },
    { name: "AveOccup", type: "float", desc: "Average number of household members / occupants." },
    { name: "Latitude", type: "float", desc: "Geographic latitude coordinate (-90 to 90)." },
    { name: "Longitude", type: "float", desc: "Geographic longitude coordinate (-180 to 180)." },
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      {/* Model Info */}
      <div className="glass-card">
        <h2 style={{ fontSize: "1.25rem", display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.8rem" }}>
          <Cpu size={22} color="#8b5cf6" /> ML Model Architecture
        </h2>
        <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem", lineHeight: "1.6" }}>
          The backend API utilizes a <strong>Random Forest Regressor</strong> trained on the official California Housing dataset.
          The model predicts median house value scaled in USD dollars ($100,000 multiplier) with a standard confidence interval of <strong>±$39,000</strong>.
        </p>
      </div>

      {/* Feature Definitions Table */}
      <div className="glass-card">
        <h3 style={{ fontSize: "1.1rem", display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "1rem" }}>
          <BookOpen size={20} color="#3b82f6" /> Input Features Schema
        </h3>

        <div className="custom-table-container">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Feature Name</th>
                <th>Data Type</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {features.map((f, i) => (
                <tr key={i}>
                  <td style={{ fontFamily: "var(--font-mono)", color: "#60a5fa", fontWeight: 600 }}>{f.name}</td>
                  <td style={{ fontFamily: "var(--font-mono)", color: "var(--text-muted)" }}>{f.type}</td>
                  <td>{f.desc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* API Code Examples */}
      <div className="glass-card">
        <h3 style={{ fontSize: "1.1rem", display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "1rem" }}>
          <Code size={20} color="#34d399" /> API Integration Snippets
        </h3>

        <div style={{ background: "rgba(15, 23, 42, 0.9)", padding: "1.25rem", borderRadius: "12px", border: "1px solid var(--border-color)" }}>
          <span style={{ fontSize: "0.75rem", color: "var(--text-muted)", textTransform: "uppercase", fontWeight: 700 }}>
            cURL Request (POST /predict)
          </span>
          <pre style={{ fontFamily: "var(--font-mono)", fontSize: "0.85rem", color: "#34d399", overflowX: "auto", marginTop: "0.5rem", whiteSpace: "pre-wrap" }}>
{`curl -X POST "${backendUrl}/predict" \\
  -H "Content-Type: application/json" \\
  -d '{
    "MedInc": 8.32,
    "HouseAge": 41.0,
    "AveRooms": 6.98,
    "AveBedrms": 1.02,
    "Population": 322.0,
    "AveOccup": 2.55,
    "Latitude": 37.88,
    "Longitude": -122.23
  }'`}
          </pre>
        </div>
      </div>
    </div>
  );
}
