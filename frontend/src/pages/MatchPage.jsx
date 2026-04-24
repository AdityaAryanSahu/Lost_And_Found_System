import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { findMatches } from '../api/matchService';
import './MatchPage.css'; 

const MatchPage = () => {
  const navigate = useNavigate();
  
  const [postType, setPostType] = useState('LOST'); 
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

    const keywordArray = keywords
      .split(',')
      .map(word => word.trim())
      .filter(word => word.length > 0);

    try {
      const response = await findMatches({
        search_type: searchType,
        keywords: keywordArray,
        location: location,
        post_type: postType 
      });
      
      setMatches(response.data.matches || []);
    } catch (err) {
      console.error("Match engine failed:", err);
      setError(err.response?.data?.detail || "Failed to find matches.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="match-page">
      {/* HEADER: Matches your Item Detail and Upload headers */}
      <header className="match-header">
        <button onClick={() => navigate(-1)} className="back-btn" style={{ background: 'transparent', border: '1px solid #D4AF37', color: '#D4AF37', padding: '10px 20px', borderRadius: '8px', cursor: 'pointer' }}>
          ← Back
        </button>
        <h1>Smart Matching Engine</h1>
      </header>

      <div className="match-container">
        <div className="match-intro">
          <p>Describe the item below and our AI will scan the database for the highest probability matches.</p>
        </div>

        {/* THE SEARCH FORM */}
        <div className="match-form-card">
          <form onSubmit={handleMatchSearch}>
            
            <div className="match-radio-group">
              <label className="match-radio-label">
                <input 
                  type="radio" 
                  value="LOST" 
                  checked={postType === 'LOST'} 
                  onChange={(e) => setPostType(e.target.value)}
                />
                I am looking for an item I LOST
              </label>
              <label className="match-radio-label">
                <input 
                  type="radio" 
                  value="FOUND" 
                  checked={postType === 'FOUND'} 
                  onChange={(e) => setPostType(e.target.value)}
                />
                I am looking for the owner of an item I FOUND
              </label>
            </div>

            <div className="match-inputs-grid">
              <div className="match-input-group">
                <label>Item Category</label>
                <input 
                  type="text" 
                  placeholder="e.g. Electronics, Books" 
                  value={searchType} 
                  onChange={(e) => setSearchType(e.target.value)}
                  required
                />
              </div>

              <div className="match-input-group">
                <label>Keywords (comma separated)</label>
                <input 
                  type="text" 
                  placeholder="e.g. black, apple, iphone" 
                  value={keywords} 
                  onChange={(e) => setKeywords(e.target.value)}
                  required
                />
              </div>

              <div className="match-input-group">
                <label>Location</label>
                <input 
                  type="text" 
                  placeholder="e.g. Library, Cafeteria" 
                  value={location} 
                  onChange={(e) => setLocation(e.target.value)}
                  required
                />
              </div>

              <button 
                type="submit" 
                className="match-submit-btn"
                disabled={loading}
              >
                {loading ? 'Scanning...' : 'Find Matches'}
              </button>
            </div>
          </form>
        </div>

        {/* ERROR STATE */}
        {error && <div style={{ color: '#ff4c4c', textAlign: 'center', marginBottom: '20px' }}>{error}</div>}

        {/* THE RESULTS GRID */}
        {hasSearched && !loading && (
          <div>
            <h2 style={{ color: '#D4AF37', marginBottom: '20px', borderBottom: '1px solid rgba(212, 175, 55, 0.2)', paddingBottom: '10px' }}>
              Results ({matches.length} found)
            </h2>
            
            {matches.length === 0 ? (
              <p style={{ color: '#999', textAlign: 'center', padding: '40px', background: 'rgba(255,255,255,0.02)', borderRadius: '8px', border: '1px dashed #444' }}>
                No highly probable matches found. Try broadening your keywords!
              </p>
            ) : (
              <div className="match-results-grid">
                {matches.map((match) => {
                  const item = match.matched_item;
                  const scorePercentage = Math.round(match.score * 100);
                  
                  return (
                    <div 
                      key={item.item_id} 
                      className="match-card"
                      onClick={() => navigate(`/items/${item.item_id}`)}
                    >
                      <div className={`match-score-banner ${scorePercentage > 75 ? 'match-score-high' : ''}`}>
                        {scorePercentage}% MATCH
                      </div>

                      <div className="match-image-container">
                        {item.img?.[0]?.url ? (
                          <img src={item.img[0].url} alt={item.desc} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                        ) : (
                          <span style={{ fontSize: '40px', color: '#666' }}>📷</span>
                        )}
                      </div>

                      <div className="match-info">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                          <h3 style={{ margin: '0', color: '#D4AF37', fontSize: '16px', textTransform: 'uppercase' }}>{item.type}</h3>
                          <span style={{ 
                            fontSize: '11px', 
                            background: item.post_type === 'LOST' ? 'rgba(220, 53, 69, 0.2)' : 'rgba(76, 175, 80, 0.2)', 
                            color: item.post_type === 'LOST' ? '#ff6b6b' : '#81c784', 
                            padding: '4px 8px', 
                            borderRadius: '4px',
                            fontWeight: 'bold'
                          }}>
                            {item.post_type}
                          </span>
                        </div>
                        
                        <p style={{ margin: '0 0 15px 0', color: '#CCC', fontSize: '14px', lineHeight: '1.4' }}>
                          {item.desc}
                        </p>
                        
                        <p style={{ margin: 0, fontSize: '12px', color: '#888', fontStyle: 'italic', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '10px' }}>
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
    </div>
  );
};

export default MatchPage;