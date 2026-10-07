"use client";

import React, { useState } from "react";
import { Sparkles, DollarSign, Home, Users, MapPin, Calculator, CheckCircle2, AlertTriangle, RefreshCw } from "lucide-react";
import CaliforniaMap from "./CaliforniaMap";

export default function SinglePredictForm({ backendUrl }) {
  const defaultValues = {
    MedInc: 8.32,
    HouseAge: 41,
    AveRooms: 6.98,
    AveBedrms: 1.02,
    Population: 322,
    AveOccup: 2.55,
    Latitude: 37.88,
    Longitude: -122.23,
  };

  const [formData, setFormData] = useState(defaultValues);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const presets = [
    {
      name: "🌆 SF Luxury Heights",
      desc: "High income, historic Bay Area home",
      data: { MedInc: 10.5, HouseAge: 45, AveRooms: 7.2, AveBedrms: 1.1, Population: 450, AveOccup: 2.4, Latitude: 37.77, Longitude: -122.41 }
    },
    {
      name: "🌴 LA Coastal Villa",
      desc: "Prime West LA location near coast",
      data: { MedInc: 9.2, HouseAge: 28, AveRooms: 6.8, AveBedrms: 1.05, Population: 600, AveOccup: 2.7, Latitude: 34.05, Longitude: -118.24 }
    },
    {
      name: "🏡 Suburban Family",
      desc: "Moderate income, newer construction",
      data: { MedInc: 4.8, HouseAge: 18, AveRooms: 5.5, AveBedrms: 1.0, Population: 1200, AveOccup: 3.1, Latitude: 38.58, Longitude: -121.49 }
    },
    {
      name: "🌾 Rural Valley Farm",
      desc: "Spacious land, lower density",
      data: { MedInc: 2.9, HouseAge: 35, AveRooms: 5.0, AveBedrms: 1.15, Population: 350, AveOccup: 2.8, Latitude: 36.74, Longitude: -119.77 }
    }
  ];

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: parseFloat(value) || 0,
    }));
  };

  const applyPreset = (presetData) => {
    setFormData(presetData);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch(`${backendUrl}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to calculate prediction");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Cannot connect to FastAPI backend server");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "grid", gridTemplateColumns: result ? "1fr 1fr" : "1fr", gap: "2rem" }}>
      {/* Left Column - Input Form */}
      <div className="glass-card">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.25rem" }}>
          <div>
            <h2 style={{ fontSize: "1.25rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <Calculator size={22} color="#3b82f6" /> Property Specifications
            </h2>
            <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginTop: "0.2rem" }}>
              Adjust indicators or pick a preset to estimate California property market value.
            </p>
          </div>
          <button
            type="button"
            onClick={() => setFormData(defaultValues)}
            style={{
              background: "transparent",
              border: "1px solid rgba(255,255,255,0.1)",
              color: "var(--text-muted)",
              padding: "0.4rem 0.75rem",
              borderRadius: "6px",
              cursor: "pointer",
              fontSize: "0.8rem",
              display: "flex",
              alignItems: "center",
              gap: "0.3rem"
            }}
          >
            <RefreshCw size={12} /> Reset
          </button>
        </div>

        {/* Presets */}
        <div style={{ marginBottom: "1.5rem" }}>
          <span style={{ fontSize: "0.8rem", color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.05em", fontWeight: 700, display: "block", marginBottom: "0.5rem" }}>
            Quick Sample Presets
          </span>
          <div className="presets-grid">
            {presets.map((preset, i) => (
              <button
                key={i}
                type="button"
                className="preset-chip"
                onClick={() => applyPreset(preset.data)}
              >
                <div>
                  <div style={{ fontWeight: 600 }}>{preset.name}</div>
                  <div style={{ fontSize: "0.72rem", color: "var(--text-muted)" }}>{preset.desc}</div>
                </div>
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            {/* MedInc */}
            <div className="form-group">
              <div className="form-label">
                <span>Median Income (MedInc)</span>
                <span className="gradient-text">${(formData.MedInc * 10).toFixed(1)}k / yr</span>
              </div>
              <input
                type="number"
                step="0.1"
                min="0.5"
                max="15"
                className="custom-input"
                value={formData.MedInc}
                onChange={(e) => handleInputChange("MedInc", e.target.value)}
              />
              <input
                type="range"
                min="0.5"
                max="15"
                step="0.1"
                className="custom-range"
                value={formData.MedInc}
                onChange={(e) => handleInputChange("MedInc", e.target.value)}
              />
              <span className="form-sublabel">Median block income in $10,000s</span>
            </div>

            {/* HouseAge */}
            <div className="form-group">
              <div className="form-label">
                <span>House Age</span>
                <span>{formData.HouseAge} yrs</span>
              </div>
              <input
                type="number"
                min="1"
                max="52"
                className="custom-input"
                value={formData.HouseAge}
                onChange={(e) => handleInputChange("HouseAge", e.target.value)}
              />
              <input
                type="range"
                min="1"
                max="52"
                className="custom-range"
                value={formData.HouseAge}
                onChange={(e) => handleInputChange("HouseAge", e.target.value)}
              />
              <span className="form-sublabel">Median house age in block</span>
            </div>

            {/* AveRooms */}
            <div className="form-group">
              <div className="form-label">
                <span>Average Rooms</span>
                <span>{formData.AveRooms} rooms</span>
              </div>
              <input
                type="number"
                step="0.1"
                min="1"
                max="15"
                className="custom-input"
                value={formData.AveRooms}
                onChange={(e) => handleInputChange("AveRooms", e.target.value)}
              />
              <input
                type="range"
                min="1"
                max="15"
                step="0.1"
                className="custom-range"
                value={formData.AveRooms}
                onChange={(e) => handleInputChange("AveRooms", e.target.value)}
              />
              <span className="form-sublabel">Average rooms per household</span>
            </div>

            {/* AveBedrms */}
            <div className="form-group">
              <div className="form-label">
                <span>Average Bedrooms</span>
                <span>{formData.AveBedrms} bdrms</span>
              </div>
              <input
                type="number"
                step="0.05"
                min="0.5"
                max="5"
                className="custom-input"
                value={formData.AveBedrms}
                onChange={(e) => handleInputChange("AveBedrms", e.target.value)}
              />
              <input
                type="range"
                min="0.5"
                max="5"
                step="0.05"
                className="custom-range"
                value={formData.AveBedrms}
                onChange={(e) => handleInputChange("AveBedrms", e.target.value)}
              />
              <span className="form-sublabel">Average bedrooms per household</span>
            </div>

            {/* Population */}
            <div className="form-group">
              <div className="form-label">
                <span>Block Population</span>
                <span>{formData.Population.toLocaleString()} people</span>
              </div>
              <input
                type="number"
                min="10"
                max="15000"
                className="custom-input"
                value={formData.Population}
                onChange={(e) => handleInputChange("Population", e.target.value)}
              />
              <input
                type="range"
                min="10"
                max="10000"
                step="50"
                className="custom-range"
                value={formData.Population}
                onChange={(e) => handleInputChange("Population", e.target.value)}
              />
              <span className="form-sublabel">Total block group population</span>
            </div>

            {/* AveOccup */}
            <div className="form-group">
              <div className="form-label">
                <span>Average Occupants</span>
                <span>{formData.AveOccup} / house</span>
              </div>
              <input
                type="number"
                step="0.1"
                min="1"
                max="10"
                className="custom-input"
                value={formData.AveOccup}
                onChange={(e) => handleInputChange("AveOccup", e.target.value)}
              />
              <input
                type="range"
                min="1"
                max="10"
                step="0.1"
                className="custom-range"
                value={formData.AveOccup}
                onChange={(e) => handleInputChange("AveOccup", e.target.value)}
              />
              <span className="form-sublabel">Avg household members</span>
            </div>

            {/* Map Component for Lat & Lon */}
            <CaliforniaMap
              latitude={formData.Latitude}
              longitude={formData.Longitude}
              onChangeLocation={(lat, lon) => {
                setFormData((prev) => ({ ...prev, Latitude: lat, Longitude: lon }));
              }}
            />
          </div>

          {error && (
            <div style={{ padding: "0.85rem", marginTop: "1.25rem", borderRadius: "10px", background: "rgba(244, 63, 94, 0.15)", border: "1px solid rgba(244, 63, 94, 0.3)", color: "#f87171", fontSize: "0.875rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <AlertTriangle size={18} />
              <span>{error}</span>
            </div>
          )}

          <button type="submit" className="btn-submit" disabled={loading}>
            {loading ? (
              <>
                <div className="spinner" /> Calculating Valuation...
              </>
            ) : (
              <>
                <Sparkles size={20} /> Run ML Valuation Predictor
              </>
            )}
          </button>
        </form>
      </div>

      {/* Right Column - Prediction Results Display */}
      {result && (
        <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
          <div className="result-box">
            <div style={{ textTransform: "uppercase", letterSpacing: "0.1em", fontSize: "0.8rem", color: "var(--text-secondary)", fontWeight: 700 }}>
              Estimated Market Value
            </div>
            <div className="result-price">{result.predicted_price}</div>
            
            <div className="confidence-badge" style={{ marginBottom: "1rem" }}>
              <CheckCircle2 size={16} /> Confidence Range: {result.confidence_range}
            </div>

            <p style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
              Estimated using Random Forest Regressor trained on California Census Data ({result.predicted_price_short}).
            </p>
          </div>

          {/* Detailed Breakdown Card */}
          <div className="glass-card">
            <h3 style={{ fontSize: "1.05rem", marginBottom: "1rem", color: "var(--text-main)" }}>
              📊 Property Metrics Summary
            </h3>
            
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
              <div style={{ background: "rgba(15, 23, 42, 0.6)", padding: "1rem", borderRadius: "12px", border: "1px solid var(--border-color)" }}>
                <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Est. Price / Room</span>
                <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#60a5fa", marginTop: "0.2rem" }}>
                  ${formData.AveRooms > 0 ? (parseInt(result.predicted_price.replace(/[^0-9]/g, "")) / formData.AveRooms).toLocaleString("en-US", { maximumFractionDigits: 0 }) : 0}
                </div>
              </div>

              <div style={{ background: "rgba(15, 23, 42, 0.6)", padding: "1rem", borderRadius: "12px", border: "1px solid var(--border-color)" }}>
                <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Location Coords</span>
                <div style={{ fontSize: "0.95rem", fontWeight: 600, color: "var(--text-main)", marginTop: "0.3rem" }}>
                  {formData.Latitude}° N, {formData.Longitude}° W
                </div>
              </div>

              <div style={{ background: "rgba(15, 23, 42, 0.6)", padding: "1rem", borderRadius: "12px", border: "1px solid var(--border-color)" }}>
                <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Est. Income Level</span>
                <div style={{ fontSize: "1.05rem", fontWeight: 600, color: "#34d399", marginTop: "0.2rem" }}>
                  ${(formData.MedInc * 10000).toLocaleString()}/yr
                </div>
              </div>

              <div style={{ background: "rgba(15, 23, 42, 0.6)", padding: "1rem", borderRadius: "12px", border: "1px solid var(--border-color)" }}>
                <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Structure Age</span>
                <div style={{ fontSize: "1.05rem", fontWeight: 600, color: "#a78bfa", marginTop: "0.2rem" }}>
                  {formData.HouseAge} Years Old
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
