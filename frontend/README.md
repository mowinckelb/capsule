# Frontend Module

## Executive Summary
**What**: Minimal monochrome web interface (black/white, Courier New, lowercase). **Why**: Clean, distraction-free UX for memory interaction. **Agent Instructions**: Maintain monochrome aesthetic, all text lowercase, use input/output mode toggle, show "thinking..." animation, test UI locally before PRs.

This is a **self-contained frontend module** that contains all UI components and static files.

## 📁 Structure

```
frontend/
├── components/             # HTML UI components
│   ├── landing.html       # Landing page
│   ├── interface.html     # Main application interface
│   └── auth.html         # Authentication forms (future)
├── static/               # Static assets
│   ├── js/              # JavaScript files
│   │   ├── app.js       # Main application logic
│   │   └── config.js    # Frontend configuration
│   └── css/             # CSS files (future)
│       └── styles.css   # Custom styles
├── interface.py         # Clean interface for other modules
├── config.py           # Frontend configuration
├── test_frontend.py    # Comprehensive tests (future)
├── __init__.py         # Module initialization
└── README.md          # This file
```

## 🔧 Usage

### For Other Modules:
```python
from frontend import frontend_service

# Get paths to frontend files
landing_page = frontend_service.get_landing_page_path()
interface_page = frontend_service.get_interface_page_path()
app_js = frontend_service.get_app_js_path()

# Check frontend health
health = frontend_service.health_check()

# List all static files
static_files = frontend_service.list_static_files()
```

### For Web Servers:
```python
from frontend import frontend_service
from fastapi.staticfiles import StaticFiles

# Mount static files
app.mount("/static", StaticFiles(directory=str(frontend_service.static_dir)), name="static")

# Serve landing page
@app.get("/")
async def get_landing():
    return FileResponse(frontend_service.get_landing_page_path())

# Serve main interface
@app.get("/interface")
async def get_interface():
    return FileResponse(frontend_service.get_interface_page_path())
```

## 🎨 Components

### Landing Page (`components/landing.html`)
- Beautiful gradient landing page
- Auto-redirects to main interface
- Fallback basic interface if needed

### Main Interface (`components/interface.html`)
- Modern, responsive design
- Authentication (login/register)
- Memory management (add/query)
- Real-time status indicators

### JavaScript App (`static/js/app.js`)
- Class-based architecture
- API communication
- Local storage management
- Keyboard shortcuts
- Error handling

### Configuration (`static/js/config.js`)
- Frontend settings
- API configuration
- Feature flags
- UI preferences

## 🧪 Features

- ✅ **Responsive Design**: Works on desktop and mobile
- ✅ **Authentication**: Login and registration forms
- ✅ **Memory Management**: Add and query personal memories
- ✅ **Real-time Updates**: Live status indicators
- ✅ **Keyboard Shortcuts**: Ctrl/Cmd + Enter to submit
- ✅ **Local Storage**: Persistent login state
- ✅ **Error Handling**: User-friendly error messages
- ✅ **Loading States**: Visual feedback during operations

## 🔄 Development Workflow

1. **Work on this branch**: `feature/frontend`
2. **Make improvements**: Modify any files in this folder
3. **Test in browser**: Open HTML files directly or through web server
4. **Test integration**: Use with API server
5. **Commit changes**: All frontend changes in one commit
6. **Merge to develop**: Only when thoroughly tested

## 🎯 Independence

This module is **completely isolated**:
- ✅ No dependencies on other feature branches
- ✅ Self-contained HTML/CSS/JS
- ✅ Can be opened directly in browser
- ✅ Clean interface for backend integration
- ✅ Independent development and testing

## 🚀 Future Enhancements

- **Dark Mode**: Toggle between light and dark themes
- **Offline Mode**: Cache and sync when online
- **PWA Support**: Install as mobile/desktop app
- **Real-time Chat**: WebSocket integration
- **File Upload**: Support for documents and images
- **Advanced Search**: Filters and sorting
- **Export/Import**: Backup and restore memories

You can improve this module without affecting any other features!
