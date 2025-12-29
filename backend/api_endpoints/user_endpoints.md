# User API Endpoints

## Base Route
All user endpoints are prefixed with: `/api/v1/user`

## Authentication & Account Management

---

### POST /api/v1/user/signup

**Purpose:** Creates a new user account and returns authentication tokens.

**Authentication:** None (public endpoint)

**Request:**
- Method: `POST`
- Content-Type: `application/json`
- Body:
  ```json
  {
    "username": "string (required)",
    "email": "string (required)",
    "password": "string (required)"
  }
  ```

**Responses:**

**201 Created** - User successfully created
```json
{
  "message": "Signup successful",
  "userId": "string (MongoDB ObjectId)"
}
```
- JWT tokens set in cookies (see JWT Configuration below)

**400 Bad Request** - Invalid input or validation failed
```json
{
  "message": "Invalid email format"
}
```

**409 Conflict** - Username or email already exists
```json
{
  "message": "User already exists with this email"
}
```
OR
```json
{
  "message": "User already exists with this username"
}
```

**500 Internal Server Error** - Server/database error
```json
{
  "message": "Internal server error"
}
```

**Business Logic:**

1. **Input Normalization:**
   - Convert `username` and `email` to lowercase before any processing
   - Store normalized values in database
   - Use normalized values for uniqueness checks

2. **Validation:**
   - Validate email format (use email validator)
   - Validate password requirements (use appropriate Python validation library)
   - All fields are required

3. **Uniqueness Check:**
   - Check if user exists with the provided email (case-insensitive)
   - Check if user exists with the provided username (case-insensitive)
   - If either exists, reject with 409 status

4. **Password Hashing:**
   - Use bcrypt (passlib library) for password hashing
   - Use 12 rounds for hashing
   - Helper functions for password operations are documented in root `agents.md`
   - NEVER store plaintext passwords

5. **JWT Token Creation:**
   - Use python-jose (or similar JWT library) to create tokens
   - Create access token with 1 day expiration
   - Create refresh token with 10 days expiration
   - JWT payload structure and helper functions are documented in root `agents.md`
   - Set both tokens as HTTP-only cookies (cookie names: `access_token`, `refresh_token`)

6. **Database Operations:**
   - Create new User document with normalized username/email
   - Initialize `created_bots` as empty array
   - Initialize `credit_id` as None
   - Store hashed password

7. **Response:**
   - Return `userId` (user._id as string) in camelCase
   - Return success message
   - Tokens automatically sent via cookies

**Helper Functions:**
- Helper functions for password hashing, JWT generation, etc. are documented in root `agents.md`
- Coding agents should reference root `agents.md` for available helper functions in `/backend/src/helpers/`
- Helpers should be modular and reusable across endpoints

**Error Handling:**
- Ensure proper error handling for all database operations
- Use try-except blocks for database queries
- Return appropriate status codes with clear messages
- Log errors but don't expose internal details to client

---

### POST /api/v1/user/signin

**Purpose:** Authenticates a user and returns authentication tokens.

**Authentication:** None (public endpoint)

**Request:**
- Method: `POST`
- Content-Type: `application/json`
- Body:
  ```json
  {
    "username": "string (optional, provide username OR email)",
    "email": "string (optional, provide username OR email)",
    "password": "string (required)"
  }
  ```
  **Note:** Either `username` OR `email` must be provided (not both required, but at least one)

**Responses:**

**200 OK** - Sign-in successful
```json
{
  "message": "Sign-in successful",
  "userId": "string (MongoDB ObjectId)"
}
```
- JWT tokens set in cookies (see JWT Configuration below)

**400 Bad Request** - Invalid credentials (incorrect password)
```json
{
  "message": "Incorrect password"
}
```

**404 Not Found** - User does not exist with provided username/email
```json
{
  "message": "User not found with this username"
}
```
OR
```json
{
  "message": "User not found with this email"
}
```

**500 Internal Server Error** - Server/database error
```json
{
  "message": "Internal server error"
}
```

**Business Logic:**

1. **Input Validation:**
   - Validate that either `username` OR `email` is provided (at least one required)
   - Validate `password` field is provided
   - Use Pydantic models for request validation

2. **User Lookup:**
   - Normalize input (convert to lowercase)
   - Query User collection based on whichever field was provided (username or email)
   - Check if user exists

3. **Password Verification:**
   - Fetch user's hashed password from database
   - Use bcrypt (passlib) to compare provided password with stored hash
   - Helper functions for password operations are documented in root `agents.md`

4. **Authentication Flow:**
   - If user not found: Return 404 with specific message (username vs email)
   - If password doesn't match: Return 400 with "Incorrect password" message
   - If password matches: Proceed to token generation

5. **JWT Token Creation:**
   - Use python-jose (or similar JWT library) to create tokens
   - Create access token with 1 day expiration
   - Create refresh token with 10 days expiration
   - JWT payload structure and helper functions are documented in root `agents.md`
   - Decode JWT payload when needed to extract userId, email, username
   - Set both tokens as HTTP-only cookies (cookie names: `access_token`, `refresh_token`)

6. **Response:**
   - Return `userId` (user._id as string) in camelCase
   - Return success message
   - Tokens automatically sent via cookies

**Helper Functions:**
- Use or create helper for password hash comparison in `/backend/src/helpers/`
- Reuse JWT token generation helper from signup
- Helper functions and their usage are documented in root `agents.md`
- Consider creating a user lookup helper (by email or username)

**Error Handling:**
- Ensure proper error handling for all database operations
- Handle cases where user exists but password is incorrect separately
- Handle cases where user doesn't exist
- Use try-except blocks for database queries
- Return appropriate status codes with clear messages

---

## JWT Configuration

**Token Types:**
- **Access Token:** 1 day expiration
- **Refresh Token:** 10 days expiration

**Cookie Names:**
- `access_token` - for access token
- `refresh_token` - for refresh token

**Cookie Settings:**
- HTTP-only cookies (prevent XSS attacks)
- Secure flag in production (HTTPS only)
- SameSite attribute for CSRF protection
- Appropriate path and domain settings

**Token Payload:**
The JWT payload structure is defined in the root `agents.md` file. When decoding JWT tokens in middleware or route handlers, you can extract userId, email, and username from the payload. Refer to root `agents.md` for exact payload schema.

**Libraries:**
- Use `python-jose` (or equivalent) for JWT operations
- Use `passlib` with bcrypt for password hashing

**Storage:**
- Both tokens are set as cookies in the response
- Client automatically sends cookies with subsequent requests
- Backend middleware will validate tokens for protected endpoints

---

## Notes for AI Coding Agents

**File Organization:**
- This file documents user-related endpoints only
- For bot endpoints, see `bot_endpoints.md`
- For material endpoints (image/video/ppt), see `material_endpoints.md`

**Helper Functions:**
- Helper functions are located in `/backend/src/helpers/`
- Available helper functions and their usage are documented in root `agents.md`
- Examples may include: `hash_password()`, `verify_password()`, `generate_jwt()`, `decode_jwt()`, `validate_email()`
- Always refer to root `agents.md` for complete helper function documentation

**Database Reference:**
- User schema is defined in `../db_schema.md`
- Use Beanie ODM for all database operations
- All database fields use snake_case in MongoDB, camelCase in API responses

**Security Priorities:**
1. Never store plaintext passwords
2. Always use bcrypt (passlib) for password hashing (12 rounds)
3. Set JWT tokens as HTTP-only cookies
4. Perform case-insensitive checks for username/email
5. Use python-jose for JWT operations
6. Return informative error messages to help users understand issues

**Code Quality:**
- Use Pydantic models for request/response validation
- Implement proper error handling with try-except
- Log errors appropriately
- Keep route handlers clean by using helper functions
- Follow FastAPI best practices
