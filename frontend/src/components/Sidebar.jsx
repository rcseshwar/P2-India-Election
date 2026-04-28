/**
 * Sidebar with agent list and navigation.
 */
export default function Sidebar({ isOpen, agents, activeAgent, onSelectAgent, onNewChat }) {
  return (
    <aside
      className={`sidebar ${isOpen ? '' : 'collapsed'}`}
      role="complementary"
      aria-label="Agent navigation sidebar"
      id="sidebar"
    >
      <div className="sidebar-header">
        <button
          className="sidebar-new-chat"
          onClick={onNewChat}
          aria-label="Start a new conversation"
          id="sidebar-new-chat"
        >
          ✨ New Conversation
        </button>
      </div>

      <div className="sidebar-section-title">Specialist Agents</div>

      <nav className="sidebar-agents" aria-label="Available specialist agents">
        {agents.map((agent) => (
          <div
            key={agent.name}
            className={`agent-card ${activeAgent === agent.name ? 'active' : ''}`}
            onClick={() => onSelectAgent(agent)}
            onKeyDown={(e) => e.key === 'Enter' && onSelectAgent(agent)}
            role="button"
            tabIndex={0}
            aria-label={`${agent.title}: ${agent.description}`}
            aria-pressed={activeAgent === agent.name}
            id={`agent-${agent.name}`}
          >
            <div
              className="agent-card-icon"
              style={{ background: `${agent.color}20` }}
            >
              {agent.icon}
            </div>
            <div className="agent-card-info">
              <div className="agent-card-name">{agent.title}</div>
              <div className="agent-card-desc">{agent.description}</div>
            </div>
          </div>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-footer-text">
          Powered by Google ADK & Gemini
        </div>
        <div className="sidebar-tricolor" aria-hidden="true">
          <span style={{ background: '#FF9933' }} />
          <span style={{ background: '#FFFFFF' }} />
          <span style={{ background: '#138808' }} />
        </div>
      </div>
    </aside>
  );
}
