import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [summaryLength, setSummaryLength] = useState('medium');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleLengthChange = (e) => {
    setSummaryLength(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('length', summaryLength);

    setLoading(true); // Show spinner

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        params: {
          length: summaryLength,
        }
      });

      setSummary(response.data.summary);
    } catch (error) {
      console.error(error);
      alert("There was an error processing your file.");
    } finally {
      setLoading(false); // Hide spinner
    }
  };

  return (
    <div className="App">
      <h1>Document Summarizer</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="file">Choose a PDF or Image file:</label>
          <input type="file" id="file" onChange={handleFileChange} />
        </div>
        <div>
          <label htmlFor="length">Summary Length:</label>
          <select id="length" value={summaryLength} onChange={handleLengthChange}>
            <option value="short">Short</option>
            <option value="medium">Medium</option>
            <option value="long">Long</option>
          </select>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Uploading...' : 'Upload and Summarize'}
        </button>
      </form>

      {loading && <div className="spinner"></div>}

      {summary && (
        <div className="summary">
          <h3>Summary:</h3>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}

export default App;
