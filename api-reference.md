# Podbean API Quick Reference

Base URL: `https://api.podbean.com/v1`
Auth: OAuth via `multiplePodcastsToken` — returns per-podcast access tokens
POST body: form-encoded (`data=`), NOT JSON (`json=`)

## Authentication

### Single podcast (default)
```
POST /oauth/token
Auth: HTTP Basic (client_id:client_secret)
Body: grant_type=client_credentials
      podcast_id=ID (optional, defaults to primary podcast)
```

### Multiple podcasts (required for multi-podcast accounts)
```
POST /oauth/multiplePodcastsToken
Auth: HTTP Basic (client_id:client_secret)
Body: grant_type=client_credentials
```

Response:
```json
{
  "access_token": "ACCOUNT_TOKEN",
  "token_type": "Bearer",
  "expires_in": 604800,
  "scope": "podcast_read episode_read podcast_update episode_publish private_members",
  "podcasts": [{
    "access_token": "PODCAST_SPECIFIC_TOKEN",
    "expires_in": 604800,
    "token_type": "Bearer",
    "scope": "...",
    "title": "TITLE",
    "link": "LINK",
    "podcast_id": "PODCAST_ID"
  }]
}
```

**Important**: The access_token determines which podcast's data is returned.
The `/episodes` endpoint does NOT accept a `podcast_id` query param for filtering.

## Podcasts

```
GET /podcasts?access_token=TOKEN&offset=0&limit=100
```

Response: `{ podcasts: [{ id, title, desc, logo, website }] }`

## Episodes

### List episodes (token determines podcast)
```
GET /episodes?access_token=PODCAST_TOKEN&offset=0&limit=20
```

### Get single episode
```
GET /episodes/{episode_id}?access_token=TOKEN
```

### Create episode
```
POST /episodes
  access_token=PODCAST_TOKEN
  title=...
  content=...           # HTML description
  media_key=...         # from upload authorize
  status=draft|publish
  type=public|premium|private
  apple_episode_type=full|trailer|bonus
```

### Update episode
```
POST /episodes/{episode_id}
  access_token=TOKEN
  title=...
  content=...
  status=draft|publish
```

### Delete episode
```
POST /episodes/{episode_id}/delete
  access_token=TOKEN
  delete_media_file=yes|no (default: no)
```

## File Upload (3-step)

### Step 1: Authorize

```
GET /files/uploadAuthorize?access_token=TOKEN&filename=X&content_type=audio/mpeg&filesize=N
```

Response: `{ presigned_url, file_key, expire_at }`

### Step 2: Upload to presigned URL

```
PUT {presigned_url}
Content-Type: audio/mpeg
Body: raw file bytes
```

### Step 3: Create episode (see POST /episodes above)

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad request |
| 401 | Invalid/expired token |
| 403 | Insufficient permissions |
| 404 | Not found |
| 429 | Rate limited |
| 500 | Server error |

## Key Gotchas

- Token goes as `access_token` parameter, NOT `Authorization: Bearer` header
- POST body uses form-encoded (`data=`), not JSON
- **Token determines podcast** — `/episodes` does NOT filter by `podcast_id` param
- Use `multiplePodcastsToken` for accounts with multiple podcasts
- Episode update is `POST /episodes/{id}`, NOT `PUT /episodes`
- Episode delete is `POST /episodes/{id}/delete`, NOT `DELETE /episodes`
- Upload is 3-step: authorize → PUT to S3 → create episode
- `file_key` from authorize is used as `media_key` in episode creation
- API rate limit: 60-request bucket, refills 2/second
