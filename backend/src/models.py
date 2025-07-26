"""Data models for the serve-md application."""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileInfo:
    """Information about a file or directory."""
    name: str
    path: str
    is_directory: bool
    size: int
    modified_time: Optional[float] = None
    
    @classmethod
    def from_path(cls, file_path: Path, base_path: Path) -> "FileInfo":
        """Create FileInfo from a file path."""
        relative_path = file_path.relative_to(base_path)
        stat = file_path.stat()
        
        return cls(
            name=file_path.name,
            path=str(relative_path).replace("\\", "/"),  # Normalize path separators
            is_directory=file_path.is_dir(),
            size=stat.st_size if not file_path.is_dir() else 0,
            modified_time=stat.st_mtime
        )


@dataclass
class DirectoryInfo:
    """Information about a directory and its contents."""
    name: str
    path: str
    files: List[FileInfo]
    
    def get_markdown_files(self) -> List[FileInfo]:
        """Get only markdown files from the directory."""
        return [f for f in self.files if f.name.endswith('.md') and not f.is_directory]
    
    def get_subdirectories(self) -> List[FileInfo]:
        """Get only subdirectories."""
        return [f for f in self.files if f.is_directory]


@dataclass
class MarkdownContent:
    """Parsed markdown content with metadata."""
    raw_content: str
    html_content: str
    frontmatter: Dict[str, Any]
    file_path: str
    title: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Extract title from frontmatter or content."""
        if not self.title:
            # Try to get title from frontmatter
            self.title = self.frontmatter.get('title')
            
            # If no title in frontmatter, try to extract from first heading
            if not self.title and self.raw_content:
                lines = self.raw_content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('# '):
                        self.title = line[2:].strip()
                        break
            
            # Fallback to filename
            if not self.title:
                self.title = Path(self.file_path).stem.replace('-', ' ').replace('_', ' ').title()