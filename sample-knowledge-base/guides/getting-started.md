---
title: "Getting Started with serve-md"
date: "2025-07-26"
tags: ["guide", "getting-started"]
---

# Getting Started with serve-md

This guide will help you get started with the serve-md application.

## Prerequisites

- Python 3.8+
- Node.js 16+
- Git

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/serve-md.git
   cd serve-md
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

## Running the Application

### Backend Only (API)

```bash
cd backend
source venv/bin/activate
python -m src.main --directory ../sample-knowledge-base --port 8000
```

### With Frontend

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python -m src.main --directory ../sample-knowledge-base --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Usage

1. Open your browser to `http://localhost:3000` (frontend) or `http://localhost:8000/docs` (API docs)
2. Navigate through your markdown files
3. Use the search functionality to find content
4. Enjoy GitHub-like markdown rendering!

## Next Steps

- [Installation Guide](./installation.md)
- [Configuration](./configuration.md)
- [API Reference](../api/README.md)

## Back to [Guides](./README.md) | [Home](../README.md)