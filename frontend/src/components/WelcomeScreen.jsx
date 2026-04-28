/**
 * Welcome screen with hero section, agent cards, and quick actions.
 */

const QUICK_QUESTIONS = [
  "How does India's election system work?",
  "What is the difference between Lok Sabha and Rajya Sabha?",
  "How do I register to vote?",
  "How can I check my candidate's criminal record?",
  "Explain the EVM in simple terms",
  "What should I carry on voting day?",
  "What is NOTA?",
  "How are election results counted?",
];

export default function WelcomeScreen({ agents, onQuickAction }) {
  return (
    <div className="welcome" id="welcome-screen">
      <div className="welcome-hero">
        <div className="welcome-icon" role="img" aria-label="Ballot box emoji">🗳️</div>
        <h1 className="welcome-title">🇮🇳 Election Buddy 🇮🇳</h1>
        <p className="hero-subtitle">Empowering every citizen with knowledge of Indian democracy.</p>
        <div className="hero-divider"></div>
        <p className="hero-description">
          Your expert AI assistant for everything related to India's election process. 
          From registration to polling day, we've got you covered 🇮🇳.
        </p>
      </div>

      <div className="welcome-agents" role="list" aria-label="Available specialist agents">
        {agents.map((agent) => (
          <div
            key={agent.name}
            className="welcome-agent-card"
            onClick={() => onQuickAction(`Tell me about ${agent.title.toLowerCase()}`)}
            onKeyDown={(e) => e.key === 'Enter' && onQuickAction(`Tell me about ${agent.title.toLowerCase()}`)}
            role="listitem"
            tabIndex={0}
            aria-label={`${agent.title}: ${agent.description}`}
            id={`welcome-${agent.name}`}
          >
            <div className="welcome-agent-icon">{agent.icon}</div>
            <div className="welcome-agent-name">{agent.title}</div>
            <div className="welcome-agent-desc">{agent.description}</div>
          </div>
        ))}
      </div>

      <div className="welcome-quick-actions" role="list" aria-label="Suggested questions">
        {QUICK_QUESTIONS.map((q, i) => (
          <button
            key={i}
            className="quick-action-btn"
            onClick={() => onQuickAction(q)}
            role="listitem"
            id={`quick-action-${i}`}
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
