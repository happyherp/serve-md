"""Service for handling markdown files and rendering."""
import re
from pathlib import Path
from typing import List, Optional
import markdown
from markdown.extensions import codehilite, toc, tables
import frontmatter
from ..models import MarkdownContent, FileInfo, DirectoryInfo


class MarkdownService:
    """Service for parsing and rendering markdown files."""
    
    def __init__(self, base_directory: Path):
        """Initialize the service with a base directory."""
        self.base_directory = Path(base_directory).resolve()
        self.markdown_processor = markdown.Markdown(
            extensions=[
                'codehilite',
                'toc',
                'tables',
                'fenced_code',
                'nl2br'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': True
                }
            }
        )
    
    def _validate_path(self, path: Path) -> Path:
        """Validate that the path is within the base directory."""
        try:
            resolved_path = (self.base_directory / path).resolve()
            resolved_path.relative_to(self.base_directory)
            return resolved_path
        except ValueError:
            raise ValueError(f"Path traversal detected: {path}")
    
    def _convert_relative_links(self, html_content: str) -> str:
        """Convert relative markdown links to API endpoints."""
        # Pattern to match markdown links: [text](./path.md) or [text](path.md)
        def replace_link(match):
            link_text = match.group(1)
            link_url = match.group(2)
            
            # Skip external links (http/https)
            if link_url.startswith(('http://', 'https://')):
                return match.group(0)
            
            # Convert relative markdown links to API endpoints
            if link_url.endswith('.md'):
                # Remove leading ./ if present
                clean_path = link_url.lstrip('./')
                return f'<a href="/api/content?path={clean_path}">{link_text}</a>'
            
            return match.group(0)
        
        # Replace <a href="...">...</a> tags
        html_content = re.sub(
            r'<a href="([^"]*\.md)"[^>]*>([^<]*)</a>',
            lambda m: f'<a href="/api/content?path={m.group(1).lstrip("./")}">{m.group(2)}</a>',
            html_content
        )
        
        return html_content
    
    def parse_markdown(self, file_path: Path) -> MarkdownContent:
        """Parse a markdown file and return MarkdownContent."""
        validated_path = self._validate_path(file_path)
        
        if not validated_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read and parse frontmatter
        with open(validated_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        raw_content = post.content
        metadata = post.metadata
        
        # Convert markdown to HTML
        html_content = self.markdown_processor.convert(raw_content)
        
        # Convert relative links
        html_content = self._convert_relative_links(html_content)
        
        # Reset the markdown processor for next use
        self.markdown_processor.reset()
        
        relative_path = str(validated_path.relative_to(self.base_directory))
        
        return MarkdownContent(
            raw_content=raw_content,
            html_content=html_content,
            frontmatter=metadata,
            file_path=relative_path
        )
    
    def get_file_list(self, directory_path: str = ".") -> List[FileInfo]:
        """Get list of files in a directory."""
        dir_path = Path(directory_path) if directory_path != "." else Path(".")
        validated_path = self._validate_path(dir_path)
        
        if not validated_path.exists() or not validated_path.is_dir():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        files = []
        for item in validated_path.iterdir():
            # Skip hidden files
            if item.name.startswith('.'):
                continue
            
            # Include markdown files and directories
            if item.is_dir() or item.suffix == '.md':
                files.append(FileInfo.from_path(item, self.base_directory))
        
        # Sort: directories first, then files, both alphabetically
        files.sort(key=lambda x: (not x.is_directory, x.name.lower()))
        
        return files
    
    def get_directory_info(self, directory_path: str = ".") -> DirectoryInfo:
        """Get detailed information about a directory."""
        dir_path = Path(directory_path) if directory_path != "." else Path(".")
        validated_path = self._validate_path(dir_path)
        
        if not validated_path.exists() or not validated_path.is_dir():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        files = self.get_file_list(directory_path)
        
        return DirectoryInfo(
            name=validated_path.name if validated_path.name else ".",
            path=directory_path,
            files=files
        )
    
    def search_content(self, query: str) -> List[dict]:
        """Search for content across all markdown files."""
        results = []
        
        def search_in_directory(directory: Path):
            for item in directory.iterdir():
                if item.name.startswith('.'):
                    continue
                
                if item.is_dir():
                    search_in_directory(item)
                elif item.suffix == '.md':
                    try:
                        content = self.parse_markdown(item.relative_to(self.base_directory))
                        
                        # Search in title, content, and frontmatter
                        if (query.lower() in content.title.lower() or
                            query.lower() in content.raw_content.lower() or
                            any(query.lower() in str(v).lower() for v in content.frontmatter.values())):
                            
                            results.append({
                                'path': content.file_path,
                                'title': content.title,
                                'excerpt': self._get_excerpt(content.raw_content, query)
                            })
                    except Exception:
                        # Skip files that can't be parsed
                        continue
        
        search_in_directory(self.base_directory)
        return results
    
    def _get_excerpt(self, content: str, query: str, context_length: int = 100) -> str:
        """Get an excerpt around the search query."""
        content_lower = content.lower()
        query_lower = query.lower()
        
        index = content_lower.find(query_lower)
        if index == -1:
            return content[:context_length] + "..." if len(content) > context_length else content
        
        start = max(0, index - context_length // 2)
        end = min(len(content), index + len(query) + context_length // 2)
        
        excerpt = content[start:end]
        if start > 0:
            excerpt = "..." + excerpt
        if end < len(content):
            excerpt = excerpt + "..."
        
        return excerpt