# 🚀 Django Studio

**Professional Django Development Environment** — a modern, feature-rich IDE for Django developers.

Django Studio is a desktop IDE built with PySide6 that provides everything you need to develop Django applications efficiently. From code editing to database management, all in one integrated environment with Django's official color scheme.

## ✨ Key Features

### Advanced Code Editor

- **Syntax Highlighting** - Django & Python-optimized with 20+ color-coded token types
- **Find & Replace** - Real-time matching with case/whole-word options  
- **Code Folding** - Collapse/expand functions, classes, and blocks with visual indicators
- **Bracket Matching** - Visual pair highlighting for perfect alignment
- **Minimap** - Color-coded file overview with viewport tracking
- **Auto-Formatting** - Intelligent code formatting on save
- **Git Gutter** - Visual diff indicators (added/modified/deleted lines)
- **Multi-Cursor** - Edit multiple locations simultaneously
- **Breadcrumb Navigation** - Quick navigation through code structure
- **Line Numbers** - With visual fold and git indicators

### Project Management

- **Project Wizard** - Create Django projects with recommended settings
- **File Browser** - Navigate your project structure visually
- **Recent Projects** - Quick access to frequently used projects
- **Auto-Save** - Never lose work with dirty file tracking

### Django Integration

- **Management Commands** - Run Django commands from the toolbar
- **Database Inspector** - Browse models and inspect data
- **API Tester** - Built-in request builder for testing APIs
- **Log Viewer** - Monitor application output in real-time
- **Terminal Integration** - Run custom commands directly

### Modern UI & Theme

- **Django-Branded** - Official Django green (`#092E20`, `#44B78B`)
- **Dark Mode** - Eye-friendly dark theme for extended development sessions
- **Professional Design** - Inspired by VS Code and modern IDEs
- **Responsive Layout** - Seamless experience on all screen sizes
- **Custom Icons** - SVG toolbar with professional status indicators

## 🛠️ Installation

### Requirements

- Python 3.10+
- PySide6 6.5+
- Git (optional, for git gutter features)

### Setup (Windows PowerShell)

```powershell
# Clone the repository
git clone https://github.com/yourusername/Django-Studio.git
cd Django-Studio

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run Django Studio
python src/main.py
```

### Setup (macOS/Linux)

```bash
# Clone the repository
git clone https://github.com/Arsey-Tracy/django-studio.git
cd django-studio

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Django Studio
python src/main.py
```

## 🎯 Quick Start

1. **Launch Django Studio** - Run `python src/main.py`
2. **Create or Open Project** - Welcome screen guides you
3. **Open Files** - Browse and edit from the file tree
4. **Use Toolbar** - Run servers, manage migrations, test APIs
5. **Auto-Format** - Press Ctrl+S to save and format code

## 📋 Keyboard Shortcuts

| Shortcut   | Action             |
|:---------- |:------------------ |
| `Ctrl+S`   | Save & Auto-Format |
| `Ctrl+F`   | Find Text          |
| `Ctrl+H`   | Find & Replace     |
| `Ctrl+O`   | Open Project       |
| `Ctrl+/`   | Toggle Comments    |

## 🎨 Django Theme

Django Studio features the official Django color scheme throughout:

- **Django Green Dark**: `#092E20` - Primary accent
- **Django Green Light**: `#44B78B` - Secondary accent  
- **Status Success**: `#44B78B` - Git added, check marks
- **Status Error**: `#FF6B6B` - Git deleted, errors
- **Status Warning**: `#FFD700` - Warnings
- **Status Info**: `#0C90FF` - Information

All UI elements, syntax highlighting, and status indicators use this cohesive Django-inspired palette.

## 📁 Project Structure

```bash
Django-Studio/
├── src/
│   ├── main.py                    # Application entry point
│   ├── ui/
│   │   ├── main_window.py         # Main application window
│   │   ├── welcome_window.py      # Welcome & recent projects
│   │   ├── syntax_highlighter.py  # Python syntax highlighting
│   │   └── project_wizard.py      # Django project setup
│   ├── widgets/
│   │   ├── code_editor.py         # Advanced code editor
│   │   ├── modern_toolbar.py      # Professional toolbar
│   │   ├── find_replace_widget.py # Find & Replace dialog
│   │   ├── minimap.py             # File overview widget
│   │   ├── breadcrumb_widget.py   # Code navigation
│   │   ├── line_number_area.py    # Line numbers & git gutter
│   │   ├── log_widget.py          # Output logging
│   │   └── api_tester_widget.py   # API testing tool
│   ├── utils/
│   │   ├── code_folder.py         # Code folding detection
│   │   ├── bracket_matcher.py     # Bracket pair matching
│   │   ├── git_gutter.py          # Git diff integration
│   │   ├── python_formatter.py    # Code formatting
│   │   ├── breadcrumb.py          # Code structure analysis
│   │   └── multi_cursor.py        # Multi-cursor management
│   ├── theme/
│   │   └── django_theme.py        # Django color scheme
│   ├── assets/
│   │   └── icons/                 # SVG toolbar icons
│   └── __init__.py
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project configuration
├── LICENSE                        # Project license
└── README.md                      # This file
```

## 🚀 Features Breakdown

### Code Editing

- **Smart Indentation** - Automatic Python indentation matching
- **Syntax Coloring** - 20+ token types for Python/Django
- **Operator Spacing** - Auto-spacing around operators on save
- **Definition Formatting** - Clean function and class declarations

### Navigation

- **Breadcrumb Trail** - Shows file → class → method path
- **Click Navigation** - Jump to definitions from breadcrumb
- **Minimap Viewport** - Visual file position indicator
- **Click-to-Jump** - Click minimap to jump to lines

### Version Control

- **Git Gutter** - Left margin shows git status per line
- **Change Types** - Added (green), Modified (blue), Deleted (red)
- **Automatic Detection** - Updates when files change

### Development Tools

- **Run Server** - Start Django development server from toolbar
- **Make Migrations** - Generate migration files
- **Migrate** - Apply migrations to database
- **Database Inspector** - Browse tables and data
- **API Tester** - Test endpoints with custom requests

## 📦 Dependencies

```bash
PySide6>=6.5.0
```

Optional dependencies for extended features:

- `django` - For full Django integration
- `black` - For Python code formatting
- `pylint` - For code analysis

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [PySide6](https://wiki.qt.io/Qt_for_Python) - Qt for Python
- Inspired by [Django](https://www.djangoproject.com/) and modern IDEs
- Color scheme based on [Django's official branding](https://www.djangoproject.com/weblog/)
- Icons and design patterns from VS Code

## 📞 Support

For issues, questions, or suggestions:

- Open an [Issue](https://github.com/yourusername/Django-Studio/issues)
- Check existing [Discussions](https://github.com/yourusername/Django-Studio/discussions)
- Submit a [Pull Request](https://github.com/yourusername/Django-Studio/pulls)

---

**Django Studio** — Making Django development smoother, faster, and more enjoyable. 🚀

*Built by Django developers, for Django developers.*
