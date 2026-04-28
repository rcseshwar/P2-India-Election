/**
 * API service for communicating with Election Buddy 🇮🇳 backend.
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

/**
 * Send a chat message and get a response.
 */
export async function sendMessage(message, sessionId = null, userId = 'anonymous') {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      user_id: userId,
      language: 'en',
    }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

/**
 * Send a chat message and stream the response via SSE.
 */
export async function streamMessage(message, sessionId, userId, onChunk, onDone, onError) {
  try {
    const response = await fetch(`${API_URL}/api/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        session_id: sessionId,
        user_id: userId,
        language: 'en',
      }),
    });

    if (!response.ok) throw new Error(`API error: ${response.status}`);

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.type === 'chunk') {
              onChunk(data.content, data.agent);
            } else if (data.type === 'session') {
              sessionId = data.session_id;
            } else if (data.type === 'done') {
              onDone(sessionId);
            } else if (data.type === 'error') {
              onError(data.message);
            }
          } catch (e) {
            // Skip invalid JSON lines
          }
        }
      }
    }
  } catch (error) {
    onError(error.message);
  }
}

/**
 * Create a new chat session.
 */
export async function createSession(userId = 'anonymous') {
  const response = await fetch(`${API_URL}/api/session?user_id=${userId}`, {
    method: 'POST',
  });
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}

/**
 * Get chat history for a session.
 */
export async function getHistory(sessionId) {
  const response = await fetch(`${API_URL}/api/history/${sessionId}`);
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}

/**
 * Get list of available agents.
 */
export async function getAgents() {
  const response = await fetch(`${API_URL}/api/agents`);
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}

/**
 * Submit feedback on a response.
 */
export async function submitFeedback(sessionId, messageId, rating, comment = '') {
  const response = await fetch(`${API_URL}/api/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message_id: messageId, rating, comment }),
  });
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}

/**
 * Health check.
 */
export async function healthCheck() {
  const response = await fetch(`${API_URL}/health`);
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}
