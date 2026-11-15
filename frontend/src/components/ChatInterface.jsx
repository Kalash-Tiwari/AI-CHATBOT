import React, { useRef, useState, useEffect } from 'react';

const ChatInterface = ({
  onSendMessage,
  isSending,
  onClear,
  onStop,
  onAttachFile,
  attachments,
  disabled,
  webSearch,
  setWebSearch,
  responseMode,
  setResponseMode,
  suggestedPrompts
}) => {
  const [inputValue, setInputValue] = useState('');
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 180)}px`;
    }
  }, [inputValue]);

  const handleSend = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech recognition is not supported in this browser.');
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInputValue((prev) => `${prev}${prev ? ' ' : ''}${transcript}`);
    };
    recognition.start();
  };

  return (
    <div className="composer-panel">
      <div className="composer-controls">
        <label className="toggle-pill">
          <input type="checkbox" checked={webSearch} onChange={() => setWebSearch((prev) => !prev)} />
          <span>Web research</span>
        </label>

        <select value={responseMode} onChange={(event) => setResponseMode(event.target.value)}>
          <option value="concise">Concise</option>
          <option value="balanced">Balanced</option>
          <option value="detailed">Detailed</option>
        </select>

        <button type="button" className="ghost-button" onClick={() => fileInputRef.current?.click()}>
          Attach file
        </button>

        <input
          ref={fileInputRef}
          type="file"
          hidden
          multiple
          onChange={onAttachFile}
          aria-label="Attach a file"
        />
      </div>

      {attachments.length > 0 && (
        <div className="attachment-list">
          {attachments.map((attachment) => (
            <span key={attachment}>{attachment}</span>
          ))}
        </div>
      )}

      <div className="composer-box">
        <textarea
          ref={textareaRef}
          value={inputValue}
          onChange={(event) => setInputValue(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask Nexus AI anything..."
          rows={1}
          disabled={isSending || disabled}
        />

        <div className="composer-actions">
          <button type="button" className="secondary-button" onClick={handleVoiceInput}>
            Voice
          </button>
          {isSending ? (
            <button type="button" className="primary-button" onClick={onStop}>
              Stop
            </button>
          ) : (
            <button type="button" className="primary-button" onClick={handleSend} disabled={!inputValue.trim() || disabled}>
              Send
            </button>
          )}
          <button type="button" className="danger-button" onClick={onClear}>
            Clear
          </button>
        </div>
      </div>

      <div className="prompt-row">
        {suggestedPrompts.map((prompt) => (
          <button key={prompt} type="button" className="prompt-pill" onClick={() => setInputValue(prompt)}>
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ChatInterface;
