import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ChatInterface from './components/ChatInterface';
import './App.css';

const API_BASE_URL = 'http://localhost:8000/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (userMessage) => {
    if (!userMessage.trim()) return;

    // Add user message to chat
    const newMessage = {
      id: Date.now(),
      text: userMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, newMessage]);
    setLoading(true);
    setError(null);

    try {
      // Send to backend API
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message: userMessage,
        conversation_history: messages.map(msg => ({
          role: msg.sender === 'user' ? 'user' : 'assistant',
          content: msg.text
        }))
      });

      // Add bot response to chat
      const botMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get response from the AI. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-dark-bg to-dark-card">
      <header className="bg-gradient-to-r from-accent-blue to-blue-600 text-white p-4 shadow-lg">
        <h1 className="text-2xl font-bold">AI Chatbot</h1>
        <p className="text-blue-100 text-sm">Powered by Foundation Model API</p>
      </header>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-gray-300 mb-2">Welcome to AI Chatbot</h2>
              <p className="text-gray-400">Start a conversation by typing a message below.</p>
            </div>
          </div>
        )}

        {messages.map(message => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-md px-4 py-2 rounded-lg ${
                message.sender === 'user'
                  ? 'bg-accent-blue text-white rounded-br-none'
                  : 'bg-dark-card text-gray-200 rounded-bl-none border border-dark-border'
              }`}
            >
              <p className="break-words">{message.text}</p>
              <span className="text-xs opacity-70 mt-1 block">{message.timestamp}</span>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-dark-card text-gray-200 px-4 py-2 rounded-lg border border-dark-border rounded-bl-none">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="bg-red-900 bg-opacity-30 border border-red-600 text-red-200 px-4 py-2 rounded">
            {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <ChatInterface onSendMessage={sendMessage} isSending={loading} onClear={clearChat} />
    </div>
  );
}

export default App;
