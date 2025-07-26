"""Tests for data models."""
import pytest
from pathlib import Path
from src.models import FileInfo, DirectoryInfo, MarkdownContent


class TestFileInfo:
    """Test FileInfo model."""
    
    def test_file_info_creation(self):
        """Test creating a FileInfo instance."""
        file_info = FileInfo(
            name="test.md",
            path="docs/test.md",
            is_directory=False,
            size=1024
        )
        
        assert file_info.name == "test.md"
        assert file_info.path == "docs/test.md"
        assert file_info.is_directory is False
        assert file_info.size == 1024
    
    def test_file_info_from_path(self):
        """Test creating FileInfo from a file path."""
        # This will be implemented when we have the actual file system
        pass


class TestDirectoryInfo:
    """Test DirectoryInfo model."""
    
    def test_directory_info_creation(self):
        """Test creating a DirectoryInfo instance."""
        files = [
            FileInfo(name="file1.md", path="docs/file1.md", is_directory=False, size=100),
            FileInfo(name="subdir", path="docs/subdir", is_directory=True, size=0)
        ]
        
        dir_info = DirectoryInfo(
            name="docs",
            path="docs",
            files=files
        )
        
        assert dir_info.name == "docs"
        assert dir_info.path == "docs"
        assert len(dir_info.files) == 2
        assert dir_info.files[0].name == "file1.md"
        assert dir_info.files[1].is_directory is True


class TestMarkdownContent:
    """Test MarkdownContent model."""
    
    def test_markdown_content_creation(self):
        """Test creating a MarkdownContent instance."""
        content = MarkdownContent(
            raw_content="# Hello\n\nThis is a test.",
            html_content="<h1>Hello</h1><p>This is a test.</p>",
            frontmatter={"title": "Test", "date": "2025-07-24"},
            file_path="docs/test.md"
        )
        
        assert content.raw_content == "# Hello\n\nThis is a test."
        assert content.html_content == "<h1>Hello</h1><p>This is a test.</p>"
        assert content.frontmatter["title"] == "Test"
        assert content.file_path == "docs/test.md"
    
    def test_markdown_content_without_frontmatter(self):
        """Test creating MarkdownContent without frontmatter."""
        content = MarkdownContent(
            raw_content="# Hello",
            html_content="<h1>Hello</h1>",
            frontmatter={},
            file_path="docs/test.md"
        )
        
        assert content.frontmatter == {}