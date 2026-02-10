"use client";

/**
 * MESA Chat Component
 * Futuristic AI chat interface with markdown support and enhanced controls
 */

import {
  useState,
  useRef,
  useEffect,
  FormEvent,
  KeyboardEvent,
  useCallback,
} from "react";
import { createPortal } from "react-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useMesaStore } from "@/lib/api/stores/mesaStore";
import { cn } from "@/lib/utils";

/* ============================================================================
   ICONS
============================================================================ */

const CopyIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
    <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />
  </svg>
);

const CheckIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <polyline points="20,6 9,17 4,12" />
  </svg>
);

const EditIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
    <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
  </svg>
);

const ExpandIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <polyline points="15,3 21,3 21,9" />
    <polyline points="9,21 3,21 3,15" />
    <line x1="21" y1="3" x2="14" y2="10" />
    <line x1="3" y1="21" x2="10" y2="14" />
  </svg>
);

const CollapseIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <polyline points="4,14 10,14 10,20" />
    <polyline points="20,10 14,10 14,4" />
    <line x1="14" y1="10" x2="21" y2="3" />
    <line x1="3" y1="21" x2="10" y2="14" />
  </svg>
);

const RegenerateIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <polyline points="1,4 1,10 7,10" />
    <path d="M3.51 15a9 9 0 102.13-9.36L1 10" />
  </svg>
);

/* ============================================================================
   MESSAGE BUBBLE COMPONENT
============================================================================ */

interface MessageBubbleProps {
  content: string;
  role: "user" | "assistant";
  selectedModel: string;
  onEdit?: (newContent: string) => void;
  onRegenerate?: () => void;
  isLastAssistant?: boolean;
}

function MessageBubble({
  content,
  role,
  selectedModel,
  onEdit,
  onRegenerate,
  isLastAssistant,
}: MessageBubbleProps) {
  const [copied, setCopied] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(content);
  const editRef = useRef<HTMLTextAreaElement>(null);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  }, [content]);

  const handleEdit = useCallback(() => {
    if (onEdit && editValue.trim() && editValue !== content) {
      onEdit(editValue.trim());
    }
    setIsEditing(false);
  }, [onEdit, editValue, content]);

  const handleCancelEdit = useCallback(() => {
    setEditValue(content);
    setIsEditing(false);
  }, [content]);

  useEffect(() => {
    if (isEditing && editRef.current) {
      editRef.current.focus();
      editRef.current.setSelectionRange(editValue.length, editValue.length);
    }
  }, [isEditing, editValue.length]);

  return (
    <div className={cn("mesa-chat-message", role)}>
      <div className="mesa-chat-message-avatar">
        {role === "user" ? (
          <span>👤</span>
        ) : (
          <span className="mesa-avatar-pulse">🏥</span>
        )}
      </div>
      <div className="mesa-chat-message-content">
        <div className="mesa-chat-message-header">
          <span className="mesa-chat-message-sender">
            {role === "user" ? "You" : "MESA"}
          </span>
          {role === "assistant" && (
            <span className="mesa-chat-message-model">
              via {selectedModel.split("-")[0]}
            </span>
          )}
        </div>

        {/* Message Content */}
        {isEditing ? (
          <div className="mesa-chat-edit-container">
            <textarea
              ref={editRef}
              value={editValue}
              onChange={(e) => setEditValue(e.target.value)}
              className="mesa-chat-edit-input"
              rows={3}
            />
            <div className="mesa-chat-edit-actions">
              <button onClick={handleCancelEdit} className="mesa-chat-edit-cancel">
                Cancel
              </button>
              <button onClick={handleEdit} className="mesa-chat-edit-save">
                Save & Resend
              </button>
            </div>
          </div>
        ) : (
          <div className="mesa-chat-message-text">
            {role === "assistant" ? (
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  // Custom code block rendering
                  code({ className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || "");
                    const isInline = !match && !className;
                    return isInline ? (
                      <code className="mesa-inline-code" {...props}>
                        {children}
                      </code>
                    ) : (
                      <div className="mesa-code-block">
                        {match && (
                          <div className="mesa-code-header">
                            <span>{match[1]}</span>
                          </div>
                        )}
                        <pre>
                          <code className={className} {...props}>
                            {children}
                          </code>
                        </pre>
                      </div>
                    );
                  },
                  // Custom table rendering
                  table({ children }) {
                    return (
                      <div className="mesa-table-wrapper">
                        <table>{children}</table>
                      </div>
                    );
                  },
                  // Custom link rendering
                  a({ href, children }) {
                    return (
                      <a
                        href={href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="mesa-link"
                      >
                        {children}
                      </a>
                    );
                  },
                }}
              >
                {content}
              </ReactMarkdown>
            ) : (
              content
            )}
          </div>
        )}

        {/* Message Controls */}
        {!isEditing && (
          <div className="mesa-chat-message-controls">
            <button
              onClick={handleCopy}
              className="mesa-chat-control-btn"
              title="Copy message"
            >
              {copied ? <CheckIcon /> : <CopyIcon />}
              <span>{copied ? "Copied!" : "Copy"}</span>
            </button>

            {role === "user" && onEdit && (
              <button
                onClick={() => setIsEditing(true)}
                className="mesa-chat-control-btn"
                title="Edit message"
              >
                <EditIcon />
                <span>Edit</span>
              </button>
            )}

            {role === "assistant" && isLastAssistant && onRegenerate && (
              <button
                onClick={onRegenerate}
                className="mesa-chat-control-btn"
                title="Regenerate response"
              >
                <RegenerateIcon />
                <span>Regenerate</span>
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

/* ============================================================================
   MAIN CHAT COMPONENT
============================================================================ */

export function MesaChat() {
  const [inputValue, setInputValue] = useState("");
  const [isExpanded, setIsExpanded] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const store = useMesaStore();
  const conversationHistory = store.conversationHistory ?? [];
  const extractedSymptoms = store.extractedSymptoms ?? [];
  const suggestedDiseases = store.suggestedDiseases ?? [];
  const { sendMessage, clearConversation, isLoading, error, selectedModel } = store;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversationHistory]);

  // Handle escape key to exit fullscreen
  useEffect(() => {
    const handleEscape = (e: globalThis.KeyboardEvent) => {
      if (e.key === "Escape" && isExpanded) {
        setIsExpanded(false);
      }
    };
    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [isExpanded]);

  // Lock body scroll when expanded
  useEffect(() => {
    if (isExpanded) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [isExpanded]);

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

  // Edit user message and resend
  const handleEditMessage = useCallback(
    async (index: number, newContent: string) => {
      // Clear conversation from this point and resend
      clearConversation();
      // Re-add messages before this one
      // For simplicity, we just send the new message
      await sendMessage(newContent);
    },
    [clearConversation, sendMessage]
  );

  // Regenerate last assistant response
  const handleRegenerate = useCallback(async () => {
    if (conversationHistory.length < 2) return;
    // Find the last user message
    const lastUserMsg = [...conversationHistory]
      .reverse()
      .find((m) => m.role === "user");
    if (lastUserMsg) {
      clearConversation();
      await sendMessage(lastUserMsg.content);
    }
  }, [conversationHistory, clearConversation, sendMessage]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  }, [inputValue]);

  // Find last assistant message index
  const lastAssistantIndex = conversationHistory
    .map((m, i) => (m.role === "assistant" ? i : -1))
    .filter((i) => i !== -1)
    .pop();

  const chatContent = (
    <div className={cn("mesa-chat", isExpanded && "mesa-chat-expanded")}>
      {/* Expand/Collapse Header */}
      <div className="mesa-chat-toolbar">
        <div className="mesa-chat-toolbar-left">
          {conversationHistory.length > 0 && (
            <span className="mesa-chat-message-count">
              {conversationHistory.length} messages
            </span>
          )}
        </div>
        <div className="mesa-chat-toolbar-right">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="mesa-chat-expand-btn"
            title={isExpanded ? "Exit fullscreen (Esc)" : "Fullscreen"}
            aria-label={isExpanded ? "Exit fullscreen" : "Expand to fullscreen"}
          >
            {isExpanded ? <CollapseIcon /> : <ExpandIcon />}
          </button>
        </div>
      </div>

      {/* Chat Messages Area */}
      <div className="mesa-chat-messages">
        {conversationHistory.length === 0 ? (
          <div className="mesa-chat-empty">
            <div className="mesa-chat-empty-icon">
              <svg
                viewBox="0 0 80 80"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <circle
                  cx="40"
                  cy="40"
                  r="35"
                  stroke="currentColor"
                  strokeWidth="2"
                  opacity="0.2"
                />
                <circle
                  cx="40"
                  cy="40"
                  r="25"
                  stroke="currentColor"
                  strokeWidth="2"
                  opacity="0.3"
                />
                <circle
                  cx="40"
                  cy="40"
                  r="15"
                  stroke="currentColor"
                  strokeWidth="2"
                  opacity="0.4"
                />
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
              <MessageBubble
                key={index}
                content={message.content}
                role={message.role as "user" | "assistant"}
                selectedModel={selectedModel}
                onEdit={
                  message.role === "user"
                    ? (newContent) => handleEditMessage(index, newContent)
                    : undefined
                }
                onRegenerate={handleRegenerate}
                isLastAssistant={index === lastAssistantIndex}
              />
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
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
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
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
                </svg>
              )}
            </button>
          </div>
        </div>
        <p className="mesa-chat-disclaimer">
          MESA provides information only. Always consult a healthcare
          professional.
        </p>
      </form>
    </div>
  );

  // Use portal when expanded to break out of parent stacking context
  if (isExpanded && typeof document !== "undefined") {
    return createPortal(chatContent, document.body);
  }

  return chatContent;
}
