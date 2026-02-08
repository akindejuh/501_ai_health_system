"use client";

/**
 * MESA Chat Component
 * Futuristic AI chat interface with symptom extraction display
 */

import { useState, useRef, useEffect, FormEvent, KeyboardEvent } from "react";
import { useMesaStore } from "@/lib/api/stores/mesaStore";
import { cn } from "@/lib/utils";

export function MesaChat() {
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const {
    conversationHistory = [],
    sendMessage,
    clearConversation,
    isLoading,
    error,
    extractedSymptoms = [],
    suggestedDiseases = [],
    selectedModel,
  } = useMesaStore();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversationHistory]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const message = inputValue.trim();
    setInputValue("");
    await sendMessage(message);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  }, [inputValue]);

  return (
    <div className="mesa-chat">
      {/* Chat Messages Area */}
      <div className="mesa-chat-messages">
        {conversationHistory.length === 0 ? (
          <div className="mesa-chat-empty">
            <div className="mesa-chat-empty-icon">
              <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="40" cy="40" r="35" stroke="currentColor" strokeWidth="2" opacity="0.2" />
                <circle cx="40" cy="40" r="25" stroke="currentColor" strokeWidth="2" opacity="0.3" />
                <circle cx="40" cy="40" r="15" stroke="currentColor" strokeWidth="2" opacity="0.4" />
                <circle cx="40" cy="40" r="5" fill="currentColor" opacity="0.6" />
              </svg>
            </div>
            <h3 className="mesa-chat-empty-title">Start a Conversation</h3>
            <p className="mesa-chat-empty-text">
              Describe your symptoms to MESA. I&apos;ll help guide you through a
              medical assessment and provide relevant information.
            </p>
            <div className="mesa-chat-suggestions">
              <p className="mesa-chat-suggestions-label">Try asking:</p>
              <div className="mesa-chat-suggestion-chips">
                {[
                  "I've been having fever and chills for 3 days",
                  "What are the symptoms of malaria?",
                  "I have stomach pain after eating street food",
                ].map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => setInputValue(suggestion)}
                    className="mesa-chat-suggestion-chip"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <>
            {conversationHistory.map((message, index) => (
              <div
                key={index}
                className={cn(
                  "mesa-chat-message",
                  message.role === "user" ? "user" : "assistant"
                )}
              >
                <div className="mesa-chat-message-avatar">
                  {message.role === "user" ? (
                    <span>👤</span>
                  ) : (
                    <span className="mesa-avatar-pulse">🏥</span>
                  )}
                </div>
                <div className="mesa-chat-message-content">
                  <div className="mesa-chat-message-header">
                    <span className="mesa-chat-message-sender">
                      {message.role === "user" ? "You" : "MESA"}
                    </span>
                    {message.role === "assistant" && (
                      <span className="mesa-chat-message-model">
                        via {selectedModel.split("-")[0]}
                      </span>
                    )}
                  </div>
                  <div className="mesa-chat-message-text">
                    {message.content}
                  </div>
                </div>
              </div>
            ))}
            
            {/* Loading indicator */}
            {isLoading && (
              <div className="mesa-chat-message assistant">
                <div className="mesa-chat-message-avatar">
                  <span className="mesa-avatar-pulse">🏥</span>
                </div>
                <div className="mesa-chat-message-content">
                  <div className="mesa-chat-typing">
                    <span className="mesa-chat-typing-dot" />
                    <span className="mesa-chat-typing-dot" />
                    <span className="mesa-chat-typing-dot" />
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Extracted Data Panel */}
      {(extractedSymptoms.length > 0 || suggestedDiseases.length > 0) && (
        <div className="mesa-chat-extracted">
          {extractedSymptoms.length > 0 && (
            <div className="mesa-extracted-section">
              <span className="mesa-extracted-label">Detected Symptoms:</span>
              <div className="mesa-extracted-tags">
                {extractedSymptoms.map((symptom) => (
                  <span key={symptom} className="mesa-extracted-tag symptom">
                    {symptom.replace(/_/g, " ")}
                  </span>
                ))}
              </div>
            </div>
          )}
          {suggestedDiseases.length > 0 && (
            <div className="mesa-extracted-section">
              <span className="mesa-extracted-label">Possible Conditions:</span>
              <div className="mesa-extracted-tags">
                {suggestedDiseases.map((disease) => (
                  <span key={disease} className="mesa-extracted-tag disease">
                    {disease.replace(/_/g, " ")}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mesa-chat-error">
          <span className="mesa-chat-error-icon">⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="mesa-chat-input-area">
        <div className="mesa-chat-input-wrapper">
          <textarea
            ref={textareaRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your symptoms..."
            disabled={isLoading}
            rows={1}
            className="mesa-chat-input"
          />
          <div className="mesa-chat-input-actions">
            {conversationHistory.length > 0 && (
              <button
                type="button"
                onClick={clearConversation}
                className="mesa-chat-clear-btn"
                title="Clear conversation"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            )}
            <button
              type="submit"
              disabled={!inputValue.trim() || isLoading}
              className="mesa-chat-send-btn"
            >
              {isLoading ? (
                <span className="mesa-chat-send-loading" />
              ) : (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
                </svg>
              )}
            </button>
          </div>
        </div>
        <p className="mesa-chat-disclaimer">
          MESA provides information only. Always consult a healthcare professional.
        </p>
      </form>
    </div>
  );
}
