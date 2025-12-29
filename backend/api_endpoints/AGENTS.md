## JWT Payload Structure

Throughout the backend of this project, JWTs (JSON Web Tokens) are used for authenticating and authorizing API requests. The payload structure for the JWT is as follows:

```json
{
    "userId": "<str>",     // The `_id` of the user from the MongoDB database (as a string)
    "email": "<str>",      // The email address of the user
    "username": "<str>"    // The username of the user
}
```

- **userId**: The unique identifier of the user in the database. This should be the value of the `_id` field from the MongoDB user document.
- **email**: The user's email address, as stored in the user collection.
- **username**: The user's display or login name.

## Instruction

**AI coding agents must use this JWT payload structure in the backend throughout the project.** All API endpoints, authentication middleware, and any backend feature that encodes or decodes JWTs should adhere strictly to this structure. This ensures consistent user identification and access control.

For v0, no additional fields are included in the JWT payload beyond `userId`, `email`, and `username`.


