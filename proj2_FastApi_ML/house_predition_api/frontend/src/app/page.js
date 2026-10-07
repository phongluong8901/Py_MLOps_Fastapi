"use client";

import React, { useState, useEffect } from "react";
import { Building2, Sparkles, Layers, BookOpen, Activity, Server, Settings } from "lucide-react";
import SinglePredictForm from "@/components/SinglePredictForm";
import BatchPredictForm from "@/components/BatchPredictForm";
import DocsTab from "@/components/DocsTab";

export default function Home() {
  const [activeTab, setActiveTab] = useState("single");
  const [backendUrl, setBackendUrl] = useState("http://localhost:8000");
  const [apiStatus, setApiStatus] = useState({ status: "checking", details: null });
  const [showSettings, setShowSettings] = useState(false);

  // Check health of backend API
  const checkHealth = async (url) => {
    setApiStatus({ status: "checking", details: null });
    try {
      const res = await fetch(`${url}/health`, { cache: "no-store" });
      if (!res.ok) throw new Error("Server error");
      const data = await res.json();
      setApiStatus({ status: "online", details: data });
    } catch {
      setApiStatus({ status: "offline", details: null });
    }
  };

  useEffect(() => {
    checkHealth(backendUrl);
    const interval = setInterval(() => checkHealth(backendUrl), 10000);
    return () => clearInterval(interval);
  }, [backendUrl]);

  return (
    <main className="app-container">
      {/* Top Header */}
      <header className="header-bar">
        <div className="logo-section">
          <div className="logo-icon">
            <Building2 size={26} />
          </div>
          <div>
            <h1 style={{ fontSize: "1.6rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
              California Real Estate <span className="gradient-text">AI Predictor</span>
            </h1>
            <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>
              ML-Powered Property Valuation Studio • Random Forest Engine
            </p>
          </div>
        </div>

        {/* Status Indicator & Settings */}
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <div className="api-status-badge">
            <span
              className={`status-dot ${
                apiStatus.status === "online"
                  ? "status-online"
                  : apiStatus.status === "offline"
                  ? "status-offline"
                  : "status-checking"
              }`}
            />
            <span>
              Backend API:{" "}
              {apiStatus.status === "online" ? (
                <strong style={{ color: "#34d399" }}>Online ({apiStatus.details?.model || "FastAPI"})</strong>
              ) : apiStatus.status === "offline" ? (
                <strong style={{ color: "#f87171" }}>Offline (Check Port 8000)</strong>
              ) : (
                "Connecting..."
              )}
            </span>
          </div>

          <button
            type="button"
            className="preset-chip"
            style={{ padding: "0.5rem 0.75rem" }}
            onClick={() => setShowSettings(!showSettings)}
            title="Backend Configuration"
          >
            <Settings size={18} />
          </button>
        </div>
      </header>

      {/* Backend Settings Panel */}
      {showSettings && (
        <div className="glass-card" style={{ marginBottom: "1.5rem", border: "1px solid rgba(59, 130, 246, 0.4)" }}>
          <h3 style={{ fontSize: "1rem", marginBottom: "0.75rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <Server size={18} color="#3b82f6" /> FastAPI Backend Configuration
          </h3>
          <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
            <input
              type="text"
              className="custom-input"
              style={{ maxWidth: "400px" }}
              value={backendUrl}
              onChange={(e) => setBackendUrl(e.target.value)}
              placeholder="http://localhost:8000"
            />
            <button
              type="button"
              className="tab-btn active"
              onClick={() => checkHealth(backendUrl)}
            >
              Test Connection
            </button>
          </div>
        </div>
      )}

      {/* Navigation Tabs */}
      <nav className="tab-nav">
        <button
          className={`tab-btn ${activeTab === "single" ? "active" : ""}`}
          onClick={() => setActiveTab("single")}
        >
          <Sparkles size={18} /> Single House Valuation
        </button>

        <button
          className={`tab-btn ${activeTab === "batch" ? "active" : ""}`}
          onClick={() => setActiveTab("batch")}
        >
          <Layers size={18} /> Batch CSV Valuation
        </button>

        <button
          className={`tab-btn ${activeTab === "docs" ? "active" : ""}`}
          onClick={() => setActiveTab("docs")}
        >
          <BookOpen size={18} /> API & Model Docs
        </button>
      </nav>

      {/* Main Tab Content */}
      <section>
        {activeTab === "single" && <SinglePredictForm backendUrl={backendUrl} />}
        {activeTab === "batch" && <BatchPredictForm backendUrl={backendUrl} />}
        {activeTab === "docs" && <DocsTab backendUrl={backendUrl} />}
      </section>
    </main>
  );
}
