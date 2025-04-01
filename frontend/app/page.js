"use client";
import React, { useState, useEffect } from "react"; // Add useEffect import

export default function SearchPage() {
  const [query, setQuery] = useState(""); // Store search query
  const [results, setResults] = useState([]); // Store search results
  const [currentPage, setCurrentPage] = useState(1); // Current page
  const [totalPages, setTotalPages] = useState(0); // Total pages
  const [searched, setSearched] = useState(false); // Track if search has been performed
  const [loading, setLoading] = useState(false); // Track loading state

  const fetchResults = async (page = 1) => {
    setResults([]); // Clear results before fetching new ones
    window.scrollTo(0, 0); // Scroll to top

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/search?query=${encodeURIComponent(query)}&page=${page}`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data.results || []);
      setCurrentPage(data.page);
      setTotalPages(data.total_pages);

      // Update URL with current query and page
      const url = new URL(window.location);
      url.searchParams.set('q', query);
      url.searchParams.set('page', page);
      window.history.pushState({}, '', url);
    } catch (error) {
      console.error("Error fetching data:", error.message);
      alert("Failed to fetch search results. Please try again.");
      setResults([]);
    }
  };

  const handleSearch = async () => {
    if (!query.trim()) return; // Prevent search if query is empty

    setSearched(true); // Mark as searched
    setLoading(true); // Start loading indicator

    await fetchResults(1); // Fetch results for the first page

    setLoading(false); // End loading indicator
  };

  // Modify handlePageChange to use window.location.replace
  const handlePageChange = async (newPage) => {
    if (newPage > 0 && newPage <= totalPages) {
      setLoading(true);
      const url = new URL(window.location);
      url.searchParams.set('page', newPage);
      window.location.replace(url); // This will cause a full page refresh
    }
  };

  // Replace the existing useEffect with this updated version
  useEffect(() => {
    const handleInitialLoad = async () => {
      const url = new URL(window.location);
      const pageParam = url.searchParams.get('page');
      const queryParam = url.searchParams.get('q');

      if (queryParam) {
        setQuery(queryParam);
        setSearched(true);
        setLoading(true);
        
        try {
          const response = await fetch(
            `http://127.0.0.1:5000/search?query=${encodeURIComponent(queryParam)}&page=${pageParam || 1}`
          );

          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }

          const data = await response.json();
          setResults(data.results || []);
          setCurrentPage(parseInt(pageParam) || 1);
          setTotalPages(data.total_pages);
        } catch (error) {
          console.error("Error fetching data:", error.message);
          setResults([]);
        } finally {
          setLoading(false);
        }
      } else {
        // Clear everything if no query parameter exists
        setQuery("");
        setResults([]);
        setSearched(false);
        setCurrentPage(1);
        setTotalPages(0);
      }
    };

    // Add event listener for popstate (browser back/forward buttons)
    window.addEventListener('popstate', handleInitialLoad);
    handleInitialLoad();

    // Cleanup
    return () => {
      window.removeEventListener('popstate', handleInitialLoad);
    };
  }, []); // Empty dependency array since we want this to run only once on mount

  const renderPagination = () => {
    const visiblePages = 5; // Number of visible page links
    const pages = [];
    const startPage = Math.max(1, currentPage - Math.floor(visiblePages / 2));
    const endPage = Math.min(totalPages, startPage + visiblePages - 1);

    for (let i = startPage; i <= endPage; i++) {
      pages.push(
        <button
          key={i}
          onClick={() => handlePageChange(i)}
          style={{
            padding: "8px 12px",
            margin: "0 5px",
            backgroundColor: i === currentPage ? "#4285F4" : "#f1f1f1",
            color: i === currentPage ? "white" : "#000",
            border: "1px solid #ddd",
            borderRadius: "5px",
            cursor: "pointer",
            fontWeight: i === currentPage ? "bold" : "normal",
          }}
        >
          {i}
        </button>
      );
    }

    return (
      <div style={{ textAlign: "center", marginTop: "20px" }}>
        {currentPage > 1 && (
          <button
            onClick={() => handlePageChange(currentPage - 1)}
            style={{
              padding: "8px 12px",
              margin: "0 5px",
              backgroundColor: "#f1f1f1",
              color: "#000",
              border: "1px solid #ddd",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Previous
          </button>
        )}
        {pages}
        {currentPage < totalPages && (
          <button
            onClick={() => handlePageChange(currentPage + 1)}
            style={{
              padding: "8px 12px",
              margin: "0 5px",
              backgroundColor: "#f1f1f1",
              color: "#000",
              border: "1px solid #ddd",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Next
          </button>
        )}
      </div>
    );
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
          placeholder="Search the web"
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
              <div
                className="search-result-card"
                key={index}
                style={{
                  marginBottom: "20px",
                  border: "1px solid #ddd",
                  borderRadius: "8px", // Slightly rounded corners
                  padding: "20px", // Increased padding
                  backgroundColor: "#FFFFFF", // Light white background
                  boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)", // Subtle shadow
                  transition: "transform 0.3s, box-shadow 0.3s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "scale(1.03)";
                  e.currentTarget.style.boxShadow =
                    "0 6px 12px rgba(0, 0, 0, 0.2)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "scale(1)";
                  e.currentTarget.style.boxShadow =
                    "0 4px 8px rgba(0, 0, 0, 0.1)";
                }}
              >
                <h3
                  className="result-title"
                  style={{
                    margin: "10px 0",
                    fontSize: "18px",
                    fontWeight: "600",
                    color: "#333",
                  }}
                >
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      textDecoration: "none",
                      color: "#4285F4", // Title color
                    }}
                  >
                    {item.title}
                  </a>
                </h3>
                <p
                  className="result-snippet"
                  style={{
                    color: "#555",
                    margin: "10px 0",
                    fontSize: "14px",
                    lineHeight: "1.5",
                  }}
                >
                  {item.snippet}
                </p>
                <p
                  className="result-url"
                  style={{
                    color: "#007BFF",
                    fontSize: "14px",
                    marginTop: "10px",
                    textDecoration: "underline",
                  }}
                >
                  <a href={item.url} target="_blank" rel="noopener noreferrer">
                    {item.url}
                  </a>
                </p>
              </div>
            ))}

            {/* Pagination */}
            {renderPagination()}
          </div>
        )}
      </div>
    </div>
  );
}
