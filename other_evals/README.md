# AI-Native Flask Template

A Flask application template designed for AI-collaborative development with smart defaults, automated workflows, and comprehensive testing.

## Features

- 🌐 **Production-Ready Flask**: Complete Flask app with health endpoints and proper structure
- 🤖 **AI-Optimized**: Structured for seamless AI collaboration
- 🚀 **Smart Defaults**: Only asks for project name - handles the rest
- 📁 **Project-Based Naming**: Uses your project name instead of generic `main.py`
- 🧪 **4-Phase Testing**: Backend → API → Contract → Frontend
- 🔄 **Automated Workflows**: Git branching, testing, and merging scripts
- 📦 **Complete Setup**: Virtual environment, dependencies, and structure

## Prerequisites

- Python 3.8+ installed on your system
- Git (for cloning and project workflows)
- Terminal/Command line access

## Quick Start

git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
git clone https://github.com/ksylvain77/ai-native-flask-template.git

### Recommended: Generate Projects Outside the Template Directory

**1. Download or clone this template repository somewhere safe (e.g., `~/templates/ai-native-flask-template`).**

**2. Whenever you want to create a new project, go to the folder where you want your project to live (e.g., `~/projects/`):**

```bash
# Example: create a new project called my-awesome-project in ~/projects
cd ~/projects
python3 ~/templates/ai-native-flask-template/init_project.py my-awesome-project
cd my-awesome-project
python manage.py setup
python manage.py start
```

**This keeps the template repo clean and lets you generate as many projects as you want, anywhere you want.**

---

### Option: Use as GitHub Template

Click the green **"Use this template"** button above, then:

```bash
# 1. Clone your new repository
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME

# 2. Initialize your project (this transforms the template into a working app)
python3 init_project.py

# 3. Start developing
python manage.py setup
python manage.py start
```

**That's it!** Your project will be running at `http://localhost:5000` with a complete development environment ready for AI collaboration.

## What Gets Generated

```
my-awesome-project/
├── my_awesome_project.py    # Main Flask application (named after your project)
├── modules/
│   ├── core.py             # Core business logic
│   └── utils.py            # Utility functions
├── tests/
│   ├── quick_test.py       # Fast development tests (2s)
│   └── test_suite.py       # Comprehensive testing (30s+)
├── scripts/
│   ├── create-repo.sh      # GitHub repository automation
│   ├── create-branch.sh    # AI workflow: create feature branch
│   ├── merge-to-main.sh    # AI workflow: test + merge + cleanup
│   └── run-tests.sh        # Comprehensive test runner
├── .github/
│   └── copilot-instructions.md  # AI collaboration guide
├── requirements.txt        # Python dependencies
├── manage.sh              # Project management script
├── .gitignore             # Comprehensive Git ignore rules
└── README.md              # Project-specific documentation
```

## AI-Native Development Workflow

The generated projects follow an AI-collaborative workflow:

1. **Initialize project**: Create and set up your project locally
2. **Create GitHub repository**: `./scripts/create-repo.sh` (optional: `--private`)
3. **AI creates feature branch**: `./scripts/create-branch.sh feature-name "Description"`
4. **AI implements feature** with immediate testing feedback
5. **User approves** the implementation
6. **AI merges automatically**: `./scripts/merge-to-main.sh "Final message"`

### Repository Creation

The template includes automated GitHub repository creation:

```bash
# Create a public repository (default)
./scripts/create-repo.sh

# Create a private repository
./scripts/create-repo.sh --private
```

**Prerequisites**:

- GitHub CLI installed (`brew install gh` or `apt install gh`)
- Authenticated with GitHub (`gh auth login`)

The script will:

- ✅ Create the GitHub repository with your project name and description
- ✅ Set up the remote origin automatically
- ✅ Push your initial commit
- ✅ Update any placeholder URLs in your project files

### Key Principles

- **Merge as You Go**: Main branch always working, immediate integration
- **Test-Driven**: 100% test pass rate required before merge
- **Documentation-Driven**: Auto-maintained docs with live system data

## Template Customization

The template uses placeholder replacement for full customization:

- `{{PROJECT_NAME}}` → Your project name
- `{{PROJECT_DESCRIPTION}}` → Your project description
- `{{MAIN_FILE}}` → `your_project_name.py`
- `{{SERVICE_NAME}}` → `your_project_name`

All generated files are fully functional with proper Flask setup, testing framework, and development scripts.

## Requirements

- Python 3.8+
- Git (for generated project workflows)

## Generated Project Features

Each generated project includes:

- ✅ **Working Flask application** with health endpoints
- ✅ **Complete test suite** with 4-phase methodology
- ✅ **Virtual environment setup** with dependencies
- ✅ **Git workflow automation** for AI collaboration
- ✅ **Proper .gitignore** for Python projects
- ✅ **AI collaboration guides** in `.github/copilot-instructions.md`

## Examples

```bash
# Create a blog API
python3 init_project.py blog-api
# Generates: blog_api.py as Flask main file

# Create a user management service
python3 init_project.py user-service
# Generates: user_service.py as Flask main file

# Create any Flask web service
python3 init_project.py my-api
# Generates: my_api.py as Flask main file
```

Each generated project is a complete Flask application with endpoints, testing, and AI-collaborative workflows.

## Contributing

This template itself follows the AI-native methodology. To improve the template:

1. Create issues for template improvements
2. Test changes with multiple generated projects
3. Ensure 100% success rate for generated project workflows
4. Update documentation to reflect changes

**Philosophy**: The template should generate projects that work perfectly out-of-the-box with zero manual intervention required.
