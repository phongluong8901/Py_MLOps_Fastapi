"use client";

import React, { useState, useRef } from "react";
import { UploadCloud, FileText, Download, CheckCircle2, AlertTriangle, Play, Table, Layers } from "lucide-react";

export default function BatchPredictForm({ backendUrl }) {
  const [file, setFile] = useState(null);
  const [csvPreview, setCsvPreview] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [predictedRows, setPredictedRows] = useState([]);
  const [stats, setStats] = useState(null);
  const fileInputRef = useRef(null);

  const requiredColumns = [
    "MedInc", "HouseAge", "AveRooms", "AveBedrms", 
    "Population", "AveOccup", "Latitude", "Longitude"
  ];

  // Generate and download a sample CSV file
  const downloadSampleCsv = () => {
    const sampleContent = [
      "MedInc,HouseAge,AveRooms,AveBedrms,Population,AveOccup,Latitude,Longitude",
      "8.3252,41,6.9841,1.0238,322,2.5556,37.88,-122.23",
      "8.3014,21,6.2381,0.9719,2401,2.1098,37.86,-122.22",
      "7.2574,52,8.2881,1.0734,496,2.8023,37.85,-122.24",
      "5.6431,52,5.8173,1.0731,558,2.5479,37.85,-122.25",
      "3.8462,52,6.2818,1.0810,565,2.1815,37.85,-122.25",
      "4.0125,15,5.6000,1.0500,800,3.2000,34.05,-118.24"
    ].join("\n");

    const blob = new Blob([sampleContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", "sample_california_houses.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleFileSelect = (selectedFile) => {
    if (!selectedFile) return;

    if (!selectedFile.name.endsWith(".csv")) {
      setError("Please select a valid .csv file");
      return;
    }

    setFile(selectedFile);
    setError(null);
    setPredictedRows([]);
    setStats(null);

    // Read and parse preview
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target.result;
      const lines = text.split("\n").map(line => line.trim()).filter(line => line.length > 0);
      if (lines.length > 0) {
        const parsedHeaders = lines[0].split(",").map(h => h.trim().replace(/^"|"$/g, ''));
        setHeaders(parsedHeaders);

        const rows = lines.slice(1, 11).map(line => line.split(",").map(c => c.trim()));
        setCsvPreview(rows);
      }
    };
    reader.readAsText(selectedFile);
  };

  const handleSubmitBatch = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please choose a CSV file first");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${backendUrl}/predict-file`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errorText = await res.text();
        let errMsg = "Batch prediction failed";
        try {
          const jsonErr = JSON.parse(errorText);
          errMsg = jsonErr.detail || errMsg;
        } catch {
          errMsg = errorText || errMsg;
        }
        throw new Error(errMsg);
      }

      // Backend returns a CSV blob
      const blob = await res.blob();
      const csvText = await blob.text();

      // Trigger browser download
      const downloadUrl = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = downloadUrl;
      a.download = `predicted_${file.name}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      // Parse output CSV for display
      const lines = csvText.split("\n").map(l => l.trim()).filter(l => l.length > 0);
      if (lines.length > 1) {
        const resultHeaders = lines[0].split(",").map(h => h.trim());
        const dataRows = lines.slice(1).map(line => line.split(",").map(c => c.trim()));
        
        setHeaders(resultHeaders);
        setPredictedRows(dataRows);

        // Compute summary statistics
        const priceColIdx = resultHeaders.indexOf("predicted_price_usd");
        if (priceColIdx !== -1) {
          const prices = dataRows.map(row => {
            const raw = row[priceColIdx]?.replace(/[\$,]/g, "");
            return parseFloat(raw) || 0;
          });

          const total = prices.length;
          const avg = prices.reduce((a, b) => a + b, 0) / (total || 1);
          const max = Math.max(...prices);
          const min = Math.min(...prices);

          setStats({
            count: total,
            avgPrice: `$${avg.toLocaleString("en-US", { maximumFractionDigits: 0 })}`,
            maxPrice: `$${max.toLocaleString("en-US", { maximumFractionDigits: 0 })}`,
            minPrice: `$${min.toLocaleString("en-US", { maximumFractionDigits: 0 })}`
          });
        }
      }

    } catch (err) {
      setError(err.message || "An error occurred while uploading file");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
        <div>
          <h2 style={{ fontSize: "1.25rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <Layers size={22} color="#06b6d4" /> Batch Valuation via CSV Upload
          </h2>
          <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginTop: "0.2rem" }}>
            Upload a CSV containing multiple property rows to generate bulk predictions and download the output CSV.
          </p>
        </div>

        <button
          type="button"
          onClick={downloadSampleCsv}
          className="preset-chip"
          style={{ background: "rgba(6, 182, 212, 0.15)", borderColor: "rgba(6, 182, 212, 0.3)", color: "#22d3ee" }}
        >
          <Download size={16} /> Download Sample CSV
        </button>
      </div>

      {/* Drag & Drop Box */}
      <div
        className="dropzone"
        onClick={() => fileInputRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileSelect(e.dataTransfer.files[0]);
          }
        }}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          style={{ display: "none" }}
          onChange={(e) => e.target.files && handleFileSelect(e.target.files[0])}
        />
        <UploadCloud size={48} color="#06b6d4" style={{ marginBottom: "0.75rem" }} />
        <h4 style={{ fontSize: "1.1rem", marginBottom: "0.3rem" }}>
          {file ? file.name : "Click or drag & drop CSV file here"}
        </h4>
        <p style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
          Required columns: <code style={{ color: "#60a5fa" }}>{requiredColumns.join(", ")}</code>
        </p>
      </div>

      {error && (
        <div style={{ padding: "0.85rem", marginTop: "1.25rem", borderRadius: "10px", background: "rgba(244, 63, 94, 0.15)", border: "1px solid rgba(244, 63, 94, 0.3)", color: "#f87171", fontSize: "0.875rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Preview table if file uploaded */}
      {file && csvPreview.length > 0 && (
        <div style={{ marginTop: "1.5rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.5rem" }}>
            <span style={{ fontSize: "0.85rem", color: "var(--text-secondary)", fontWeight: 600 }}>
              📄 CSV Data Preview (First 10 rows)
            </span>
          </div>

          <div className="custom-table-container">
            <table className="custom-table">
              <thead>
                <tr>
                  {headers.map((h, idx) => (
                    <th key={idx}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {csvPreview.map((row, rIdx) => (
                  <tr key={rIdx}>
                    {row.map((val, cIdx) => (
                      <td key={cIdx}>{val}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <button
            type="button"
            onClick={handleSubmitBatch}
            className="btn-submit"
            disabled={loading}
            style={{ background: "linear-gradient(135deg, #06b6d4 0%, #0284c7 100%)" }}
          >
            {loading ? (
              <>
                <div className="spinner" /> Processing Batch Predictions...
              </>
            ) : (
              <>
                <Play size={18} /> Run Batch Valuation ({csvPreview.length}+ rows)
              </>
            )}
          </button>
        </div>
      )}

      {/* Batch Stats & Output Results Table */}
      {stats && (
        <div style={{ marginTop: "2rem", paddingTop: "1.5rem", borderTop: "1px solid var(--border-color)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "1rem" }}>
            <CheckCircle2 size={20} color="#10b981" />
            <h3 style={{ fontSize: "1.1rem", color: "#34d399" }}>
              Batch Valuation Completed & CSV Downloaded!
            </h3>
          </div>

          {/* Stats Bar */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "1rem", marginBottom: "1.5rem" }}>
            <div style={{ background: "rgba(15, 23, 42, 0.7)", padding: "1rem", borderRadius: "12px", border: "1px solid var(--border-color)" }}>
              <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Total Processed</span>
              <div style={{ fontSize: "1.3rem", fontWeight: 700, color: "var(--text-main)" }}>{stats.count} rows</div>
            </div>

            <div style={{ background: "rgba(15, 23, 42, 0.7)", padding: "1rem", borderRadius: "12px", border: "1px solid var(--border-color)" }}>
              <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Average House Price</span>
              <div style={{ fontSize: "1.3rem", fontWeight: 700, color: "#60a5fa" }}>{stats.avgPrice}</div>
            </div>

            <div style={{ background: "rgba(15, 23, 42, 0.7)", padding: "1rem", borderRadius: "12px", border: "1px solid var(--border-color)" }}>
              <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Highest Valuation</span>
              <div style={{ fontSize: "1.3rem", fontWeight: 700, color: "#34d399" }}>{stats.maxPrice}</div>
            </div>

            <div style={{ background: "rgba(15, 23, 42, 0.7)", padding: "1rem", borderRadius: "12px", border: "1px solid var(--border-color)" }}>
              <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Lowest Valuation</span>
              <div style={{ fontSize: "1.3rem", fontWeight: 700, color: "#a78bfa" }}>{stats.minPrice}</div>
            </div>
          </div>

          {/* Results Table preview */}
          <h4 style={{ fontSize: "0.95rem", marginBottom: "0.5rem", color: "var(--text-main)" }}>
            📊 Predicted Output Preview
          </h4>
          <div className="custom-table-container">
            <table className="custom-table">
              <thead>
                <tr>
                  {headers.map((h, idx) => (
                    <th key={idx} style={h === "predicted_price_usd" ? { color: "#34d399", fontWeight: 700 } : {}}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {predictedRows.map((row, rIdx) => (
                  <tr key={rIdx}>
                    {row.map((val, cIdx) => (
                      <td key={cIdx} style={headers[cIdx] === "predicted_price_usd" ? { color: "#34d399", fontWeight: 700 } : {}}>
                        {val}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
