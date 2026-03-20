#!/usr/bin/env python3
"""Podbean CLI — manage podcasts, episodes, uploads, and stats.

SAFETY: Episodes are created as DRAFT by default.
Delete requires --confirm flag.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

CLIENT_ID = os.getenv("PODBEAN_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("PODBEAN_CLIENT_SECRET", "")
API_BASE = "https://api.podbean.com/v1"
TOKEN_CACHE = os.path.join(BASE_DIR, ".token_cache.json")
PODCAST_CACHE = os.path.join(BASE_DIR, ".podcast_cache.json")


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

def _check_config() -> None:
    if not CLIENT_ID or CLIENT_ID == "your-client-id-here":
        print("ERROR: PODBEAN_CLIENT_ID not set. Copy .env.example to .env and add your credentials.", file=sys.stderr)
        sys.exit(1)
    if not CLIENT_SECRET or CLIENT_SECRET == "your-client-secret-here":
        print("ERROR: PODBEAN_CLIENT_SECRET not set.", file=sys.stderr)
        sys.exit(1)


def _load_token_cache() -> dict:
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE, "r") as f:
            cache = json.load(f)
        # Migrate old single-token cache format
        if "default" not in cache and "access_token" in cache:
            return {}
        return cache
    return {}


def _save_token_cache(cache: dict) -> None:
    with open(TOKEN_CACHE, "w") as f:
        json.dump(cache, f, indent=2)


def _refresh_tokens() -> dict:
    """Fetch tokens for all podcasts via multiplePodcastsToken endpoint."""
    resp = requests.post(
        f"{API_BASE}/oauth/multiplePodcastsToken",
        auth=(CLIENT_ID, CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"ERROR: OAuth multiplePodcastsToken failed ({resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)

    token_data = resp.json()
    now = time.time()

    cache: dict = {
        "default": {
            "access_token": token_data["access_token"],
            "expires_at": now + token_data.get("expires_in", 3600),
        },
        "podcasts": {},
    }

    for pod in token_data.get("podcasts", []):
        pid = pod["podcast_id"]
        cache["podcasts"][pid] = {
            "access_token": pod["access_token"],
            "expires_at": now + pod.get("expires_in", 3600),
            "title": pod.get("title", ""),
        }

    _save_token_cache(cache)
    return cache


def _get_access_token(podcast_id: str | None = None) -> str:
    """Get OAuth access token. If podcast_id given, return podcast-specific token."""
    cache = _load_token_cache()

    if podcast_id and cache.get("podcasts", {}).get(podcast_id):
        entry = cache["podcasts"][podcast_id]
        if entry.get("expires_at", 0) > time.time() + 60:
            return entry["access_token"]
    elif not podcast_id and cache.get("default"):
        entry = cache["default"]
        if entry.get("expires_at", 0) > time.time() + 60:
            return entry["access_token"]

    # Refresh all tokens
    cache = _refresh_tokens()

    if podcast_id:
        pod_entry = cache.get("podcasts", {}).get(podcast_id)
        if not pod_entry:
            print(f"ERROR: No token returned for podcast_id '{podcast_id}'. Check your credentials.", file=sys.stderr)
            sys.exit(1)
        return pod_entry["access_token"]

    return cache["default"]["access_token"]


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def _api_get(endpoint: str, params: dict | None = None, podcast_id: str | None = None) -> dict:
    """GET request with access_token as query parameter."""
    token = _get_access_token(podcast_id)
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    p = dict(params or {})
    p["access_token"] = token
    resp = requests.get(url, params=p, timeout=30)
    if resp.status_code != 200:
        print(f"ERROR: GET {endpoint} returned {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)
    return resp.json()


def _api_post(endpoint: str, data: dict | None = None, podcast_id: str | None = None) -> dict:
    """POST request with access_token in form data."""
    token = _get_access_token(podcast_id)
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    d = dict(data or {})
    d["access_token"] = token
    resp = requests.post(url, data=d, timeout=30)
    if resp.status_code not in (200, 201, 204):
        print(f"ERROR: POST {endpoint} returned {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)
    if resp.status_code == 204:
        return {}
    return resp.json()


def _api_put(endpoint: str, data: dict | None = None, podcast_id: str | None = None) -> dict:
    """PUT request with access_token in form data."""
    token = _get_access_token(podcast_id)
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    d = dict(data or {})
    d["access_token"] = token
    resp = requests.put(url, data=d, timeout=30)
    if resp.status_code not in (200, 201, 204):
        print(f"ERROR: PUT {endpoint} returned {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)
    if resp.status_code == 204:
        return {}
    return resp.json()


def _api_delete(endpoint: str, data: dict | None = None, podcast_id: str | None = None) -> dict:
    """DELETE request with access_token in form data."""
    token = _get_access_token(podcast_id)
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    d = dict(data or {})
    d["access_token"] = token
    resp = requests.delete(url, data=d, timeout=30)
    if resp.status_code not in (200, 204):
        print(f"ERROR: DELETE {endpoint} returned {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)
    if resp.status_code == 204:
        return {}
    return resp.json()


# ---------------------------------------------------------------------------
# Podcast cache helpers
# ---------------------------------------------------------------------------

def _load_podcast_cache() -> dict[str, str]:
    if os.path.exists(PODCAST_CACHE):
        with open(PODCAST_CACHE, "r") as f:
            return json.load(f)
    return {}


def _save_podcast_cache(mapping: dict[str, str]) -> None:
    with open(PODCAST_CACHE, "w") as f:
        json.dump(mapping, f, indent=2)


def _resolve_podcast(slug: str) -> str:
    """Resolve podcast slug to podcast_id."""
    mapping = _load_podcast_cache()
    if slug in mapping:
        return mapping[slug]
    print(f"ERROR: Unknown podcast '{slug}'. Run 'podcasts' first to populate the mapping.", file=sys.stderr)
    print(f"  Available: {', '.join(mapping.keys()) if mapping else '(none cached)'}", file=sys.stderr)
    sys.exit(1)


def _slugify(name: str) -> str:
    """Generate a simple slug from podcast name."""
    return name.lower().replace(" ", "-").replace("_", "-")


# ---------------------------------------------------------------------------
# Commands — Read-only
# ---------------------------------------------------------------------------

def cmd_podcasts(args: argparse.Namespace) -> None:
    """List podcasts and cache slug mapping."""
    data = _api_get("/podcasts", {"offset": 0, "limit": 100})
    podcasts = data.get("podcasts", [])

    if not podcasts:
        print("No podcasts found.")
        return

    slug_map: dict[str, str] = {}
    for pod in podcasts:
        slug = _slugify(pod.get("title", ""))
        slug_map[slug] = pod["id"]

    _save_podcast_cache(slug_map)

    if args.json:
        output = []
        for pod in podcasts:
            slug = next((s for s, pid in slug_map.items() if pid == pod["id"]), "")
            output.append({
                "podcast_id": pod["id"],
                "title": pod.get("title", ""),
                "slug": slug,
                "description": pod.get("desc", ""),
                "logo": pod.get("logo", ""),
                "website": pod.get("website", ""),
            })
        print(json.dumps(output, indent=2))
    else:
        print(f"{'Title':<40} {'Slug':<30} {'Podcast ID'}")
        print("-" * 90)
        for pod in podcasts:
            slug = next((s for s, pid in slug_map.items() if pid == pod["id"]), "?")
            print(f"{pod.get('title', ''):<40} {slug:<30} {pod['id']}")

    print(f"\nPodcast map cached ({len(slug_map)} entries).")


def cmd_episodes(args: argparse.Namespace) -> None:
    """List episodes for a podcast."""
    podcast_id = _resolve_podcast(args.podcast) if args.podcast else None

    params: dict[str, str | int] = {
        "offset": args.offset,
        "limit": args.limit,
    }

    data = _api_get("/episodes", params, podcast_id=podcast_id)
    episodes = data.get("episodes", [])

    if not episodes:
        print("No episodes found.")
        return

    if args.json:
        output = []
        for ep in episodes:
            output.append({
                "id": ep.get("id", ""),
                "title": ep.get("title", ""),
                "status": ep.get("status", ""),
                "publish_time": ep.get("publish_time", ""),
                "duration": ep.get("duration", ""),
                "permalink_url": ep.get("permalink_url", ""),
            })
        print(json.dumps(output, indent=2))
    else:
        print(f"{'Title':<50} {'Status':<10} {'Published':<20} {'ID'}")
        print("-" * 110)
        for ep in episodes:
            pub_time = ep.get("publish_time", "")
            if pub_time:
                try:
                    if isinstance(pub_time, (int, float)):
                        dt = datetime.fromtimestamp(pub_time)
                    else:
                        dt = datetime.fromisoformat(str(pub_time).replace("Z", "+00:00"))
                    pub_time = dt.strftime("%Y-%m-%d %H:%M")
                except (ValueError, TypeError, OSError):
                    pub_time = str(pub_time)
            title = ep.get("title", "")
            if len(title) > 48:
                title = title[:46] + ".."
            print(f"{title:<50} {ep.get('status', ''):<10} {pub_time:<20} {ep.get('id', '')}")

    count = data.get("count", len(episodes))
    print(f"\nShowing {len(episodes)} of {count} episodes (offset={args.offset}).")


def cmd_episode_get(args: argparse.Namespace) -> None:
    """Get detail of a single episode."""
    podcast_id = _resolve_podcast(args.podcast) if args.podcast else None
    data = _api_get(f"/episodes/{args.episode_id}", podcast_id=podcast_id)
    ep = data.get("episode", data)

    if args.json:
        print(json.dumps(ep, indent=2))
    else:
        print(f"Title:       {ep.get('title', '')}")
        print(f"ID:          {ep.get('id', '')}")
        print(f"Status:      {ep.get('status', '')}")
        print(f"Published:   {ep.get('publish_time', '')}")
        print(f"Duration:    {ep.get('duration', '')}s")
        print(f"Type:        {ep.get('type', '')}")
        print(f"Permalink:   {ep.get('permalink_url', '')}")
        print(f"Media URL:   {ep.get('media_url', '')}")
        content = ep.get("content", "")
        if content:
            if len(content) > 200:
                content = content[:200] + "..."
            print(f"Description: {content}")


# ---------------------------------------------------------------------------
# Commands — Write
# ---------------------------------------------------------------------------

def cmd_upload(args: argparse.Namespace) -> None:
    """Upload audio file and create episode (3-step process)."""
    filepath = os.path.expanduser(args.file)
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    file_size = os.path.getsize(filepath)
    filename = os.path.basename(filepath)

    # Detect content type
    ext = os.path.splitext(filename)[1].lower()
    content_types = {
        ".mp3": "audio/mpeg",
        ".m4a": "audio/mp4",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
        ".flac": "audio/flac",
        ".mp4": "video/mp4",
    }
    content_type = content_types.get(ext, "audio/mpeg")

    podcast_id = _resolve_podcast(args.podcast) if args.podcast else None

    # Step 1: Authorize upload
    print(f"Step 1/3: Authorizing upload for {filename} ({file_size} bytes)...")
    auth_data = _api_get("/files/uploadAuthorize", {
        "filename": filename,
        "content_type": content_type,
        "filesize": file_size,
    }, podcast_id=podcast_id)

    presigned_url = auth_data.get("presigned_url", "")
    file_key = auth_data.get("file_key", "")

    if not presigned_url or not file_key:
        print(f"ERROR: Upload authorization failed. Response: {json.dumps(auth_data)}", file=sys.stderr)
        sys.exit(1)

    print(f"  File key: {file_key}")

    # Step 2: Upload to presigned URL (S3)
    print(f"Step 2/3: Uploading to storage...")
    with open(filepath, "rb") as f:
        upload_resp = requests.put(
            presigned_url,
            data=f,
            headers={"Content-Type": content_type},
            timeout=600,
        )

    if upload_resp.status_code not in (200, 201):
        print(f"ERROR: Upload failed ({upload_resp.status_code}): {upload_resp.text}", file=sys.stderr)
        sys.exit(1)

    print("  Upload complete.")

    # Step 3: Create episode
    print(f"Step 3/3: Creating episode...")
    episode_data: dict[str, str] = {
        "title": args.title,
        "content": args.description or "",
        "status": args.status,
        "type": args.type,
        "media_key": file_key,
    }

    if args.apple_episode_type:
        episode_data["apple_episode_type"] = args.apple_episode_type

    result = _api_post("/episodes", episode_data, podcast_id=podcast_id)
    ep = result.get("episode", result)

    output = {
        "episode_id": ep.get("id", ""),
        "title": ep.get("title", args.title),
        "status": ep.get("status", args.status),
        "permalink_url": ep.get("permalink_url", ""),
        "media_url": ep.get("media_url", ""),
        "file_key": file_key,
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"\nEpisode created successfully.")
        print(f"  Episode ID: {output['episode_id']}")
        print(f"  Title:      {output['title']}")
        print(f"  Status:     {output['status']}")
        print(f"  Permalink:  {output['permalink_url']}")


def cmd_episode_update(args: argparse.Namespace) -> None:
    """Update episode metadata."""
    podcast_id = _resolve_podcast(args.podcast) if args.podcast else None
    data: dict[str, str] = {}

    if args.title:
        data["title"] = args.title
    if args.description:
        data["content"] = args.description
    if args.status:
        data["status"] = args.status
    if args.apple_episode_type:
        data["apple_episode_type"] = args.apple_episode_type

    if not data:
        print("ERROR: No fields to update. Use --title, --description, --status, or --apple-episode-type.", file=sys.stderr)
        sys.exit(1)

    result = _api_post(f"/episodes/{args.episode_id}", data, podcast_id=podcast_id)
    ep = result.get("episode", result)

    output = {
        "episode_id": ep.get("id", args.episode_id),
        "title": ep.get("title", ""),
        "status": ep.get("status", ""),
        "updated": True,
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"Episode updated successfully.")
        print(f"  Episode ID: {output['episode_id']}")
        if args.title:
            print(f"  Title:      {output['title']}")
        if args.status:
            print(f"  Status:     {output['status']}")


def cmd_episode_delete(args: argparse.Namespace) -> None:
    """Delete an episode (requires --confirm)."""
    if not args.confirm:
        print("ERROR: Delete requires --confirm flag for safety.", file=sys.stderr)
        print("  Usage: episode-delete --episode-id ID --confirm", file=sys.stderr)
        sys.exit(1)

    podcast_id = _resolve_podcast(args.podcast) if args.podcast else None
    _api_post(f"/episodes/{args.episode_id}/delete", podcast_id=podcast_id)

    output = {
        "episode_id": args.episode_id,
        "deleted": True,
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"Episode deleted successfully.")
        print(f"  Episode ID: {args.episode_id}")


# ---------------------------------------------------------------------------
# CLI setup
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Podbean CLI — manage podcasts, episodes, uploads, and stats.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    json_kwargs = {"action": "store_true", "help": "Output as JSON"}

    # --- podcasts ---
    p_podcasts = subparsers.add_parser("podcasts", help="List podcasts and cache slug mapping")
    p_podcasts.add_argument("--json", **json_kwargs)

    # --- episodes ---
    p_episodes = subparsers.add_parser("episodes", help="List episodes")
    p_episodes.add_argument("--podcast", type=str, help="Podcast slug")
    p_episodes.add_argument("--offset", type=int, default=0, help="Offset (default: 0)")
    p_episodes.add_argument("--limit", type=int, default=20, help="Limit (default: 20)")
    p_episodes.add_argument("--json", **json_kwargs)

    # --- episode-get ---
    p_ep_get = subparsers.add_parser("episode-get", help="Get episode detail")
    p_ep_get.add_argument("--episode-id", required=True, help="Episode ID")
    p_ep_get.add_argument("--podcast", type=str, help="Podcast slug (for multi-podcast accounts)")
    p_ep_get.add_argument("--json", **json_kwargs)

    # --- upload ---
    p_upload = subparsers.add_parser("upload", help="Upload audio and create episode")
    p_upload.add_argument("--file", required=True, help="Path to audio file")
    p_upload.add_argument("--title", required=True, help="Episode title")
    p_upload.add_argument("--description", type=str, default="", help="Episode description (HTML)")
    p_upload.add_argument("--podcast", type=str, help="Podcast slug")
    p_upload.add_argument("--status", type=str, default="draft", choices=["draft", "publish"], help="Episode status (default: draft)")
    p_upload.add_argument("--type", type=str, default="public", choices=["public", "premium", "private"], help="Episode type (default: public)")
    p_upload.add_argument("--apple-episode-type", type=str, choices=["full", "trailer", "bonus"], help="Apple episode type")
    p_upload.add_argument("--json", **json_kwargs)

    # --- episode-update ---
    p_ep_update = subparsers.add_parser("episode-update", help="Update episode metadata")
    p_ep_update.add_argument("--episode-id", required=True, help="Episode ID")
    p_ep_update.add_argument("--podcast", type=str, help="Podcast slug (for multi-podcast accounts)")
    p_ep_update.add_argument("--title", type=str, help="New title")
    p_ep_update.add_argument("--description", type=str, help="New description (HTML)")
    p_ep_update.add_argument("--status", type=str, choices=["draft", "publish"], help="New status")
    p_ep_update.add_argument("--apple-episode-type", type=str, choices=["full", "trailer", "bonus"], help="Apple episode type")
    p_ep_update.add_argument("--json", **json_kwargs)

    # --- episode-delete ---
    p_ep_delete = subparsers.add_parser("episode-delete", help="Delete an episode")
    p_ep_delete.add_argument("--episode-id", required=True, help="Episode ID")
    p_ep_delete.add_argument("--podcast", type=str, help="Podcast slug (for multi-podcast accounts)")
    p_ep_delete.add_argument("--confirm", action="store_true", help="Required to confirm deletion")
    p_ep_delete.add_argument("--json", **json_kwargs)

    args = parser.parse_args()
    _check_config()

    commands = {
        "podcasts": cmd_podcasts,
        "episodes": cmd_episodes,
        "episode-get": cmd_episode_get,
        "upload": cmd_upload,
        "episode-update": cmd_episode_update,
        "episode-delete": cmd_episode_delete,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
