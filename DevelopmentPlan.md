# MCP Server Development Plan

## Phase 1: Requirements Gathering and Technology Decision

### Project Scope and Main Functionality
- Primary focus: Flashcard management system with CRUD operations
- Secondary consideration: Practice sessions with spaced repetition algorithm (deferred to later phases)
- Portfolio project with no constraints or limitations
- Will be used by external AI systems (MCP protocol compliance)

### API Endpoint Structure
- Main operations: CRUD for flashcards
- Special read operation: Retrieve front of card for practice mode
- Simple architecture with monolithic design

### Technology Stack
- Programming language: Python
- Framework: FastAPI
- SDK: MCP SDK for server implementation
- Database: Flat files instead of database (simplified deployment)
- Latest available versions of all technologies

### Data Models
#### Flashcard Model
- Basic fields: id, user_id, front/back content, language, timestamps
- Additional fields: image and audio support for enhanced retention
- Simple structure to minimize complexity

#### Practice Session Model
- Simple design for now: session_id, user_id, flashcard_ids, status, timestamps
- Will be expanded in later phases with spaced repetition logic

### System Architecture
- Monolithic architecture for simplicity and small scope
- No authentication or security needed at this stage
- External AI integration via MCP protocol
- Deployment considerations: Easy sharing of flashcards as plain text files

# Phase 2: Design
## MCP SDK Project Structure

### Directory Layout
Glossa/
├── resources/
│   ├── flashcards/
│   │   ├── init.py
│   │   ├── create_flashcard.py
│   │   ├── get_flashcard.py
│   │   ├── update_flashcard.py
│   │   └── delete_flashcard.py
│   ├── sessions/
│   │   ├── init.py
│   │   ├── create_session.py
│   │   ├── get_session.py
│   │   ├── update_session.py
│   │   └── delete_session.py
│   └── utils.py
├── models/
│   ├── flashcard.py
│   └── session.py
├── schemas/
│   ├── flashcard.py
│   └── session.py
├── config/
│   └── settings.py
├── data/
│   ├── flashcards/
│   └── sessions/
├── tests/
│   ├── test_flashcards.py
│   └── test_sessions.py
├── .env
├── requirements.txt
├── README.md
└── pyproject.toml

### File Descriptions
#### resources/

- Directory containing individual tools/resources for the MCP SDK
- Each resource is a separate module with specific functionality
- `flashcards/`: Tools for flashcard operations
  - `create_flashcard.py`: Tool to create a new flashcard
  - `get_flashcard.py`: Tool to retrieve a flashcard by ID
  - `update_flashcard.py`: Tool to update an existing flashcard
  - `delete_flashcard.py`: Tool to delete a flashcard
- `sessions/`: Tools for session operations
  - `create_session.py`: Tool to create a new session
  - `get_session.py`: Tool to retrieve a session by ID
  - `update_session.py`: Tool to update an existing session
  - `delete_session.py`: Tool to delete a session
- `utils.py`: Shared utility functions for resources

#### models/

- Data models for the application
- `flashcard.py`: Flashcard model with all fields including last_study_date and next_study_date
- `session.py`: Session model with all fields

#### schemas/

- Data validation schemas
- `flashcard.py`: Schema for flashcard data validation
- `session.py`: Schema for session data validation

#### config/

- Configuration settings
- `settings.py`: Configuration for the application including database path, logging level, etc.

#### data/

- Directory for storing application data
- `flashcards/`: Subdirectory for flashcard data files
- `sessions/`: Subdirectory for session data files

#### tests/

- Unit and integration tests
- `test_flashcards.py`: Tests for flashcard tools
- `test_sessions.py`: Tests for session tools

#### .env

- Environment variables file
- Contains configuration values for the application

#### requirements.txt

- List of Python dependencies
- Includes mcp-sdk, pydantic, python-dotenv, etc.

#### README.md

- Project documentation
- Installation instructions
- Usage examples
- How to use the tools/

## Design of Models, MCP API Endpoints
### Overview

This document outlines the design decisions behind the models and MCP (Model-Controller-Processor) API
endpoints. The goal is to create a flexible, scalable,
and maintainable system that supports flashcard-based learning with session tracking and user progress.

### Core Design Principles

1. **Simplicity and Readability**: The models and API endpoints are designed to be intuitive and easy to
understand.

2. **Scalability**: The database structure supports growth in users, flashcards, and sessions.

3. **Consistency**: Uniform naming conventions and data types are used throughout.

4. **Extensibility**: The design allows for future features like spaced repetition, analytics, and
collaborative learning.

### Models
#### Flashcard Model

- **Purpose**: Represents a single flashcard with a front (question) and back (answer), along with
metadata.

- **Key Fields**:
  - `id`: Unique identifier (auto-incrementing integer).
  - `front`: The question or prompt (string).
  - `back`: The answer or response (string).
  - `language`: The language of the card (e.g., "en", "es").
  - `image_url`: Optional URL to an image associated with the card.
  - `audio_url`: Optional URL to an audio clip for pronunciation.
  - `created_at`: Timestamp when the card was created.
  - `updated_at`: Timestamp when the card was last modified.
  - `last_studied`: Timestamp of the last time the card was reviewed.
  - `next_study`: Scheduled time for the next review (used for spaced repetition).

- **Design Rationale**:
  - Separating `front` and `back` allows for flexible presentation (e.g., quiz mode).
  - Including `language` enables multilingual support.
  - Media fields are optional to keep the core model lightweight.
  - Timestamps support tracking and analytics.

#### Session Model

- **Purpose**: Tracks a user’s learning session, including which cards were reviewed and performance.

- **Key Fields**:
  - `id`: Unique identifier (auto-incrementing integer).
  - `user_id`: Reference to the user who created the session.
  - `flashcard_ids`: List of card IDs included in this session.
  - `status`: Current state (`active`, `completed`, `cancelled`).
  - `started_at`: When the session began.
  - `completed_at`: When the session ended (nullable until completed).
  - `results`: Array of scores for each card reviewed (card_id + score).

- **Design Rationale**:
  - Sessions are tied to users for accountability and progress tracking.
  - Storing `flashcard_ids` allows for replay or review of past sessions.
  - `results` captures user performance, enabling adaptive learning algorithms.