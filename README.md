# serve-md

A web application to serve and render Markdown files with GitHub-like styling and navigation.

## Features

- 🎨 GitHub-like markdown rendering
- 🔗 Automatic hyperlink navigation between files
- 📁 Directory tree navigation
- 🔄 Live reload when files change
- 🔍 Search functionality
- 📱 Responsive design
- 🛡️ Secure file serving (prevents directory traversal)

## Quick Start

```bash
# Install dependencies
pip install -r backend/requirements.txt
cd frontend && npm install

# Start the development servers
# Backend (from project root)
python -m backend.src.main --directory ./sample-knowledge-base

# Frontend (in another terminal)
cd frontend && npm run dev
```

## Architecture

- **Backend**: Python with FastAPI
- **Frontend**: TypeScript with React
- **Testing**: Comprehensive test coverage with pytest and Jest

## Development

This project follows Test-Driven Development (TDD) principles. All features are developed with tests first.

### Backend Development

```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest
```

### Frontend Development

```bash
cd frontend
npm install
npm test
npm run dev
```

## License

MIT License - see [LICENSE](LICENSE) file for details.