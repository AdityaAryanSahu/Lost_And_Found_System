// src/components/FilterBar.jsx
import React, { useState } from 'react';
import './FilterBar.css'; // Assume basic CSS for styling

// Placeholder list of item types (should ideally be fetched from API)
const ITEM_TYPES = ['Electronics', 'Clothing', 'Books', 'Keys', 'Others'];

const FilterBar = ({ onFilterChange }) => {
    const [query, setQuery] = useState('');
    const [itemType, setItemType] = useState('');
    const [isClaimed, setIsClaimed] = useState(false);
    const [dateFrom, setDateFrom] = useState('');

    const handleSearch = (e) => {
        e.preventDefault();
        
        // Construct the SearchRequest object
        const filters = {
            query: query || undefined,
            item_type: itemType || undefined,
            is_claimed: isClaimed,
            date_from: dateFrom || undefined,
            // Pagination defaults:
            limit: 20,
            offset: 0
        };

        // Pass the updated filters back to the ItemListingPage
        onFilterChange(filters);
    };

    return (
        <form className="filter-bar" onSubmit={handleSearch}>
            <h2>Filter Items</h2>
            
            {/* General Search Query */}
            <input
                type="text"
                placeholder="Search keywords (e.g., 'blue backpack')"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />

            {/* Item Type Filter */}
            <select value={itemType} onChange={(e) => setItemType(e.target.value)}>
                <option value="">All Types</option>
                {ITEM_TYPES.map(type => (
                    <option key={type} value={type}>{type}</option>
                ))}
            </select>

            {/* Date Filter (Simplified) */}
            <input
                type="date"
                title="Found/Lost Date After"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
            />

            {/* Status Filter */}
            <label>
                Show Claimed:
                <input
                    type="checkbox"
                    checked={isClaimed}
                    onChange={(e) => setIsClaimed(e.target.checked)}
                />
            </label>
            
            <button type="submit">Search & Filter</button>
        </form>
    );
};

export default FilterBar;