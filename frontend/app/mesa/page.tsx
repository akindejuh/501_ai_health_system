"use client";

/**
 * MESA (Medical Expert System Assistant) Main Page
 * Production-grade futuristic medical diagnostic interface
 */

import { useEffect } from "react";
import { useMesaStore } from "@/lib/api/stores/mesaStore";
import { MesaHeader, MesaChat, MesaExpert, MesaVoiceOverlay } from "@/components/mesa";
import { cn } from "@/lib/utils";

export default function MesaPage() {
  const { mode, initialize, isInitialized, isLoading, error } = useMesaStore();

  // Initialize MESA on mount
  useEffect(() => {
    initialize();
  }, [initialize]);

  // Loading state
  if (!isInitialized && isLoading) {
    return (
      <div className="mesa-loading-screen">
        <div className="mesa-loading-content">
          <div className="mesa-loading-logo">
            <div className="mesa-loading-orb">
              <div className="mesa-loading-ring" />
              <div className="mesa-loading-ring" />
              <div className="mesa-loading-ring" />
              <div className="mesa-loading-core" />
            </div>
          </div>
          <h1 className="mesa-loading-title">MESA</h1>
          <p className="mesa-loading-text">Initializing Medical Expert System...</p>
          <div className="mesa-loading-bar">
            <div className="mesa-loading-progress" />
          </div>
        </div>
      </div>
    );
  }

  // Error state during initialization
  if (!isInitialized && error) {
    return (
      <div className="mesa-error-screen">
        <div className="mesa-error-content">
          <div className="mesa-error-icon">⚠️</div>
          <h1 className="mesa-error-title">Connection Error</h1>
          <p className="mesa-error-text">{error}</p>
          <button onClick={initialize} className="mesa-error-retry">
            Retry Connection
          </button>
          <p className="mesa-error-hint">
            Make sure the MESA backend is running at{" "}
            <code>http://localhost:8000</code>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="mesa-app">
      {/* Background effects */}
      <div className="mesa-bg">
        <div className="mesa-bg-grid" />
        <div className="mesa-bg-glow glow-1" />
        <div className="mesa-bg-glow glow-2" />
        <div className="mesa-bg-gradient" />
      </div>

      {/* Header */}
      <MesaHeader />

      {/* Main content area */}
      <main className={cn("mesa-main", mode)}>
        {mode === "chat" && <MesaChat />}
        {mode === "expert" && <MesaExpert />}
        {mode === "voice" && (
          <div className="mesa-voice-placeholder">
            <p>Voice mode is active</p>
          </div>
        )}
      </main>

      {/* Voice overlay (portal) */}
      <MesaVoiceOverlay />
    </div>
  );
}
