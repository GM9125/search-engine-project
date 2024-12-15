"use client";
import React, { useState } from "react";

export default function SearchPage() {
  const [query, setQuery] = useState(""); // Store search query
  const [results, setResults] = useState([]); // Store search results
  const [searched, setSearched] = useState(false); // Track if search has been performed
  const [loading, setLoading] = useState(false); // Track loading state

  const handleSearch = async () => {
    if (!query.trim()) return; // Prevent search if query is empty

    setSearched(true); // Mark as searched
    setLoading(true); // Start loading indicator

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/search?query=${encodeURIComponent(query)}`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data.results || []); // Set results or empty array if no results
    } catch (error) {
      console.error("Error fetching data:", error.message);
      alert("Failed to fetch search results. Please try again.");
      setResults([]); // Reset results if error occurs
    } finally {
      setLoading(false); // End loading indicator
    }
  };

  return (
    <div className="search-container">
      {/* Logo */}
      <h1 className="logo">
        <span className="blue">S</span>
        <span className="red">e</span>
        <span className="yellow">a</span>
        <span className="blue">r</span>
        <span className="green">c</span>
        <span className="red">h</span>
        <span className="blue">I</span>
        <span className="red">T</span>
      </h1>

      {/* Search Bar */}
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        />
        <span className="search-icon" onClick={handleSearch}></span>
      </div>

      {/* Results Section */}
      <div className="results-container">
        {loading && <p className="loading">Loading...</p>}
        {searched && !loading && results.length === 0 && (
          <p className="no-results">No results found. Try another query.</p>
        )}

        {results.length > 0 && (
          <div className="search-results">
            {results.map((item, index) => (
              <div className="search-result" key={index}>
                <h3 className="result-title">
                  <a href={item.url} target="_blank" rel="noopener noreferrer">
                    {item.title}
                  </a>
                </h3>
                <p className="result-url">{item.url}</p>
                <p className="result-snippet">{item.snippet}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}