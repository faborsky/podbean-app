# Podbean CLI

Python CLI for managing Podbean podcasts via their REST API.

## Quick Start

```bash
source venv/bin/activate && python podbean_cli.py <command>
```

## Structure

```
podbean_cli.py           # Main CLI (single file)
.env                     # PODBEAN_CLIENT_ID, PODBEAN_CLIENT_SECRET
.token_cache.json        # Cached per-podcast OAuth tokens (auto-generated)
.podcast_cache.json      # Slug → podcast_id mapping (auto-generated)
```

## Commands

| Command | Purpose | Key Flags |
|---------|---------|-----------|
| `podcasts` | List podcasts, cache slug mapping (run first!) | `--json` |
| `episodes` | List episodes | `--podcast SLUG`, `--offset`, `--limit`, `--json` |
| `episode-get` | Get episode detail | `--episode-id ID`, `--podcast SLUG`, `--json` |
| `upload` | Upload audio + create episode (3-step) | `--file`, `--title`, `--podcast SLUG`, `--status draft\|publish`, `--json` |
| `episode-update` | Update episode metadata | `--episode-id ID`, `--podcast SLUG`, `--title`, `--status`, `--description`, `--json` |
| `episode-delete` | Delete episode | `--episode-id ID`, `--podcast SLUG`, `--confirm` (required) |

## Safety

- Episodes are created as **draft** by default.
- Delete requires `--confirm` flag.
- Credentials are in `.env` (never commit this file).

## API Notes

- Base URL: `https://api.podbean.com/v1`
- Auth: OAuth via `/oauth/multiplePodcastsToken` — returns per-podcast tokens
- Token determines which podcast's data is returned (NOT a `podcast_id` query param)
- POST body: form-encoded (`data=`), NOT JSON
- Episode update: `POST /episodes/{id}` (not PUT)
- Episode delete: `POST /episodes/{id}/delete` (not DELETE)
- Upload flow: authorize → PUT to S3 presigned URL → POST /episodes with `media_key`

## Conventions

- All commands support `--json` for machine-readable output.
- Use podcast slugs (e.g., `my-podcast`) not raw IDs. Run `podcasts` first to populate the slug cache.
- The CLI exits with code 1 on errors and prints to stderr.
