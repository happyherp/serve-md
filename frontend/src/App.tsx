import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, useNavigate, useParams } from 'react-router-dom'
import { DirectoryView } from './components/DirectoryView'
import { ContentView } from './components/ContentView'
import { SearchView } from './components/SearchView'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>serve-md</h1>
          <SearchBar />
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<DirectoryView path="." />} />
            <Route path="/directory/*" element={<DirectoryViewRoute />} />
            <Route path="/content/*" element={<ContentViewRoute />} />
            <Route path="/search" element={<SearchView />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function SearchBar() {
  const [query, setQuery] = useState('')
  const navigate = useNavigate()

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query)}`)
    }
  }

  return (
    <form onSubmit={handleSearch} className="search-form">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
        className="search-input"
      />
      <button type="submit" className="search-button">Search</button>
    </form>
  )
}

function DirectoryViewRoute() {
  const params = useParams()
  const path = params['*'] || '.'
  return <DirectoryView path={path} />
}

function ContentViewRoute() {
  const params = useParams()
  const path = params['*'] || 'README.md'
  return <ContentView path={path} />
}

export default App