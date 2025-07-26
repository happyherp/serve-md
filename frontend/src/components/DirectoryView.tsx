import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { DirectoryInfo, FileInfo } from '../types'
import { apiService } from '../services/api'

interface DirectoryViewProps {
  path: string
}

export function DirectoryView({ path }: DirectoryViewProps) {
  const [directory, setDirectory] = useState<DirectoryInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const fetchDirectory = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await apiService.getDirectory(path)
        setDirectory(data)
      } catch (err) {
        setError(err as Error)
        setDirectory(null)
      } finally {
        setLoading(false)
      }
    }

    fetchDirectory()
  }, [path])

  if (loading) {
    return <div className="loading">Loading directory...</div>
  }

  if (error) {
    return <div className="error">Error loading directory: {error.message}</div>
  }

  if (!directory) {
    return <div className="error">Directory not found</div>
  }

  return (
    <div className="directory-view">
      <div className="directory-header">
        <h1 className="directory-title">
          {directory.name === '.' ? 'Root Directory' : directory.name}
        </h1>
        <div className="breadcrumb">
          <Breadcrumb path={path} />
        </div>
      </div>
      
      <div className="file-list">
        {directory.files.map((file) => (
          <FileItem key={file.path} file={file} />
        ))}
      </div>
    </div>
  )
}

function Breadcrumb({ path }: { path: string }) {
  const parts = path === '.' ? [] : path.split('/').filter(Boolean)
  
  return (
    <div>
      <Link to="/">Home</Link>
      {parts.map((part, index) => {
        const currentPath = parts.slice(0, index + 1).join('/')
        return (
          <span key={index}>
            {' / '}
            <Link to={`/directory/${currentPath}`}>{part}</Link>
          </span>
        )
      })}
    </div>
  )
}

function FileItem({ file }: { file: FileInfo }) {
  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
  }

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleDateString()
  }

  if (file.is_directory) {
    return (
      <Link to={`/directory/${file.path}`} className="file-item">
        <span className="file-icon">📁</span>
        <span className="file-name">{file.name}</span>
        <span className="file-size">{formatDate(file.modified_time)}</span>
      </Link>
    )
  }

  return (
    <Link to={`/content/${file.path}`} className="file-item">
      <span className="file-icon">📄</span>
      <span className="file-name">{file.name}</span>
      <span className="file-size">
        {formatFileSize(file.size)} • {formatDate(file.modified_time)}
      </span>
    </Link>
  )
}