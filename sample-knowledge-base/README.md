---
title: "Sample Knowledge Base"
date: "2025-07-26"
author: "OpenHands"
---

# Sample Knowledge Base

Welcome to the sample knowledge base! This demonstrates the serve-md application.

## Features

- **GitHub-like markdown rendering** with syntax highlighting
- **Automatic hyperlink navigation** between files
- **Directory tree navigation**
- **Search functionality**
- **Responsive design**

## Sections

- [Technical Documentation](./technical/README.md)
- [User Guides](./guides/README.md)
- [API Reference](./api/README.md)

## Quick Links

- [Getting Started](./guides/getting-started.md)
- [Installation Guide](./guides/installation.md)
- [API Overview](./api/overview.md)

## Code Example

Here's a simple Python example:

```python
def hello_world():
    """A simple hello world function."""
    print("Hello, World!")
    return "Hello, World!"

if __name__ == "__main__":
    message = hello_world()
    print(f"Message: {message}")
```

## Features Showcase

### Lists

1. **Ordered lists** work great
2. **Nested items** are supported
   - Bullet points
   - Sub-items
   - Multiple levels

### Tables

| Feature | Status | Notes |
|---------|--------|-------|
| Markdown Parsing | ✅ Complete | Full CommonMark support |
| Syntax Highlighting | ✅ Complete | Pygments integration |
| Live Reload | 🚧 Planned | WebSocket support |
| Search | ✅ Complete | Full-text search |

### Links

- [External link](https://github.com)
- [Internal link](./guides/getting-started.md)
- [Relative link](technical/architecture.md)

---

*This knowledge base was generated for the serve-md project.*