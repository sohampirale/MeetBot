# MeetBot - AI Agents for Interactive Meeting Presentations

## Project Overview

MeetBot is a platform that enables users to create voice AI agents that join video meetings and interact like human presenters. These AI agents can hold conversations, respond to questions, and present visual materials (PowerPoint presentations, images, and videos) during meetings.

### Core Concept

This project revolves around **voice AI agents in meetings**. MeetBot creates voice AI agents that can:
- Create and join video meetings dynamically
- Interact conversationally with meeting participants (respond to questions, have discussions)
- Present visual materials (PPTs, images, videos) during the meeting
- Behave according to user-defined personas, tones, and workflows

### What Makes MeetBot Special

MeetBot agents mimic human meeting behavior by combining voice interaction with visual presentations. The platform targets use cases where organizations want to automate meeting-based interactions that benefit from visual presentations - scenarios like product demos, training sessions, customer onboarding, or sales presentations.

**v0 Goal:** Build a voice AI agent that can interact conversationally while presenting PowerPoint slides, images, and videos in video meetings.

## How It Works

### Voice AI Framework
- **Framework:** Pipecat (Python framework for building voice AI agents)
- **Architecture:** Traditional voice pipeline (Speech-to-Text → LLM → Text-to-Speech)
- **Transport:** Daily.co (WebRTC-based video conferencing)
- Future consideration: LiveKit transport (not in v0)

### Visual Interactions

The bot can perform three presentation actions in meetings:

1. **Present PowerPoint (PPT)**
   - User uploads: PPT file, slide-by-slide explanation/guidelines, intent/purpose of presentation
   - Bot explains slides naturally based on provided context
   
2. **Present Video**
   - User uploads: Video file, pre-video explanation, post-video explanation, intent/purpose
   - Bot understands when to present video based on meeting context
   
3. **Present Image**
   - User uploads: Image file, explanation/description, intent/purpose
   - Bot explains image relevance during meeting

### User Workflow & Bot Behavior

**Bot Creation:**
- End users create bots through the Next.js frontend
- Users write a **system prompt** that defines the bot's:
  - Tone and persona
  - Meeting workflow and behavior
  - How it decides when to present materials (sequence or context-based)
  
**Meeting Invocation:**
- Bot is NOT invoked immediately upon creation
- User creates a **registration form** with custom fields (name, email, city, etc.)
- Visitors fill the form and receive a unique meeting URL
- Backend dynamically creates a new Daily.co meeting for each form submission
- Bot automatically joins the meeting when created
- Meeting has a maximum time limit (user-specified), after which meeting ends and bot leaves

## Tech Stack

**Full-stack application:**
- **Frontend:** Next.js (React)
- **Backend:** FastAPI (Python) + Pydantic
- **Database:** MongoDB with Beanie ODM (async, Pydantic-native)
- **Voice AI:** Pipecat framework
- **Video Transport:** Daily.co (WebRTC)

## Codebase Structure

```
meetbot/
├── AGENTS.md                    # This file - root project context
├── frontend/                    # Next.js application
│   └── AGENTS.md               # Frontend-specific context (if needed)
└── backend/                     # FastAPI application
    ├── AGENTS.md               # Backend-specific context (if needed)
    ├── db_schema.md                # Database models and schema documentation
    └── api_endpoints/  # API routes and endpoint documentation
            ├── AGENTS.md               # Context for working with any endpoints at backend level
            ├────user_endpoints.md  #All endpoints related to user
            ├────bot_endpoints.md   #All endpoints related to bot
            └────credit_endpoints.md  #All endpoints related to credit
```

### Key Context Files
- **db_schema.md:** Defines MongoDB collections, Beanie models, data relationships
- **api_endpoints.md:** Documents all API routes, request/response formats, business logic

## Instructions for AI Coding Agents

### Navigation Rules
1. **Do not enter any subdirectory without definite purpose** - stay focused on your task
2. **Each subdirectory MAY have an AGENTS.md file** for additional context specific to that directory
3. **Always read AGENTS.md when entering a subdirectory** where you need to perform work
4. **Do not read AGENTS.md files** of directories where you won't perform any read/write operations

### Context Discovery Pattern
When working on a task:
1. Read this root `AGENTS.md` first to understand the project
2. Determine which part of the codebase your task relates to (frontend/backend)
3. Navigate to the relevant directory and read its `AGENTS.md` if present
4. For backend work, consult `db_schema.md` and `api_endpoints.md` as needed

### Development Principles
- This project is in **v0 stage** - focus on core functionality
- Frontend and backend agents should work on application logic, NOT Pipecat framework internals
- Pipecat voice agent code is a separate concern (handled by specialized implementation)
- Maintain clear separation between user-facing platform and voice agent runtime

## Current Development Status

**v0 Scope:**
- User can create voice AI bots via frontend
- User can configure bot behavior via system prompt
- User can upload presentation materials (PPT, images, videos)
- User can create registration forms for meeting access
- Backend dynamically creates Daily.co meetings
- Bot joins meetings and presents materials while conversing
- Meetings have configurable time limits

**Out of Scope for v0:**
- Bot joining existing meetings via link
- Advanced features beyond core presentation capabilities
- Alternative transport layers (LiveKit)

---

**Note to AI Agents:** This is a well-architected project that separates concerns clearly. Focus on building robust frontend and backend components. The voice AI complexity is abstracted into the Pipecat framework layer.
