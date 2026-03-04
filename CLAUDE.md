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
.token_cache.json        # Cached OAuth token (auto-generated)
.podcast_cache.json      # Slug → podcast_id mapping (auto-generated)
```

## Commands

| Command | Purpose | Key Flags |
|---------|---------|-----------|
| `podcasts` | List podcasts, cache slug mapping (run first!) | `--json` |
| `episodes` | List episodes | `--podcast SLUG`, `--offset`, `--limit`, `--json` |
| `episode-get` | Get episode detail | `--episode-id ID`, `--json` |
| `upload` | Upload audio + create episode (3-step) | `--file`, `--title`, `--podcast SLUG`, `--status draft\|publish`, `--json` |
| `episode-update` | Update episode metadata | `--episode-id ID`, `--title`, `--status`, `--description`, `--json` |
| `episode-delete` | Delete episode | `--episode-id ID`, `--confirm` (required) |

## Safety

- Episodes are created as **draft** by default.
- Delete requires `--confirm` flag.
- Credentials are in `.env` (never commit this file).

## API Notes

- Base URL: `https://api.podbean.com/v1`
- Auth: OAuth Client Credentials — token passed as query/body param (NOT Bearer header)
- POST/PUT/DELETE: form-encoded (`data=`), NOT JSON
- Upload flow: authorize → PUT to S3 presigned URL → POST /episodes with `media_key`

## Conventions

- All commands support `--json` for machine-readable output.
- Use podcast slugs (e.g., `my-podcast`) not raw IDs. Run `podcasts` first to populate the slug cache.
- The CLI exits with code 1 on errors and prints to stderr.
