"use client";

import React, { useRef } from "react";
import { MapPin, Navigation } from "lucide-react";

export default function CaliforniaMap({ latitude, longitude, onChangeLocation }) {
  const mapRef = useRef(null);

  // CA bounds
  const MIN_LAT = 32.5;
  const MAX_LAT = 42.0;
  const MIN_LON = -124.5;
  const MAX_LON = -114.1;

  // Convert Lat/Lon to SVG % coordinates
  const getXY = (lat, lon) => {
    const clampedLat = Math.min(Math.max(lat, MIN_LAT), MAX_LAT);
    const clampedLon = Math.min(Math.max(lon, MIN_LON), MAX_LON);

    const xPct = ((clampedLon - MIN_LON) / (MAX_LON - MIN_LON)) * 100;
    const yPct = ((MAX_LAT - clampedLat) / (MAX_LAT - MIN_LAT)) * 100;
    return { x: xPct, y: yPct };
  };

  const currentPos = getXY(latitude, longitude);

  // Handle click on map to set lat/lon
  const handleMapClick = (e) => {
    if (!mapRef.current) return;
    const rect = mapRef.current.getBoundingClientRect();
    const xPct = (e.clientX - rect.left) / rect.width;
    const yPct = (e.clientY - rect.top) / rect.height;

    const newLon = MIN_LON + xPct * (MAX_LON - MIN_LON);
    const newLat = MAX_LAT - yPct * (MAX_LAT - MIN_LAT);

    onChangeLocation(
      parseFloat(newLat.toFixed(2)),
      parseFloat(newLon.toFixed(2))
    );
  };

  const presetCities = [
    { name: "San Francisco", lat: 37.77, lon: -122.41 },
    { name: "Los Angeles", lat: 34.05, lon: -118.24 },
    { name: "San Diego", lat: 32.71, lon: -117.16 },
    { name: "Sacramento", lat: 38.58, lon: -121.49 },
    { name: "San Jose", lat: 37.33, lon: -121.88 },
  ];

  return (
    <div className="form-group" style={{ gridColumn: "1 / -1" }}>
      <div className="form-label">
        <span style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
          <Navigation size={16} color="#3b82f6" /> Interactive Location Map (California)
        </span>
        <span className="form-sublabel">
          Lat: {latitude}° N | Lon: {longitude}° W
        </span>
      </div>

      <div
        ref={mapRef}
        onClick={handleMapClick}
        className="california-map-box"
        style={{ cursor: "crosshair", position: "relative" }}
      >
        {/* Simplified California Shape SVG */}
        <svg
          viewBox="0 0 400 400"
          className="map-svg-overlay"
          style={{ opacity: 0.85, width: "100%", height: "100%" }}
        >
          <defs>
            <linearGradient id="mapGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#1e293b" />
              <stop offset="100%" stopColor="#0f172a" />
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="3" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* Background Grid */}
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(255, 255, 255, 0.05)" strokeWidth="1" />
          </pattern>
          <rect width="400" height="400" fill="url(#grid)" />

          {/* Simplified California Border */}
          <path
            d="M 50,20 
               L 180,20 
               L 180,180 
               L 330,350 
               L 260,370 
               L 220,350 
               L 160,300 
               L 120,240 
               L 80,180 
               L 50,90 
               Z"
            fill="url(#mapGradient)"
            stroke="rgba(59, 130, 246, 0.5)"
            strokeWidth="2"
          />

          {/* City Markers */}
          {presetCities.map((city) => {
            const pos = getXY(city.lat, city.lon);
            return (
              <g key={city.name} transform={`translate(${(pos.x / 100) * 400}, ${(pos.y / 100) * 400})`}>
                <circle r="3" fill="#64748b" opacity="0.7" />
                <text
                  x="6"
                  y="3"
                  fill="#94a3b8"
                  fontSize="9"
                  fontFamily="sans-serif"
                  pointerEvents="none"
                >
                  {city.name}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Dynamic Selected Pin */}
        <div
          style={{
            position: "absolute",
            left: `${currentPos.x}%`,
            top: `${currentPos.y}%`,
            transform: "translate(-50%, -100%)",
            pointerEvents: "none",
            transition: "all 0.15s ease-out",
            zIndex: 10,
          }}
        >
          <div style={{ position: "relative" }}>
            <MapPin size={28} color="#34d399" fill="#10b981" style={{ filter: "drop-shadow(0 0 8px rgba(52,211,153,0.8))" }} />
            <div
              style={{
                position: "absolute",
                bottom: "-4px",
                left: "50%",
                transform: "translateX(-50%)",
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                backgroundColor: "#34d399",
                boxShadow: "0 0 12px 4px rgba(52, 211, 153, 0.8)",
                animation: "pulse 1.5s infinite"
              }}
            />
          </div>
        </div>

        <div style={{ position: "absolute", bottom: "8px", right: "12px", fontSize: "0.75rem", color: "#64748b" }}>
          💡 Click anywhere on map to pin coordinates
        </div>
      </div>
    </div>
  );
}
