/**
 * Chat interface with message display, input, and loading states.
 */
import { useState, useRef, useEffect } from 'react';

function formatMarkdown(text) {
  if (!text) return '';
  // Basic markdown to HTML conversion
  let html = text
    // Bold
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Italic
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    // Inline code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Links
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
    // Headers
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
    // Unordered lists
    .replace(/^\* (.*$)/gm, '<li>$1</li>')
    .replace(/^- (.*$)/gm, '<li>$1</li>')
    // Ordered lists
    .replace(/^\d+\. (.*$)/gm, '<li>$1</li>')
    // Line breaks
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br/>');

  // Wrap consecutive <li> items in <ul>
  html = html.replace(/((?:<li>.*?<\/li>\s*)+)/g, '<ul>$1</ul>');

  return `<p>${html}</p>`;
}

function MessageBubble({ message, agents }) {
  const agentInfo = agents?.find(a => a.name === message.agent);

  return (
    <div
      className={`message message-${message.role}`}
      role="article"
      aria-label={`${message.role === 'user' ? 'You' : 'Election Buddy'} said`}
    >
      <div className="message-avatar" aria-hidden="true">
        {message.role === 'user' ? '👤' : '🗳️'}
      </div>
      <div className="message-bubble">
        <div
          className="message-content"
          dangerouslySetInnerHTML={{ __html: formatMarkdown(message.content) }}
        />
        {message.role === 'assistant' && agentInfo && (
          <div className="message-agent-tag">
            <span className="message-agent-dot" style={{ background: agentInfo.color }} />
            {agentInfo.icon} {agentInfo.title}
          </div>
        )}
      </div>
    </div>
  );
}

function LoadingBubble() {
  return (
    <div className="message message-assistant" role="status" aria-label="Election Buddy is thinking">
      <div className="message-avatar" aria-hidden="true">🗳️</div>
      <div className="message-bubble">
        <div className="loading-dots">
          <div className="loading-dot" />
          <div className="loading-dot" />
          <div className="loading-dot" />
        </div>
      </div>
    </div>
  );
}

export default function ChatInterface({ messages, onSendMessage, isLoading, agents, error }) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  function handleSubmit(e) {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput('');
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  return (
    <div className="chat-container" id="chat-container">
      {error && (
        <div className="error-banner" role="alert" id="error-banner">
          ⚠️ {error}
        </div>
      )}

      <div
        className="chat-messages"
        role="log"
        aria-label="Chat messages"
        aria-live="polite"
        id="chat-messages"
      >
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} agents={agents} />
        ))}
        {isLoading && <LoadingBubble />}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <form onSubmit={handleSubmit} className="chat-input-wrapper" id="chat-input-form">
          <label htmlFor="chat-input" className="sr-only">
            Type your question about Indian elections
          </label>
          <textarea
            id="chat-input"
            ref={inputRef}
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about Indian elections, voter registration, candidates..."
            rows={1}
            disabled={isLoading}
            aria-label="Chat message input"
          />
          <button
            type="submit"
            className="chat-send-btn"
            disabled={!input.trim() || isLoading}
            aria-label="Send message"
            id="send-btn"
          >
            ➤
          </button>
        </form>
        <p className="chat-disclaimer">
          Election Buddy 🇮🇳 provides educational information only. Always verify with official ECI sources.
        </p>
      </div>
    </div>
  );
}
