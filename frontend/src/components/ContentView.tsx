import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { MarkdownContent } from '../types'
import { apiService } from '../services/api'

interface ContentViewProps {
  path: string
}

export function ContentView({ path }: ContentViewProps) {
  const [content, setContent] = useState<MarkdownContent | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const fetchContent = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await apiService.getContent(path)
        setContent(data)
      } catch (err) {
        setError(err as Error)
        setContent(null)
      } finally {
        setLoading(false)
      }
    }

    fetchContent()
  }, [path])

  if (loading) {
    return <div className="loading">Loading content...</div>
  }

  if (error) {
    return <div className="error">Error loading content: {error.message}</div>
  }

  if (!content) {
    return <div className="error">Content not found</div>
  }

  return (
    <div className="content-view">
      <div className="content-header">
        <h1 className="content-title">{content.title}</h1>
        <div className="content-meta">
          <Breadcrumb path={path} />
          {content.frontmatter.date && (
            <span> • {content.frontmatter.date}</span>
          )}
          {content.frontmatter.author && (
            <span> • by {content.frontmatter.author}</span>
          )}
        </div>
      </div>
      
      <div 
        className="content-body markdown-content"
        dangerouslySetInnerHTML={{ __html: content.html_content }}
      />
    </div>
  )
}

function Breadcrumb({ path }: { path: string }) {
  const parts = path.split('/').filter(Boolean)
  const dirParts = parts.slice(0, -1)
  const fileName = parts[parts.length - 1]
  
  return (
    <div>
      <Link to="/">Home</Link>
      {dirParts.map((part, index) => {
        const currentPath = dirParts.slice(0, index + 1).join('/')
        return (
          <span key={index}>
            {' / '}
            <Link to={`/directory/${currentPath}`}>{part}</Link>
          </span>
        )
      })}
      {fileName && <span> / {fileName}</span>}
    </div>
  )
}