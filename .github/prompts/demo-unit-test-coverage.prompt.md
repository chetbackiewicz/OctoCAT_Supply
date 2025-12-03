---
agent: 'agent'
description: 'Improve API Test Coverage - Add Unit Tests for Missing Routes.'
tools: ['runCommands', 'runTasks', 'edit/editFiles', 'search', 'usages', 'problems', 'changes', 'testFailure', 'fetch', 'githubRepo']
---
# 🧪 Add Unit Tests for Product and Supplier Routes

## 📊 Current State
- Only **1 test file exists**: `test_suppliers.py`

## 🎯 Objective
Increase API test coverage by implementing comprehensive unit tests for Product and Supplier routes.

## 📋 Missing Test Files

### 🔗 Route Tests (High Priority)
The following route files need complete test coverage:

- [ ] `tests/test_products.py`
- [ ] `tests/test_suppliers.py`

## ✅ Test Coverage Requirements

### For Each Route Test File:
- **CRUD Operations:**
  - ✅ GET all entities
  - ✅ GET single entity by ID
  - ✅ POST create new entity
  - ✅ PUT update existing entity
  - ✅ DELETE entity by ID

- **Error Scenarios:**
  - ❌ 404 for non-existent entities
  - ❌ 400 for invalid request payloads
  - ❌ 422 for validation errors
  - ❌ Edge cases (malformed IDs, empty requests)

## 🛠️ Implementation Guidelines

### Use Existing Pattern
Follow the pattern established in `tests/test_suppliers.py`:
```python
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
```

### Test Structure Template
```python
class TestEntityAPI:
    def test_create_entity(self):
        """POST test"""
        pass
    
    def test_get_all_entities(self):
        """GET all test"""
        pass
    
    def test_get_entity_by_id(self):
        """GET by ID test"""
        pass
    
    def test_update_entity(self):
        """PUT test"""
        pass
    
    def test_delete_entity(self):
        """DELETE test"""
        pass
    
    def test_not_found(self):
        """Error test - 404"""
        pass
```

## 🔧 Running Tests

```bash
# Run all tests
make test-api

# Run tests with coverage
cd api && make test-coverage

# Run specific test file
cd api && pytest tests/test_products.py
```

## 📈 Success Criteria
- [ ] Add route test files for Product and Supplier
- [ ] All tests passing in CI/CD

## 🚀 Getting Started
1. Start with `test_products.py` - copy `test_suppliers.py` pattern
2. Implement basic CRUD tests first
3. Add error scenarios incrementally
4. Run coverage after each file to track progress
5. Follow ERD relationships for cross-entity testing

## 📚 Related Files
- Existing test: `api/tests/test_suppliers.py`
- Test config: `api/pyproject.toml`
