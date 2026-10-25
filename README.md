# Podbean CLI

**🇬🇧 English** · [🇨🇿 Čeština](README.cs.md) · [🇪🇸 Español](i18n/README.es.md) · [🇧🇷 Português](i18n/README.pt-BR.md) · [🇩🇪 Deutsch](i18n/README.de.md) · [🇫🇷 Français](i18n/README.fr.md) · [🇨🇳 简体中文](i18n/README.zh-CN.md) · [🇯🇵 日本語](i18n/README.ja.md) · [🇸🇪 Svenska](i18n/README.sv.md) · [🇳🇴 Norsk](i18n/README.nb.md) · [🇩🇰 Dansk](i18n/README.da.md)

A Python CLI that uploads and manages podcast episodes through the [Podbean](https://www.podbean.com/) REST API. For podcasters who publish regularly or in several languages and don't want to click through the Podbean dashboard every time. Built to be driven by [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or another AI agent: you focus on making the show, the AI handles the admin.

Author: [Jindřich Fáborský](https://www.faborsky.com)

> [!TIP]
> **The app is free and it's yours.** Clone it, use it, rebuild it your way.
>
> Want to build tools like this for your own marketing? That's what I teach: **[faborsky.com](https://www.faborsky.com)**.

## Why it exists

Publishing a single podcast episode takes a surprising amount of repetitive work: upload the file, fill in the metadata, set the status, keep track of drafts. Multiply that by the number of shows and languages, and the time that should go into the show goes into clicking.

This CLI automates the Podbean side, so it can be chained with other tools into a complete podcast workflow:

1. **Record** the podcast
2. **Transcribe and translate** with [whisper-cz-en](https://github.com/faborsky/whisper-cz-en)
3. **Generate the cover art** with [nanobanana-app](https://github.com/faborsky/nanobanana-app)
4. **Upload and publish** with this CLI

Claude Code runs all of it in a single conversation.

## Requirements

- **Python 3.9+**
- **A Podbean account** with a podcast
- **Podbean API credentials** (client ID and secret)

### Getting Podbean API credentials

1. Go to the [Podbean Developer Portal](https://developers.podbean.com/)
2. Click **Register a New App**
3. Fill in the app details (name, contact email, logo)
4. Once approved, go to **My Apps** and click **Manage App**
5. Copy the **App ID** (client ID) and **App Secret** (client secret)

API documentation: [developers.podbean.com/podbean-api-docs](https://developers.podbean.com/podbean-api-docs/)

## Installation

```bash
git clone https://github.com/faborsky/podbean-app.git
cd podbean-app

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and add your Podbean credentials
```

## Configuration

Add your Podbean API credentials to `.env`:

```
PODBEAN_CLIENT_ID=your-client-id-here
PODBEAN_CLIENT_SECRET=your-client-secret-here
```

The CLI manages OAuth tokens by itself (it caches them in `.token_cache.json`).

## Usage

Always activate the virtual environment first:

```bash
source venv/bin/activate
```

### List podcasts

Run this first. It fills the local cache of podcast slugs:

```bash
python podbean_cli.py podcasts
python podbean_cli.py podcasts --json
```

### List episodes

```bash
python podbean_cli.py episodes --podcast my-podcast
python podbean_cli.py episodes --podcast my-podcast --limit 50 --offset 0
python podbean_cli.py episodes --json
```

### Episode details

```bash
python podbean_cli.py episode-get --episode-id EPISODE_ID
python podbean_cli.py episode-get --episode-id EPISODE_ID --json
```

### Upload and create an episode

Three steps: authorize the upload, upload to S3, create the episode. To be safe, the episode is created as a **draft**.

```bash
# create a draft (default, safe)
python podbean_cli.py upload \
  --file /path/to/episode.mp3 \
  --title "Episode Title" \
  --description "<p>Episode description in HTML</p>" \
  --podcast my-podcast

# create and publish right away
python podbean_cli.py upload \
  --file /path/to/episode.mp3 \
  --title "Episode Title" \
  --podcast my-podcast \
  --status publish

# with an episode type for Apple Podcasts
python podbean_cli.py upload \
  --file /path/to/episode.mp3 \
  --title "Episode Title" \
  --podcast my-podcast \
  --apple-episode-type full
```

### Update an episode

```bash
python podbean_cli.py episode-update --episode-id EPISODE_ID --title "New Title"
python podbean_cli.py episode-update --episode-id EPISODE_ID --status publish
python podbean_cli.py episode-update --episode-id EPISODE_ID --description "<p>Updated</p>"
```

### Custom cover art for a single episode

Uploads a local image and sets it as the episode's artwork, which is separate from the
show's logo. Apple wants a square JPG/PNG, 1400–3000 px. The episode's title and status
stay unchanged.

```bash
python podbean_cli.py episode-set-logo --episode-id EPISODE_ID --image /path/to/cover.jpg --podcast my-podcast
```

### Delete an episode

For safety, this requires the `--confirm` flag:

```bash
python podbean_cli.py episode-delete --episode-id EPISODE_ID --confirm
```

### JSON output

Every command supports `--json` for machine-readable output. Useful when an AI agent orchestrates the commands:

```bash
python podbean_cli.py episodes --podcast my-podcast --json
```

## Bilingual workflow (CZ/EN)

A typical run of a bilingual podcast, driven by Claude Code:

```
1. Record the episode (CZ or EN)
2. Transcribe with whisper-cz-en → .md transcript
3. Translate the transcript (CZ↔EN) in Claude
4. Write episode descriptions in both languages
5. Cover art with nanobanana-app
6. Upload the CZ version → podbean-app (draft)
7. Upload the EN version → podbean-app (draft)
8. Review the drafts and publish
```

Each step can be its own Claude Code skill.

## Automation chain

This CLI is the last step of a podcast pipeline run by AI:

| Step | Tool | What it does |
|------|------|-------------|
| Transcription | [whisper-cz-en](https://github.com/faborsky/whisper-cz-en) | Local transcription with Whisper Large V3 (CZ/EN) |
| Translation | Claude Code | Translates transcripts between Czech and English |
| Show notes | Claude Code | Descriptions, titles and summaries |
| Cover art | [nanobanana-app](https://github.com/faborsky/nanobanana-app) | AI-generated episode artwork |
| Publishing | **podbean-app** (this repo) | Audio upload, episode creation, metadata management |

## Project structure

```
podbean_cli.py        # main CLI (single file)
.env.example          # template for API credentials
.env                  # your credentials (not in git)
.token_cache.json     # cached OAuth token (auto-generated, not in git)
.podcast_cache.json   # slug → podcast_id mapping (auto-generated, not in git)
requirements.txt      # Python dependencies
CLAUDE.md             # instructions for Claude Code
```

---

## License

MIT, see [LICENSE](LICENSE).

## Author

[Jindřich Fáborský](https://www.faborsky.com), marketer and educator from Prague. I teach marketers to build their own tools with AI.

Podbean CLI started as part of my podcast automation toolkit and runs in production, managing several Czech podcasts.
