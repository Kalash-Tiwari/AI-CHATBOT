import React, { useState } from 'react';

const ChatInterface = ({ onSendMessage, isSending, onClear }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="bg-dark-card border-t border-dark-border p-4 shadow-lg">
      <div className="flex gap-3 mb-3">
        <button
          onClick={onClear}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded transition-colors"
        >
          Clear Chat
        </button>
      </div>

      <div className="flex gap-2">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here... (Shift+Enter for new line)"
          disabled={isSending}
          rows="3"
          className="flex-1 bg-gray-800 text-white border border-dark-border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-accent-blue resize-none disabled:opacity-50"
        />
        <button
          onClick={handleSend}
          disabled={isSending || !inputValue.trim()}
          className="bg-accent-blue hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors disabled:bg-gray-600 disabled:cursor-not-allowed self-end h-fit"
        >
          {isSending ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
