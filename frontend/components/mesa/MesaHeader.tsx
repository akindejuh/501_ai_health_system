"use client";

/**
 * MESA Header Component
 * Futuristic header with mode switcher and branding
 */

import { useMesaStore } from "@/lib/api/stores/mesaStore";
import type { MesaMode, ModelInfo } from "@/lib/api/types/mesa.types";
import { cn } from "@/lib/utils";

const modeConfig: Record<MesaMode, { icon: string; label: string; description: string }> = {
  chat: {
    icon: "💬",
    label: "AI Chat",
    description: "Natural language medical assistant",
  },
  expert: {
    icon: "🔬",
    label: "Expert System",
    description: "Rule-based diagnostic engine",
  },
  voice: {
    icon: "🎤",
    label: "Voice Mode",
    description: "Speak with MESA (Coming Soon)",
  },
};

export function MesaHeader() {
  const {
    mode,
    setMode,
    selectedModel,
    setSelectedModel,
    availableModels,
    isLoading,
    activateVoiceMode,
  } = useMesaStore();

  const handleModeChange = (newMode: MesaMode) => {
    if (newMode === "voice") {
      activateVoiceMode();
    } else {
      setMode(newMode);
    }
  };

  return (
    <header className="mesa-header">
      <div className="mesa-header-content">
        {/* Logo & Branding */}
        <div className="mesa-brand">
          <div className="mesa-logo">
            <div className="mesa-logo-icon">
              <span className="mesa-logo-pulse" />
              <svg
                viewBox="0 0 24 24"
                fill="none"
                className="mesa-logo-svg"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"
                  fill="currentColor"
                  opacity="0.3"
                />
                <path
                  d="M12 6v6l4 2"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
                <path
                  d="M8 12h8M12 8v8"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  opacity="0.5"
                />
              </svg>
            </div>
          </div>
          <div className="mesa-brand-text">
            <h1 className="mesa-title">MESA</h1>
            <p className="mesa-subtitle">Medical Expert System Assistant</p>
          </div>
        </div>

        {/* Mode Switcher */}
        <nav className="mesa-mode-switcher">
          {(Object.keys(modeConfig) as MesaMode[]).map((modeKey) => {
            const config = modeConfig[modeKey];
            const isActive = mode === modeKey;
            
            return (
              <button
                key={modeKey}
                onClick={() => handleModeChange(modeKey)}
                className={cn("mesa-mode-btn", isActive && "active")}
                title={config.description}
              >
                <span className="mesa-mode-icon">{config.icon}</span>
                <span className="mesa-mode-label">{config.label}</span>
                {isActive && <span className="mesa-mode-indicator" />}
              </button>
            );
          })}
        </nav>

        {/* Model Selector (shown in chat mode) */}
        {mode === "chat" && (
          <div className="mesa-model-selector">
            <label className="mesa-model-label">
              <span className="mesa-model-icon">🤖</span>
              <span>Model</span>
            </label>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              disabled={isLoading}
              className="mesa-model-select"
            >
              {availableModels.map((model: ModelInfo) => (
                <option key={model.id} value={model.id}>
                  {model.name}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Status Indicator */}
        <div className="mesa-status">
          <span className={cn("mesa-status-dot", isLoading ? "loading" : "online")} />
          <span className="mesa-status-text">
            {isLoading ? "Processing..." : "Online"}
          </span>
        </div>
      </div>
    </header>
  );
}
