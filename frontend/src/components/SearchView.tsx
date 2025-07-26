import { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { SearchResult } from '../types'
import { apiService } from '../services/api'

export function SearchView() {
  const [searchParams] = useSearchParams()
  const query = searchParams.get('q') || ''
  
  const [results, setResults] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    if (!query.trim()) {
      setResults([])
      return
    }

    const performSearch = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await apiService.search(query)
        setResults(data)
      } catch (err) {
        setError(err as Error)
        setResults([])
      } finally {
        setLoading(false)
      }
    }

    performSearch()
  }, [query])

  if (!query.trim()) {
    return (
      <div className="search-results">
        <div className="search-header">
          <h1>Search</h1>
          <p>Enter a search query to find content.</p>
        </div>
      </div>
    )
  }

  if (loading) {
    return <div className="loading">Searching...</div>
  }

  if (error) {
    return <div className="error">Error searching: {error.message}</div>
  }

  return (
    <div className="search-results">
      <div className="search-header">
        <h1>Search Results</h1>
        <p>
          Found {results.length} result{results.length !== 1 ? 's' : ''} for "{query}"
        </p>
      </div>
      
      {results.length === 0 ? (
        <div className="error">No results found for "{query}"</div>
      ) : (
        <div>
          {results.map((result, index) => (
            <SearchResultItem key={index} result={result} />
          ))}
        </div>
      )}
    </div>
  )
}

function SearchResultItem({ result }: { result: SearchResult }) {
  return (
    <Link to={`/content/${result.path}`} className="search-result">
      <div className="search-result-title">{result.title}</div>
      <div className="search-result-path">{result.path}</div>
      <div className="search-result-excerpt">{result.excerpt}</div>
    </Link>
  )
}