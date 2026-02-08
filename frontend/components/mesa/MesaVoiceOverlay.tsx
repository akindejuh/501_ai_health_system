"use client";

/**
 * MESA Voice Overlay Component
 * Futuristic voice interface with audio visualization
 */

import { useEffect, useRef, useState, useCallback } from "react";
import { useMesaStore } from "@/lib/api/stores/mesaStore";
import { cn } from "@/lib/utils";

const VOICE_AUDIO_PATH = "/mesa/recordings/mesa_voice_chat_not_ready.wav";

export function MesaVoiceOverlay() {
  const { isVoiceActive, isVoicePlaying, deactivateVoiceMode, setVoicePlaying } =
    useMesaStore();
  
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>(0);
  const sourceRef = useRef<MediaElementAudioSourceNode | null>(null);
  
  const [isLoaded, setIsLoaded] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const [hasInteracted, setHasInteracted] = useState(false);

  // Initialize audio context and connect analyzer
  const initializeAudio = useCallback(() => {
    if (!audioRef.current || sourceRef.current) return;

    try {
      audioContextRef.current = new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      analyserRef.current.fftSize = 256;
      
      sourceRef.current = audioContextRef.current.createMediaElementSource(audioRef.current);
      sourceRef.current.connect(analyserRef.current);
      analyserRef.current.connect(audioContextRef.current.destination);
    } catch {
      console.warn("Audio context initialization failed");
    }
  }, []);

  // Start playing the audio
  const startVoice = useCallback(async () => {
    if (!audioRef.current) return;
    
    setHasInteracted(true);
    initializeAudio();
    
    try {
      if (audioContextRef.current?.state === "suspended") {
        await audioContextRef.current.resume();
      }
      await audioRef.current.play();
      setVoicePlaying(true);
    } catch (error) {
      console.error("Failed to play audio:", error);
    }
  }, [initializeAudio, setVoicePlaying]);

  // Stop playing the audio
  const stopVoice = useCallback(() => {
    if (!audioRef.current) return;
    audioRef.current.pause();
    audioRef.current.currentTime = 0;
    setVoicePlaying(false);
  }, [setVoicePlaying]);

  // Handle close overlay
  const handleClose = useCallback(() => {
    stopVoice();
    deactivateVoiceMode();
  }, [stopVoice, deactivateVoiceMode]);

  // Visualizer animation
  useEffect(() => {
    if (!isVoicePlaying || !analyserRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const analyser = analyserRef.current;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const draw = () => {
      animationRef.current = requestAnimationFrame(draw);
      analyser.getByteFrequencyData(dataArray);

      // Calculate average level for the orb size
      const average = dataArray.reduce((a, b) => a + b, 0) / bufferLength;
      setAudioLevel(average / 255);

      // Clear canvas
      ctx.fillStyle = "rgba(0, 0, 0, 0)";
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const baseRadius = 80;

      // Draw frequency bars in a circular pattern
      const barCount = 64;
      const step = Math.floor(bufferLength / barCount);

      for (let i = 0; i < barCount; i++) {
        const value = dataArray[i * step] / 255;
        const angle = (i / barCount) * Math.PI * 2 - Math.PI / 2;
        const barLength = 30 + value * 70;

        const x1 = centerX + Math.cos(angle) * baseRadius;
        const y1 = centerY + Math.sin(angle) * baseRadius;
        const x2 = centerX + Math.cos(angle) * (baseRadius + barLength);
        const y2 = centerY + Math.sin(angle) * (baseRadius + barLength);

        // Create gradient for each bar
        const gradient = ctx.createLinearGradient(x1, y1, x2, y2);
        gradient.addColorStop(0, `rgba(0, 255, 200, ${0.3 + value * 0.5})`);
        gradient.addColorStop(1, `rgba(0, 200, 255, ${0.1 + value * 0.3})`);

        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 3;
        ctx.lineCap = "round";
        ctx.stroke();
      }

      // Draw inner glow
      const innerGradient = ctx.createRadialGradient(
        centerX,
        centerY,
        0,
        centerX,
        centerY,
        baseRadius
      );
      innerGradient.addColorStop(0, `rgba(0, 255, 200, ${0.2 + average / 255 * 0.3})`);
      innerGradient.addColorStop(0.7, `rgba(0, 200, 255, ${0.1 + average / 255 * 0.2})`);
      innerGradient.addColorStop(1, "rgba(0, 0, 0, 0)");

      ctx.beginPath();
      ctx.arc(centerX, centerY, baseRadius, 0, Math.PI * 2);
      ctx.fillStyle = innerGradient;
      ctx.fill();
    };

    draw();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isVoicePlaying]);

  // Handle audio end
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleEnded = () => {
      setVoicePlaying(false);
    };

    audio.addEventListener("ended", handleEnded);
    return () => audio.removeEventListener("ended", handleEnded);
  }, [setVoicePlaying]);

  // ESC key to close
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isVoiceActive) {
        handleClose();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isVoiceActive, handleClose]);

  if (!isVoiceActive) return null;

  return (
    <div className="mesa-voice-overlay">
      {/* Background particles */}
      <div className="mesa-voice-particles">
        {Array.from({ length: 30 }).map((_, i) => (
          <div
            key={i}
            className="mesa-voice-particle"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${3 + Math.random() * 4}s`,
            }}
          />
        ))}
      </div>

      {/* Main content */}
      <div className="mesa-voice-content">
        {/* Close button */}
        <button onClick={handleClose} className="mesa-voice-close">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        </button>

        {/* Title */}
        <div className="mesa-voice-header">
          <h2 className="mesa-voice-title">MESA Voice</h2>
          <p className="mesa-voice-subtitle">
            {isVoicePlaying ? "MESA is speaking..." : "Voice Interface Preview"}
          </p>
        </div>

        {/* Visualizer orb */}
        <div
          className={cn("mesa-voice-orb", isVoicePlaying && "active")}
          style={{
            transform: `scale(${1 + audioLevel * 0.3})`,
          }}
        >
          <canvas
            ref={canvasRef}
            width={400}
            height={400}
            className="mesa-voice-canvas"
          />
          <div className="mesa-voice-orb-inner">
            <div className="mesa-voice-orb-core" />
            <div className="mesa-voice-orb-ring ring-1" />
            <div className="mesa-voice-orb-ring ring-2" />
            <div className="mesa-voice-orb-ring ring-3" />
            {!isVoicePlaying && !hasInteracted && (
              <span className="mesa-voice-orb-text">🎤</span>
            )}
          </div>
        </div>

        {/* Controls */}
        <div className="mesa-voice-controls">
          {!isVoicePlaying ? (
            <button onClick={startVoice} className="mesa-voice-btn play">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 5v14l11-7z" />
              </svg>
              <span>Play Message</span>
            </button>
          ) : (
            <button onClick={stopVoice} className="mesa-voice-btn stop">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <rect x="6" y="6" width="12" height="12" rx="1" />
              </svg>
              <span>Stop</span>
            </button>
          )}
        </div>

        {/* Info text */}
        <p className="mesa-voice-info">
          Voice interaction with MESA is coming soon. This preview demonstrates
          the future voice interface experience.
        </p>

        {/* Hidden audio element */}
        <audio
          ref={audioRef}
          src={VOICE_AUDIO_PATH}
          preload="auto"
          onCanPlayThrough={() => setIsLoaded(true)}
          crossOrigin="anonymous"
        />

        {/* Loading state */}
        {!isLoaded && (
          <div className="mesa-voice-loading">
            <span className="mesa-voice-loading-spinner" />
            <span>Loading audio...</span>
          </div>
        )}
      </div>

      {/* Keyboard hint */}
      <div className="mesa-voice-hint">
        Press <kbd>ESC</kbd> to close
      </div>
    </div>
  );
}
