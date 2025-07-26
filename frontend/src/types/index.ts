export interface FileInfo {
  name: string
  path: string
  is_directory: boolean
  size: number
  modified_time: number
}

export interface DirectoryInfo {
  name: string
  path: string
  files: FileInfo[]
}

export interface MarkdownContent {
  raw_content: string
  html_content: string
  frontmatter: Record<string, any>
  file_path: string
  title: string
}

export interface SearchResult {
  path: string
  title: string
  excerpt: string
}