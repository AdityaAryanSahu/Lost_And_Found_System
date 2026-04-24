import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { findMatches } from '../api/matchService';
import './ItemListing.css'; // Reusing your existing card styles if possible!

const MatchPage = () => {
  const navigate = useNavigate();
  const [searchType, setSearchType] = useState('');
  const [keywords, setKeywords] = useState('');
  const [location, setLocation] = useState('');
  
  const [matches, setMatches] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleMatchSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setHasSearched(true);

    // Convert comma-separated string into an array of words
    const keywordArray = keywords
      .split(',')
      .map(word => word.trim())
      .filter(word => word.length > 0);

    try {
      const response = await findMatches({
        search_type: searchType,
        keywords: keywordArray,
        location: location
      });
      
      // Your backend returns a MatchList with a .matches array
      setMatches(response.data.matches || []);
    } catch (err) {
      console.error("Match engine failed:", err);
      setError(err.response?.data?.detail || "Failed to find matches.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="match-page-container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      <header style={{ marginBottom: '30px' }}>
        <h1>Find Potential Matches</h1>
        <p style={{ color: '#aaa' }}>Lost something? Describe it below and our matching engine will scan all found items to find the highest probability matches.</p>
      </header>

      {/* 1. THE SEARCH FORM */}
      <div style={{ background: '#1f1f1f', padding: '25px', borderRadius: '10px', marginBottom: '40px' }}>
        <form onSubmit={handleMatchSearch} style={{ display: 'grid', gap: '15px', gridTemplateColumns: '1fr 1fr 1fr auto', alignItems: 'end' }}>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
            <label>Item Type</label>
            <input 
              type="text" 
              placeholder="e.g. Electronics, Books" 
              value={searchType} 
              onChange={(e) => setSearchType(e.target.value)}
              required
              style={{ padding: '10px', borderRadius: '5px', border: '1px solid #444', background: '#333', color: '#fff' }}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
            <label>Keywords (comma separated)</label>
            <input 
              type="text" 
              placeholder="e.g. black, apple, iphone" 
              value={keywords} 
              onChange={(e) => setKeywords(e.target.value)}
              required
              style={{ padding: '10px', borderRadius: '5px', border: '1px solid #444', background: '#333', color: '#fff' }}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
            <label>Location Lost</label>
            <input 
              type="text" 
              placeholder="e.g. Library, Cafeteria" 
              value={location} 
              onChange={(e) => setLocation(e.target.value)}
              required
              style={{ padding: '10px', borderRadius: '5px', border: '1px solid #444', background: '#333', color: '#fff' }}
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            style={{ padding: '12px 20px', background: '#d4af37', color: '#000', fontWeight: 'bold', border: 'none', borderRadius: '5px', cursor: 'pointer', height: '42px' }}
          >
            {loading ? 'Scanning...' : 'Find Matches'}
          </button>
        </form>
      </div>

      {/* 2. ERROR STATE */}
      {error && <div style={{ color: '#ff4c4c', marginBottom: '20px' }}>{error}</div>}

      {/* 3. THE RESULTS GRID */}
      {hasSearched && !loading && (
        <div>
          <h2 style={{ marginBottom: '20px' }}>Results ({matches.length} found)</h2>
          
          {matches.length === 0 ? (
            <p style={{ color: '#aaa' }}>No highly probable matches found. Try broadening your keywords!</p>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
              
              {matches.map((match) => {
                const item = match.matched_item;
                const scorePercentage = Math.round(match.score * 100);
                
                return (
                  <div 
                    key={item.item_id} 
                    onClick={() => navigate(`/items/${item.item_id}`)}
                    style={{ background: '#2a2a2a', border: '1px solid #444', borderRadius: '8px', overflow: 'hidden', cursor: 'pointer', transition: 'transform 0.2s' }}
                  >
                    {/* Match Score Badge */}
                    <div style={{ background: scorePercentage > 75 ? '#4CAF50' : '#FF9800', color: '#fff', padding: '5px 10px', fontWeight: 'bold', textAlign: 'center' }}>
                      {scorePercentage}% Match
                    </div>

                    <div style={{ height: '200px', background: '#111', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      {item.img?.[0]?.url ? (
                        <img src={item.img[0].url} alt={item.desc} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                      ) : (
                        <span style={{ fontSize: '40px' }}>📷</span>
                      )}
                    </div>

                    <div style={{ padding: '15px' }}>
                      <h3 style={{ margin: '0 0 10px 0', color: '#d4af37' }}>{item.type}</h3>
                      <p style={{ margin: '0 0 10px 0', color: '#ccc', fontSize: '14px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {item.desc}
                      </p>
                      
                      {/* Reason from your backend */}
                      <p style={{ margin: 0, fontSize: '12px', color: '#888', fontStyle: 'italic' }}>
                        {match.mssg.split('Reasons: ')[1]}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default MatchPage;