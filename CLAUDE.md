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
| `episode-set-logo` | Set per-episode logo/artwork from a local image | `--episode-id ID`, `--image PATH`, `--podcast SLUG`, `--json` |
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
- Per-episode logo: same upload flow with an image `content_type`, then `logo_key` on the episode. `episode-set-logo` does this in one command.
- **Update endpoint validates the whole episode**: a partial POST /episodes/{id} fails ("Episode type is invalid" / "Post Title cannot be blank") unless a valid `type` and non-blank `title` are resent. `episode-set-logo` re-fetches the episode and resends its current title+type alongside `logo_key`.

## Conventions

- All commands support `--json` for machine-readable output.
- Use podcast slugs (e.g., `my-podcast`) not raw IDs. Run `podcasts` first to populate the slug cache.
- The CLI exits with code 1 on errors and prints to stderr.

## Changelog

- **2026-07-17** — Added `episode-set-logo` (per-episode artwork from a local image via `logo_key`). Extracted a shared `_authorize_and_upload` helper reused by `upload` and the new command. Documented the update-endpoint gotcha (a logo-only edit must resend the episode's current `title` + `type`).
