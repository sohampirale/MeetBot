# MeetBot Database Schema

## Overview

This document defines the MongoDB database schema for MeetBot v0. The schema uses **Beanie ODM** with Pydantic models for type safety and FastAPI integration.

**Database:** MongoDB  
**ODM:** Beanie (async, Pydantic-native)  
**Key Pattern:** All collections use MongoDB's default `_id` (ObjectId) as the unique identifier and for references between collections.

## Schema Philosophy

The schema is designed around ownership and references:
- Every entity (except User) has an `owner` field referencing the User who created it
- Users maintain arrays of ObjectId references to their created bots
- Bots maintain arrays of ObjectId references to their presentation materials (images, videos, PPTs)
- This allows flexible many-to-many relationships while keeping queries simple

## Collections

### 1. User Collection

Represents end users who create and manage bots on the platform.

```python
{
  _id: ObjectId,                    # MongoDB default, unique identifier
  username: str,                    # Required
  email: str,                       # Required
  password: str,                    # Required, hashed (bcrypt or similar)
  created_bots: [ObjectId],         # References to Bot collection, default: []
  credit_id: ObjectId | None        # Default: None, references Credit collection
}
```

**Notes:**
- `password` will be hashed using bcrypt before storage (never store plaintext)
- `created_bots` is an array of ObjectId references to Bot documents
- `credit_id` is ObjectId reference to Credit document; initially None (credits assigned separately)

---

### 2. Credit Collection

Manages user credits/balance for platform usage.

```python
{
  _id: ObjectId,                    # MongoDB default
  owner: ObjectId,                  # Required, references User collection
  balance: float,                   # Default: 0.0 (represents dollars)
  api_key: str,                     # Default: "" (empty string)
  history: [Any]                    # Default: [] (future feature, keep as empty array)
}
```

**Notes:**
- `balance` is stored as float/double, represents USD
- `api_key` is for future programmatic API access (users calling MeetBot API from their own applications)
- `history` is reserved for future transaction/usage history tracking

---

### 3. Bot Collection

Represents a voice AI bot created by a user.

```python
{
  _id: ObjectId,                    # MongoDB default
  bot_name: str,                    # Required
  owner: ObjectId,                  # Required, references User collection
  description: str,                 # Optional, default: ""
  system_prompt: str,               # Required (defines bot behavior, tone, workflow)
  images: [ObjectId],               # References to Image collection, default: []
  videos: [ObjectId],               # References to Video collection, default: []
  ppts: [ObjectId],                 # References to PPT collection, default: []
  form: ObjectId | None             # Optional, references Form collection (v1 feature)
}
```

**Notes:**
- `system_prompt` is critical - defines bot's personality, meeting behavior, and presentation workflow
- `images`, `videos`, `ppts` arrays store ObjectId references to respective collections
- These arrays allow the bot to access and present multiple materials during meetings
- **Material reusability:** The same Image/Video/PPT can be referenced by multiple bots, allowing users to reuse materials across different bot configurations
- `form` references the registration Form collection (schema to be defined in future iteration)

---

### 4. Image Collection

Stores image assets that bots can present during meetings.

```python
{
  _id: ObjectId,                    # MongoDB default
  owner: ObjectId,                  # Required, references User collection
  name: str,                        # Optional, default: "" (for user reference only)
  url: str,                         # Required (storage location/CDN URL)
  purpose: str,                     # Required (intent: when/why to show this image)
  description: str,                 # Required (what's in the image, for bot to explain)
  meta_system_prompt: str           # Optional, default: "" (additional presentation instructions)
}
```

**Field Purpose Explained:**
- **`purpose`**: Helps the voice AI agent decide **when** and **why** to show this image during conversation (e.g., "show when discussing pricing", "use for product comparison")
- **`description`**: What the bot should **say** about the image when presenting it. Bot doesn't analyze the image with vision models; it explains based on this text
- **`meta_system_prompt`**: Advanced control over **how** to present (e.g., "pause for 3 seconds after showing", "ask if participants can see it clearly")
- **`name`**: Human-readable label for the user's reference in the UI (not used by bot)

---

### 5. Video Collection

Stores video assets that bots can present during meetings.

```python
{
  _id: ObjectId,                    # MongoDB default
  owner: ObjectId,                  # Required, references User collection
  name: str,                        # Optional, default: "" (for user reference only)
  url: str,                         # Required (storage location/CDN URL)
  purpose: str,                     # Required (intent: when/why to show this video)
  description: str,                 # Required (what to explain before/after video)
  meta_system_prompt: str           # Optional, default: "" (additional presentation instructions)
}
```

**Field Purpose Explained:**
- **`purpose`**: When and why to play this video (e.g., "use for demo walkthrough", "show when asked about features")
- **`description`**: What the bot explains **before and after** playing the video
- **`meta_system_prompt`**: Presentation nuances (e.g., "introduce video, then stay silent during playback", "ask for questions after")

---

### 6. PPT Collection

Stores PowerPoint presentation assets with slide-level metadata.

```python
{
  _id: ObjectId,                    # MongoDB default
  owner: ObjectId,                  # Required, references User collection
  ppt_url: str,                     # Required (original PPT file location)
  pngs_url: str,                    # Required (folder URL containing PNG slides)
  purpose: str,                     # Required (intent: when/why to use this presentation)
  ppt_description: str,             # Required (overall presentation summary)
  slides_description: [str],        # Required, default: [] (description for each slide)
  total_slides: int,                # Default: 1 (total number of slides)
  meta_system_prompt: str,          # Optional, default: "" (presentation-level instructions)
  slides_meta_system_prompt: [str]  # Optional, default: [] (per-slide instructions)
}
```

**Field Purpose Explained:**
- **`ppt_url`**: Original PowerPoint file (for storage/download)
- **`pngs_url`**: Single URL/path to folder containing all slide PNGs (backend converts PPT → PNGs → uploads folder to object storage)
- **`purpose`**: Overall intent of this presentation
- **`ppt_description`**: High-level summary of the entire presentation
- **`slides_description`**: Array with one description per slide (what the bot should explain for each slide)
- **`total_slides`**: Total count of slides (helps bot navigate presentation)
- **`meta_system_prompt`**: Presentation-level behavior (e.g., "speak slowly and clearly", "pause between slides")
- **`slides_meta_system_prompt`**: Array of per-slide instructions (e.g., for slide 3: "emphasize the pricing details")

**PPT Processing Flow:**
1. User uploads PPT file → stored at `ppt_url`
2. Backend converts each slide to PNG
3. All PNGs placed in a folder and uploaded to object storage
4. Folder URL/path stored in `pngs_url` (e.g., `"https://cdn.com/user123/ppt456/"`)
5. Individual slides accessed as needed during presentation

**Array Indexing Note:**
- Arrays are zero-indexed in the database
- Slide numbers are 1-indexed for users (slide 1, slide 2, etc.)
- Backend logic will handle the index mapping (slides_description[0] = Slide 1)

---

## Relationships & References

### Ownership Hierarchy
```
User (root)
 ├── owns → Credit (1:1, optional via credit_id)
 ├── owns → Bot (1:many via created_bots array)
 │    ├── references → Form (1:1, optional - v1 feature)
 │    ├── references → Image (many:many via images array)
 │    ├── references → Video (many:many via videos array)
 │    └── references → PPT (many:many via ppts array)
 ├── owns → Image (1:many, reusable across bots)
 ├── owns → Video (1:many, reusable across bots)
 └── owns → PPT (1:many, reusable across bots)
```

### Key Reference Patterns

**User → Bots:**
- User.created_bots[] contains ObjectIds referencing Bot._id
- Each Bot.owner references back to User._id

**User → Credits:**
- User.credit_id is ObjectId referencing Credit._id (initially None)
- Credit.owner is ObjectId referencing User._id

**Bot → Materials:**
- Bot.images[] contains ObjectIds referencing Image._id
- Bot.videos[] contains ObjectIds referencing Video._id
- Bot.ppts[] contains ObjectIds referencing PPT._id
- Each material (Image/Video/PPT).owner references back to User._id
- **Material reusability:** Same material can be referenced by multiple bots

**Bot → Form:**
- Bot.form is ObjectId referencing Form._id (optional, v1 feature)
- Form collection schema to be defined in future iteration

## Implementation Notes for AI Agents

### Beanie Model Structure
When implementing Beanie models:
- Use `class User(Document):` pattern
- ObjectId references use `Link` or `PydanticObjectId` types
- Required fields should not have defaults
- Optional fields with defaults: use `Field(default=...)`
- Arrays default to empty: `Field(default_factory=list)`

### Password Handling
- NEVER store plaintext passwords
- Hash with bcrypt (or argon2) before saving to database
- Use proper salt rounds (12+ for bcrypt)

### Query Patterns
Common queries agents might implement:
- Fetch user's bots: Query Bot collection with `Bot.owner == user_id`
- Fetch bot's materials: Use Bot.images/videos/ppts arrays to query respective collections
- Populate references: Use Beanie's `fetch_links()` for eager loading

### File Storage
- `url`, `ppt_url`, `pngs_url` fields store location references (CDN URLs, S3 paths, etc.)
- Actual file upload/storage logic is handled separately (not in schema)
- Consider using cloud storage (AWS S3, Cloudinary, etc.) for production

---

## V0 Scope Reminder

This schema supports MeetBot v0 features:
- User authentication and bot creation
- Uploading and managing presentation materials
- Bot configuration via system prompts
- Material references for meeting presentations
- Material reusability across multiple bots

Future iterations may add:
- Form collection for registration/meeting access
- Meeting logs/transcripts
- Analytics and usage tracking
- Webhook integrations
- Enhanced credit/billing system
