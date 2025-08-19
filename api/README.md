# Home Shopping API - Modular Structure

This document describes the modular structure of the Home Shopping API, which has been refactored from a monolithic single file to a more maintainable architecture.

## Directory Structure

```
api/
├── __init__.py
├── app.py
├── app_factory.py
├── init_db.py
├── test_db.py
├── test_imports.py
├── verify_routes.py
├── requirements.txt
├── models/
│   ├── __init__.py
│   ├── category.py
│   ├── subcategory.py
│   ├── item.py
│   └── option.py
├── routes/
│   ├── __init__.py
│   ├── categories.py
│   ├── items.py
│   ├── options.py
│   ├── dashboard.py
│   ├── export.py
│   └── health.py
└── utils/
    ├── __init__.py
    └── helpers.py
```

## Components

### Application Factory (`app_factory.py`)

Implements the Flask application factory pattern for better structure and testing. It initializes the Flask app, configures it, and registers all blueprints.

### Models (`models/`)

Contains all database models:

-   `category.py`: Category model for main categories
-   `subcategory.py`: Subcategory model for subcategories
-   `item.py`: Item model for shopping items
-   `option.py`: Option model for item options/choices

### Routes (`routes/`)

Contains all API endpoints organized by functionality:

-   `categories.py`: Category and subcategory endpoints
-   `items.py`: Item CRUD endpoints
-   `options.py`: Option CRUD and selection endpoints
-   `dashboard.py`: Dashboard data endpoints
-   `export.py`: Export functionality
-   `health.py`: Health check endpoint

### Utilities (`utils/`)

Contains helper functions:

-   `helpers.py`: Utility functions like `ensure_one_selected`

## Benefits of This Structure

1. **Modularity**: Each component has its own file/directory
2. **Maintainability**: Easier to find and modify specific functionality
3. **Scalability**: New features can be added without cluttering existing files
4. **Testability**: Components can be tested independently
5. **Readability**: Clear separation of concerns

## Running the Application

```bash
cd api
python app.py
```

## Testing Imports

```bash
cd api
python test_imports.py
```

## Verifying Routes

```bash
cd api
python verify_routes.py
```
