"""Main FastAPI application for serve-md."""
import argparse
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .services.markdown_service import MarkdownService


def create_app(base_directory: Path) -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="serve-md",
        description="A web application to serve and render Markdown files",
        version="0.1.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify actual origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize the markdown service
    markdown_service = MarkdownService(base_directory)
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "serve-md"}
    
    @app.get("/api/directory")
    async def get_directory(path: str = Query(".", description="Directory path")):
        """Get directory listing."""
        try:
            directory_info = markdown_service.get_directory_info(path)
            return directory_info
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Directory not found")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @app.get("/api/content")
    async def get_content(path: str = Query(..., description="File path")):
        """Get markdown file content."""
        try:
            content = markdown_service.parse_markdown(Path(path))
            return content
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @app.get("/api/search")
    async def search_content(q: str = Query(..., description="Search query")):
        """Search content across all markdown files."""
        if not q.strip():
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        try:
            results = markdown_service.search_content(q)
            return results
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler."""
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(exc)}"}
        )
    
    return app


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Serve markdown files as a web application")
    parser.add_argument(
        "--directory",
        "-d",
        type=str,
        default=".",
        help="Directory containing markdown files (default: current directory)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    # Validate directory
    base_directory = Path(args.directory).resolve()
    if not base_directory.exists():
        print(f"Error: Directory '{base_directory}' does not exist")
        return 1
    
    if not base_directory.is_dir():
        print(f"Error: '{base_directory}' is not a directory")
        return 1
    
    print(f"Starting serve-md server...")
    print(f"Base directory: {base_directory}")
    print(f"Server: http://{args.host}:{args.port}")
    print(f"API docs: http://{args.host}:{args.port}/docs")
    
    # Create the app
    app = create_app(base_directory)
    
    # Run the server
    import uvicorn
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload
    )
    
    return 0


if __name__ == "__main__":
    exit(main())