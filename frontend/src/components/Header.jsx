/**
 * Header component with app branding, active agent badge, and controls.
 */
export default function Header({ onToggleSidebar, onNewChat, activeAgent, agents }) {
  const agentInfo = agents?.find(a => a.name === activeAgent);

  return (
    <header className="header" role="banner">
      <div className="header-left">
        <button
          className="btn btn-icon"
          onClick={onToggleSidebar}
          aria-label="Toggle sidebar"
          id="sidebar-toggle"
        >
          ☰
        </button>
        <div className="header-logo">
          <span className="header-logo-icon" role="img" aria-label="Indian flag">🇮🇳</span>
          <div>
            <div className="header-title">Election Buddy</div>
            <div className="header-subtitle">Your expert guide to Indian Elections 🇮🇳</div>
          </div>
        </div>
      </div>

      <div className="header-right">
        {agentInfo && (
          <div className="header-agent-badge" aria-live="polite">
            <span>{agentInfo.icon}</span>
            <span>{agentInfo.title}</span>
          </div>
        )}
        <button
          className="btn btn-ghost"
          onClick={onNewChat}
          aria-label="Start new conversation"
          id="new-chat-btn"
        >
          ✨ New Chat
        </button>
      </div>
    </header>
  );
}
