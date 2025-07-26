"""Tests for markdown service."""
import pytest
import tempfile
import os
from pathlib import Path
from src.services.markdown_service import MarkdownService
from src.models import MarkdownContent


class TestMarkdownService:
    """Test MarkdownService."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    @pytest.fixture
    def markdown_service(self, temp_dir):
        """Create a MarkdownService instance."""
        return MarkdownService(temp_dir)
    
    @pytest.fixture
    def sample_markdown_file(self, temp_dir):
        """Create a sample markdown file."""
        content = """---
title: "Test Document"
date: "2025-07-24"
tags: ["test", "sample"]
---

# Test Document

This is a **test** document with [a link](./other.md).

## Section 1

Some content here.

```python
def hello():
    print("Hello, world!")
```
"""
        file_path = temp_dir / "test.md"
        file_path.write_text(content)
        return file_path
    
    def test_parse_markdown_with_frontmatter(self, markdown_service, sample_markdown_file):
        """Test parsing markdown with frontmatter."""
        content = markdown_service.parse_markdown(sample_markdown_file)
        
        assert isinstance(content, MarkdownContent)
        assert content.frontmatter["title"] == "Test Document"
        assert content.frontmatter["date"] == "2025-07-24"
        assert "test" in content.frontmatter["tags"]
        assert '<h1 id="test-document">Test Document</h1>' in content.html_content
        assert "<strong>test</strong>" in content.html_content
        assert content.title == "Test Document"
    
    def test_parse_markdown_without_frontmatter(self, markdown_service, temp_dir):
        """Test parsing markdown without frontmatter."""
        content = "# Simple Document\n\nJust some text."
        file_path = temp_dir / "simple.md"
        file_path.write_text(content)
        
        result = markdown_service.parse_markdown(file_path)
        
        assert result.frontmatter == {}
        assert result.title == "Simple Document"
        assert '<h1 id="simple-document">Simple Document</h1>' in result.html_content
    
    def test_parse_markdown_with_code_highlighting(self, markdown_service, sample_markdown_file):
        """Test that code blocks are properly highlighted."""
        content = markdown_service.parse_markdown(sample_markdown_file)
        
        # Should contain syntax highlighting classes
        assert "codehilite" in content.html_content or "highlight" in content.html_content
    
    def test_convert_relative_links(self, markdown_service, temp_dir):
        """Test that relative links are converted properly."""
        content = """# Test
        
[Link to other](./other.md)
[Link to subdirectory](./subdir/file.md)
[External link](https://example.com)
"""
        file_path = temp_dir / "test.md"
        file_path.write_text(content)
        
        result = markdown_service.parse_markdown(file_path)
        
        # Relative links should be converted to API endpoints
        assert "/api/content?path=other.md" in result.html_content
        assert "/api/content?path=subdir/file.md" in result.html_content
        # External links should remain unchanged
        assert "https://example.com" in result.html_content
    
    def test_get_file_list(self, markdown_service, temp_dir):
        """Test getting list of markdown files."""
        # Create some test files
        (temp_dir / "file1.md").write_text("# File 1")
        (temp_dir / "file2.md").write_text("# File 2")
        (temp_dir / "not_markdown.txt").write_text("Not markdown")
        
        # Create subdirectory
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "file3.md").write_text("# File 3")
        
        files = markdown_service.get_file_list()
        
        # Should include markdown files and directories
        file_names = [f.name for f in files]
        assert "file1.md" in file_names
        assert "file2.md" in file_names
        assert "subdir" in file_names
        assert "not_markdown.txt" not in file_names
    
    def test_get_directory_info(self, markdown_service, temp_dir):
        """Test getting directory information."""
        # Create test structure
        (temp_dir / "file1.md").write_text("# File 1")
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "file2.md").write_text("# File 2")
        
        dir_info = markdown_service.get_directory_info(".")
        
        assert dir_info.path == "."
        assert len(dir_info.files) >= 2  # At least file1.md and subdir
        
        # Test subdirectory
        subdir_info = markdown_service.get_directory_info("subdir")
        assert subdir_info.name == "subdir"
        assert any(f.name == "file2.md" for f in subdir_info.files)
    
    def test_file_not_found(self, markdown_service):
        """Test handling of non-existent files."""
        with pytest.raises(FileNotFoundError):
            markdown_service.parse_markdown(Path("nonexistent.md"))
    
    def test_directory_traversal_protection(self, markdown_service):
        """Test that directory traversal is prevented."""
        with pytest.raises(ValueError, match="Path traversal"):
            markdown_service.get_directory_info("../../../etc")
        
        with pytest.raises(ValueError, match="Path traversal"):
            markdown_service.parse_markdown(Path("../../../etc/passwd"))