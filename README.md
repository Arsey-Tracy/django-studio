# Django Studio

Django Studio — a focused, developer-first IDE for building Django projects with a modern desktop UI.

Django Studio pairs a Django-powered backend with a PySide6 desktop front-end to give you an integrated environment for creating, managing and testing Django projects and apps without jumping between tools.

Key goals

- Streamline Django project creation with a project wizard and app generator.
- Provide visual tools: data modeling, URL routing editor, and API design.
- Built-in API testing (Postman-like tools), test runner and integrated terminal.
- Keep developers in one app: code, test, run, and inspect databases and routes.

Project status
Under active development — this repository contains the early scaffolding and launcher. Contributions, ideas and PRs are welcome.

Highlights / Features

- Project wizard: create a new Django project with recommended settings and optional app templates.
- Multi-app generator: add one or multiple apps to a project in a single flow.
- Visual data modeler: design models visually and generate Django model code.
- URL & Router designer: visually map URLs to views/routers and generate route files.
- API Tester: built-in request builder and test runner (similar to Postman) that integrates with your project's Django test client.
- Integrated terminal: run Django management commands, migrations, and custom commands from the app.
- Built-in test runner: run and inspect unit tests inside the IDE with quick failure navigation.
- Database inspector: browse models, rows and run quick queries.
- Extensible: plugin-friendly architecture for adding generators, code templates, and tools.

Why use Django Studio

- Reduce context switching: no more bouncing between an editor, terminal, and API testing tools.
- Accelerate project setup and scaffold repeatable app patterns.
- Visualize complex routing and data relationships to reduce mistakes.

Quick assumptions

- This repository contains a launcher/entrypoint at `main.py`. The README below assumes `main.py` starts the desktop application; adapt if your entrypoint differs.
- Python 3.10+ recommended.

Installation (development)
These commands are written for Windows PowerShell.

```powershell
# create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies (create a requirements.txt in the repo if missing)
pip install -r requirements.txt

# run the app (assumes main.py is the launcher)
python main.py
```

If you prefer, develop using an IDE (VS Code, PyCharm) with the virtual environment activated.

Quick start (what to try first)

1. Launch the app: `python main.py`.
2. Use the Project Wizard to create a new Django project scaffold.
3. Run the built-in terminal and execute `python manage.py migrate` in the project workspace.
4. Add an app using the multi-app generator and open the modeler to design new models.
5. Use the API Tester to craft requests against your local development server.

Development notes

- Architecture: the project pairs a Django backend (providing project/app generation, template rendering and optional local servers) with a PySide6 desktop client that serves as the UI.
- Expect a folder structure that contains UI code (PySide) and Django scaffolding templates. The backend will often run embedded or be called through the launcher process.

Contributing

- Issues and feature requests: file them in the repository's issue tracker with a clear title and reproduction steps.
- Development workflow:
    1. Fork the repo and create a feature branch.
    2. Add tests for new features where applicable.
    3. Open a PR with a clear summary of changes and any migration or environment notes.

Roadmap (next high-value items)

- Add a published `requirements.txt` and a minimal `pyproject.toml`.
- Implement the multi-app generator CLI and wire it into the UI.
- Add unit and integration tests for generators and modeler codegen.
- Create template starter projects (minimal, REST API, channels-ready).
- Improve API test runner to save and export request collections.

Files & entry points

- `main.py` — development launcher / app entrypoint (assumed).
- `LICENSE` — project license (see repo root).

Security & privacy

- This tool runs locally. When integrating network tools (API tester, request history) be mindful of storing secrets. We recommend an opt-in encrypted store for tokens and credentials.

Contact & credits
Built with ❤️ by the project maintainers. If you'd like to help, open an issue or submit a PR.

License
See the `LICENSE` file in the repository root for license details.

Enjoy using Django Studio — feedback and contributions welcome!
