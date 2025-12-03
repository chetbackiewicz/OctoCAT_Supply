# Contributing to OctoCAT Supply

Thank you for your interest in contributing to the OctoCAT Supply Chain Management application! This is a full-stack e-commerce application built with Vue.js and FastAPI.

## 🎯 About This Project

This is a modern supply chain management and e-commerce application for AI-powered smart cat products. The frontend is built with Vue 3 and the backend uses FastAPI with Python.

## 🤝 How to Contribute

We welcome contributions in several areas:

### 1. Application Code (Vue.js/Python)

Contributions to the actual application code (frontend and API) should:

- Be realistic and representative of typical enterprise applications
- Follow existing patterns and coding standards
- Include tests where appropriate

### 2. Documentation

Documentation improvements are always welcome:

- Architecture documentation in [`docs/`](./docs/)
- Setup and configuration instructions
- Troubleshooting guides

## 🚀 Getting Started

### Prerequisites

- **Python** 3.10 or higher
- **Node.js** 18 or higher
- **npm** (comes with Node.js)
- **Git**
- **(Optional)** Docker for containerized development

### Initial Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd OctoCAT_Supply
   ```

2. **Install dependencies:**

   ```bash
   make install
   ```

3. **Initialize the database:**

   ```bash
   make db-seed
   ```

4. **Start the development servers:**

   ```bash
   make dev
   ```

   This starts both the API (port 3000) and frontend (port 5137).

### Development Workflow

1. **Create a feature branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines below

3. **Test your changes:**

   ```bash
   # Run all tests
   make test
   
   # Run API tests only
   make test-api
   
   # Run frontend tests only
   make test-frontend
   
   # Lint code
   make lint
   ```

4. **Build to ensure no errors:**

   ```bash
   make build
   ```

5. **Commit your changes** with a clear, descriptive commit message:

   ```bash
   git add .
   git commit -m "feat: Add shopping cart functionality"
   ```

6. **Push and create a Pull Request:**

   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Code Standards

### TypeScript/JavaScript

- Use TypeScript for type safety (avoid `any` unless absolutely necessary)
- Follow existing patterns in the codebase
- Use meaningful variable and function names
- Write tests for new features and bug fixes

### Vue.js/Frontend

- Use Composition API with `<script setup lang="ts">`
- Follow existing component structure patterns
- Use Pinia for global state management
- Use TanStack Vue Query for server state
- Use Tailwind CSS for styling (avoid custom CSS when possible)
- Ensure responsive design (test at mobile, tablet, and desktop sizes)
- Follow accessibility best practices (semantic HTML, ARIA labels when needed)

### API/Backend (Python/FastAPI)

- Follow RESTful conventions
- Use the repository pattern for data access
- Use Pydantic models for validation
- Validate inputs and handle errors appropriately
- Update Swagger/OpenAPI documentation for new endpoints
- Use parameterized SQL queries (never build raw query strings with user input)

### Database

- Add migrations for schema changes in `api/database/migrations/`
- Never modify existing migration files - always create a new sequential file
- Update seed data in `api/database/seed/` if needed

## 🧪 Testing Guidelines

All code changes should include appropriate tests:

- **Unit tests** for business logic and utilities
- **Integration tests** for API endpoints
- **Component tests** for complex Vue components
- Ensure tests are deterministic and don't depend on external services

Run tests before submitting:

```bash
make test
```

## 📝 Commit Message Guidelines

Use conventional commit format:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions or updates
- `refactor:` - Code refactoring
- `chore:` - Build process or auxiliary tool changes

Example:

```
feat: Add product filtering to catalog page

- Implement filter by category
- Add price range slider
- Update API endpoint to support filtering
```

## 🔍 Review Process

All contributions go through a review process:

1. **Automated checks** - Linting, tests, and builds must pass
2. **Code review** - At least one maintainer will review your changes
3. **Documentation review** - Ensure docs are updated for behavioral changes

## ❓ Questions or Issues?

- **Bug reports**: Open an Issue with details
- **Feature proposals**: Open an Issue describing the feature

## 📚 Additional Resources

- [Main README](./README.md) - Project overview and setup
- [Architecture Documentation](./docs/architecture.md) - System design details
- [Build Guide](./docs/build.md) - Detailed build instructions

## 🙏 Thank You

Your contributions help make this project better. We appreciate your time and effort!
