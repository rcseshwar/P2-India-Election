import { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import WelcomeScreen from './components/WelcomeScreen';
import { sendMessage, createSession } from './services/api';
import './App.css';

const AGENTS = [
  { name: 'election_system_agent', title: 'Election System', icon: '📊', description: "India's multi-level election system", color: '#FF9933' },
  { name: 'parliament_guide_agent', title: 'Parliament Guide', icon: '🏛️', description: 'Lok Sabha vs Rajya Sabha', color: '#4A90D9' },
  { name: 'voter_registration_agent', title: 'Voter Registration', icon: '📝', description: 'Register, update, check status', color: '#138808' },
  { name: 'candidate_info_agent', title: 'Candidate Research', icon: '🔍', description: 'Background & disclosures', color: '#E74C3C' },
  { name: 'language_assist_agent', title: 'Language Help', icon: '🗣️', description: 'Simple explanations', color: '#9B59B6' },
  { name: 'voting_day_agent', title: 'Voting Day', icon: '📅', description: 'Polling booth guide', color: '#F39C12' },
];

function App() {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeAgent, setActiveAgent] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    initSession();
  }, []);

  async function initSession() {
    try {
      const session = await createSession();
      setSessionId(session.session_id);
    } catch (err) {
      console.warn('Backend not available, using local session');
      setSessionId(`local-${Date.now()}`);
    }
  }

  async function handleSendMessage(text) {
    if (!text.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendMessage(text, sessionId);
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        agent: response.agent_name,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
      setSessionId(response.session_id);
      if (response.agent_name) {
        setActiveAgent(response.agent_name);
      }
    } catch (err) {
      setError('Unable to reach the server. Please try again.');
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '🗳️ I apologize, but I\'m having trouble connecting to the server. Please make sure the backend is running and try again.',
        agent: 'system',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }

  function handleQuickAction(question) {
    handleSendMessage(question);
  }

  function handleNewChat() {
    setMessages([]);
    setActiveAgent(null);
    setError(null);
    initSession();
  }

  const showWelcome = messages.length === 0;

  return (
    <div className="app" role="application" aria-label="Chunav Mitra - India Election Education Assistant">
      <Header
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        onNewChat={handleNewChat}
        activeAgent={activeAgent}
        agents={AGENTS}
      />
      <div className="app-body">
        <Sidebar
          isOpen={sidebarOpen}
          agents={AGENTS}
          activeAgent={activeAgent}
          onSelectAgent={(agent) => handleSendMessage(`Tell me about ${agent.title}`)}
          onNewChat={handleNewChat}
        />
        <main className="main-content" id="main-content" role="main">
          {showWelcome ? (
            <WelcomeScreen
              agents={AGENTS}
              onQuickAction={handleQuickAction}
            />
          ) : (
            <ChatInterface
              messages={messages}
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
              agents={AGENTS}
              error={error}
            />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
