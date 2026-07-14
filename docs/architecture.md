# MacroVerba Architecture

## Purpose

MacroVerba is an open-source framework for extracting, analyzing, and visualizing macroeconomic narratives from textual data.

---

## Guiding Principles

- Modular architecture
- Reproducible research
- Separation of data, models, and visualization
- Extensible NLP pipeline
- Version-controlled development

---

## Initial Design Decisions

### Project Structure

The project follows a modular Python architecture.

```
src/
    data/
    features/
    models/
    pipeline/
    utils/
    visualization/
```

### Data Storage

The initial database backend will be SQLite.

This can later be replaced with PostgreSQL without changing the project architecture.

### Development Environment

Python virtual environments are managed using `.venv`.

Dependencies are tracked in `requirements.txt`.