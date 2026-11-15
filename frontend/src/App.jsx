import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ChatInterface from './components/ChatInterface.jsx';
import './App.css';

const API_BASE_URL = 'http://localhost:8000/api';
const SUGGESTED_PROMPTS = [
  'Explain machine learning in simple terms',
  'Write a Python function for API validation',
  'Compare Python and Java for backend work',
  'What are the latest AI developments in 2026?',
  'Summarize database normalization'
];

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [provider, setProvider] = useState('gemini');
  const [configStatus, setConfigStatus] = useState(null);
  const [webSearch, setWebSearch] = useState(false);
  const [responseMode, setResponseMode] = useState('balanced');
  const [attachments, setAttachments] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const abortControllerRef = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const buildConversationHistory = (history) =>
    history.map((msg) => ({
      role: msg.sender === 'user' ? 'user' : 'assistant',
      content: msg.text
    }));

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const fetchConfigStatus = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/status`);
        setConfigStatus(response.data);
        if (response.data.active_provider && response.data.active_provider !== 'mock') {
          setProvider(response.data.active_provider);
        }
      } catch (err) {
        setConfigStatus({
          status: 'unknown',
          message: 'Unable to verify backend provider configuration.'
        });
      }
    };

    fetchConfigStatus();
  }, []);

  const stopGeneration = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setLoading(false);
    setError('Generation stopped by the user.');
  };

  const sendMessage = async (userMessage) => {
    const trimmedMessage = userMessage.trim();
    if (!trimmedMessage) return;

    const userMessageEntry = {
      id: Date.now(),
      text: trimmedMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    const nextMessages = [...messages, userMessageEntry];
    setMessages(nextMessages);
    setLoading(true);
    setError(null);

    const requestBody = {
      message: trimmedMessage,
      provider,
      web_search: webSearch,
      response_mode: responseMode,
      conversation_history: buildConversationHistory(nextMessages)
    };

    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, requestBody, {
        signal: controller.signal
      });

      const assistantMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString(),
        sources: response.data.sources || []
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      if (err.name === 'CanceledError' || err.code === 'ERR_CANCELED') {
        return;
      }

      const backendDetail = err.response?.data?.detail;
      const missingKeyError = backendDetail && backendDetail.includes('not set in environment variables');
      if (missingKeyError) {
        setError(
          'No valid LLM API key is configured. Please add GEMINI_API_KEY or OPENAI_API_KEY in the root .env file and restart the backend.'
        );
      } else {
        setError(backendDetail || 'Failed to get a response from the AI. Please try again.');
      }
      console.error('Error:', err);
    } finally {
      setLoading(false);
      abortControllerRef.current = null;
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
    setAttachments([]);
  };

  const handleAttachment = (event) => {
    const files = Array.from(event.target.files || []);
    setAttachments(files.map((file) => file.name));
  };

  const copyMessage = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      setError('Response copied to clipboard.');
    } catch (err) {
      setError('Unable to copy the response.');
    }
  };

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <div>
            <p className="eyebrow">Workspace</p>
            <h2>Nexus AI</h2>
          </div>
          <button type="button" className="ghost-button" onClick={() => setSidebarOpen((prev) => !prev)}>
            {sidebarOpen ? 'Hide' : 'Show'}
          </button>
        </div>

        <button type="button" className="primary-button sidebar-action" onClick={clearChat}>
          + New chat
        </button>

        <div className="sidebar-search">
          <input type="text" placeholder="Search chats" aria-label="Search chats" />
        </div>

        <div className="sidebar-section">
          <p className="section-label">Quick actions</p>
          <ul className="history-list">
            {SUGGESTED_PROMPTS.slice(0, 4).map((prompt) => (
              <li key={prompt}>
                <button type="button" onClick={() => sendMessage(prompt)}>
                  {prompt}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </aside>

      <main className="chat-panel">
        <header className="topbar">
          <div className="brand-block">
            <div className="brand-mark">N</div>
            <div>
              <h1>Nexus AI</h1>
              <p>Intelligent assistant</p>
            </div>
          </div>

          <div className="header-controls">
            <label htmlFor="provider" className="control-label">Model</label>
            <select id="provider" value={provider} onChange={(event) => setProvider(event.target.value)}>
              <option value="gemini">Gemini</option>
              <option value="openai">GPT-4.1</option>
            </select>
          </div>
        </header>

        {configStatus && configStatus.status !== 'ready' && (
          <div className="status-banner warning">
            <strong>Provider status:</strong>
            <span>
              {configStatus.status === 'mock'
                ? 'No valid API key is configured yet. Mock mode is active.'
                : configStatus.message}
            </span>
          </div>
        )}

        <div className="conversation-container">
          {messages.length === 0 ? (
            <div className="welcome-panel">
              <p className="eyebrow">Ready to help</p>
              <h2>Ask anything. Research anything. Build faster.</h2>
              <div className="prompt-grid">
                {SUGGESTED_PROMPTS.map((prompt) => (
                  <button key={prompt} type="button" className="prompt-chip" onClick={() => sendMessage(prompt)}>
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="message-list">
              {messages.map((message) => (
                <div key={message.id} className={`message-row ${message.sender === 'user' ? 'outgoing' : 'incoming'}`}>
                  <div className="message-bubble">
                    <p>{message.text}</p>
                    <div className="message-meta">
                      <span>{message.timestamp}</span>
                      {message.sender === 'assistant' && (
                        <div className="toolbar">
                          <button type="button" onClick={() => copyMessage(message.text)}>Copy</button>
                          <button type="button" onClick={() => sendMessage(`Explain this in simpler terms: ${message.text}`)}>Simplify</button>
                        </div>
                      )}
                    </div>
                    {message.sources && message.sources.length > 0 && (
                      <div className="source-list">
                        {message.sources.map((source) => (
                          <a key={`${source.url}-${source.title}`} href={source.url} target="_blank" rel="noreferrer">
                            {source.title}
                          </a>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="message-row incoming">
                  <div className="message-bubble typing-bubble">
                    <span /><span /><span />
                  </div>
                </div>
              )}
            </div>
          )}

          {error && <div className="status-banner error">{error}</div>}
          <div ref={messagesEndRef} />
        </div>

        <ChatInterface
          onSendMessage={sendMessage}
          isSending={loading}
          onClear={clearChat}
          onStop={stopGeneration}
          onAttachFile={handleAttachment}
          attachments={attachments}
          disabled={configStatus?.status === 'unknown'}
          webSearch={webSearch}
          setWebSearch={setWebSearch}
          responseMode={responseMode}
          setResponseMode={setResponseMode}
          suggestedPrompts={SUGGESTED_PROMPTS}
        />
      </main>
    </div>
  );
}

export default App;
