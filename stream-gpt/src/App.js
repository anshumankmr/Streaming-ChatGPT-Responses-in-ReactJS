import './App.css';
import React, { useState } from 'react';

async function createCompletions(prompt) {
  return fetch("http://localhost:5000/create-completions/gpt3", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ prompt })
  });
}

function App() {
  const [message, updateMessage] = useState("");
  const [inputValue, updateInputValue] = useState("");

  const handleClick = async () => {
    const response = await createCompletions(inputValue);
    if (!response.body) {
      console.error('No response body');
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    reader.read().then(function processText({ done, value }) {
      if (done) {
        console.log('Stream complete');
        return;
      }

      const chunk = decoder.decode(value);
      updateMessage(prevMessage => chunk.replace('data:' , ''));

      return reader.read().then(processText);
    }).catch(err => {
      console.error('Error reading stream', err);
    });
  };

  return (
    <div className="App">
      <h1>Simple ChatGPT Streaming Completions Demo</h1>
      <textarea value={message} readOnly />
      <button onClick={handleClick}>Call ChatGPT</button>
      <input value={inputValue} onChange={e => updateInputValue(e.target.value)} />
    </div>
  );
}

export default App;
