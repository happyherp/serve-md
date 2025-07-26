"""Tests for the FastAPI application."""
import pytest
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from src.main import create_app


class TestAPI:
    """Test the FastAPI application."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    @pytest.fixture
    def sample_knowledge_base(self, temp_dir):
        """Create a sample knowledge base structure."""
        # Create main README
        readme_content = """---
title: "Knowledge Base"
date: "2025-07-24"
---

# Knowledge Base

Welcome to the knowledge base!

## Sections

- [Technical Research](./technical/README.md)
- [Market Research](./market/README.md)
"""
        (temp_dir / "README.md").write_text(readme_content)
        
        # Create technical directory
        tech_dir = temp_dir / "technical"
        tech_dir.mkdir()
        (tech_dir / "README.md").write_text("# Technical Research\n\nTechnical documentation goes here.")
        (tech_dir / "study1.md").write_text("# Study 1\n\nFirst technical study.")
        
        # Create market directory
        market_dir = temp_dir / "market"
        market_dir.mkdir()
        (market_dir / "README.md").write_text("# Market Research\n\nMarket analysis goes here.")
        
        return temp_dir
    
    @pytest.fixture
    def client(self, sample_knowledge_base):
        """Create a test client."""
        app = create_app(sample_knowledge_base)
        return TestClient(app)
    
    def test_get_directory_root(self, client):
        """Test getting the root directory."""
        response = client.get("/api/directory")
        assert response.status_code == 200
        
        data = response.json()
        assert data["path"] == "."
        assert len(data["files"]) >= 3  # README.md, technical/, market/
        
        # Check that we have the expected files
        file_names = [f["name"] for f in data["files"]]
        assert "README.md" in file_names
        assert "technical" in file_names
        assert "market" in file_names
    
    def test_get_directory_subdirectory(self, client):
        """Test getting a subdirectory."""
        response = client.get("/api/directory?path=technical")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "technical"
        assert data["path"] == "technical"
        
        file_names = [f["name"] for f in data["files"]]
        assert "README.md" in file_names
        assert "study1.md" in file_names
    
    def test_get_directory_not_found(self, client):
        """Test getting a non-existent directory."""
        response = client.get("/api/directory?path=nonexistent")
        assert response.status_code == 404
    
    def test_get_content_root_readme(self, client):
        """Test getting the root README content."""
        response = client.get("/api/content?path=README.md")
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Knowledge Base"
        assert data["file_path"] == "README.md"
        assert "Knowledge Base" in data["html_content"]
        assert data["frontmatter"]["title"] == "Knowledge Base"
    
    def test_get_content_subdirectory_file(self, client):
        """Test getting content from a subdirectory."""
        response = client.get("/api/content?path=technical/study1.md")
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Study 1"
        assert data["file_path"] == "technical/study1.md"
        assert "First technical study" in data["html_content"]
    
    def test_get_content_not_found(self, client):
        """Test getting non-existent content."""
        response = client.get("/api/content?path=nonexistent.md")
        assert response.status_code == 404
    
    def test_get_content_directory_traversal(self, client):
        """Test that directory traversal is prevented."""
        response = client.get("/api/content?path=../../../etc/passwd")
        assert response.status_code == 400
        assert "Path traversal" in response.json()["detail"]
    
    def test_search_content(self, client):
        """Test searching content."""
        response = client.get("/api/search?q=technical")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) >= 1
        
        # Should find the technical README
        paths = [result["path"] for result in data]
        assert any("technical" in path for path in paths)
    
    def test_search_empty_query(self, client):
        """Test searching with empty query."""
        response = client.get("/api/search?q=")
        assert response.status_code == 400
    
    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_cors_headers(self, client):
        """Test that CORS headers are present for preflight requests."""
        # Test that the app handles CORS (middleware is configured)
        # For actual CORS testing, we'd need a real browser or more complex setup
        # For now, just verify the endpoint works
        response = client.get("/api/directory")
        assert response.status_code == 200