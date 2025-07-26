import { DirectoryInfo, MarkdownContent, SearchResult } from '../types'

const API_BASE_URL = import.meta.env.PROD ? 'http://localhost:50858/api' : '/api'

class ApiService {
  private async fetchJson<T>(url: string): Promise<T> {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return response.json()
  }

  async getDirectory(path: string = '.'): Promise<DirectoryInfo> {
    const encodedPath = encodeURIComponent(path)
    return this.fetchJson<DirectoryInfo>(`${API_BASE_URL}/directory?path=${encodedPath}`)
  }

  async getContent(path: string): Promise<MarkdownContent> {
    const encodedPath = encodeURIComponent(path)
    return this.fetchJson<MarkdownContent>(`${API_BASE_URL}/content?path=${encodedPath}`)
  }

  async search(query: string): Promise<SearchResult[]> {
    const encodedQuery = encodeURIComponent(query)
    return this.fetchJson<SearchResult[]>(`${API_BASE_URL}/search?q=${encodedQuery}`)
  }

  async healthCheck(): Promise<{ status: string; service: string }> {
    const healthUrl = import.meta.env.PROD ? 'http://localhost:50858/health' : '/health'
    return this.fetchJson(healthUrl)
  }
}

export const apiService = new ApiService()