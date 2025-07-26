# System Architecture

The serve-md application follows a modern web architecture pattern.

## Components

### Backend (Python)
- **FastAPI** - Modern, fast web framework
- **Markdown** - Python markdown parser
- **Pygments** - Syntax highlighting
- **Python-frontmatter** - YAML frontmatter parsing

### Frontend (TypeScript)
- **React** - UI framework
- **Vite** - Build tool
- **TypeScript** - Type safety

## Data Flow

```
User Request → FastAPI → MarkdownService → File System
                ↓
            JSON Response ← HTML Content ← Parsed Markdown
```

## Security

- Path traversal protection
- CORS configuration
- Input validation

## Back to [Technical Docs](./README.md) | [Home](../README.md)