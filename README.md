# Podbean CLI

A Python command-line tool for managing [Podbean](https://www.podbean.com/) podcasts via their REST API. Built to be orchestrated by [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or any AI coding agent — so you can focus on creating content while AI handles the admin.

## Why This Exists

Publishing a podcast episode involves a surprising amount of repetitive work: uploading files, filling in metadata, setting statuses, managing drafts. Multiply that across multiple shows and languages, and you're spending creative energy on admin tasks.

This CLI automates Podbean operations so they can be chained with other tools into a full podcast workflow:

1. **Record** your podcast
2. **Transcribe & translate** with [whisper-cz-en](https://github.com/faborsky/whisper-cz-en)
3. **Generate cover art** with [nanobonana-agent](https://github.com/faborsky/nanobonana-agent-public)
4. **Upload & publish** with this CLI

All orchestrated by Claude Code in a single conversation. You talk, AI does the paperwork.

## Prerequisites

- **Python 3.9+**
- **Podbean account** with a podcast
- **Podbean API credentials** (client ID and secret)

### Getting Podbean API Credentials

1. Go to [Podbean Developer Portal](https://developers.podbean.com/)
2. Click **Register a New App**
3. Fill in your app details (name, contact email, logo)
4. Once approved, go to **My Apps** and click **Manage App**
5. Copy your **App ID** (client ID) and **App Secret** (client secret)

API documentation: [developers.podbean.com/podbean-api-docs](https://developers.podbean.com/podbean-api-docs/)

## Installation

```bash
git clone https://github.com/faborsky/podbean-app.git
cd podbean-app

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your Podbean credentials
```

## Configuration

Edit `.env` with your Podbean API credentials:

```
PODBEAN_CLIENT_ID=your-client-id-here
PODBEAN_CLIENT_SECRET=your-client-secret-here
```

The CLI handles OAuth token management automatically (cached in `.token_cache.json`).

## Usage

Always activate the virtual environment first:

```bash
source venv/bin/activate
```

### List Podcasts

Run this first to populate the local podcast slug cache:

```bash
python podbean_cli.py podcasts
python podbean_cli.py podcasts --json
```

### List Episodes

```bash
python podbean_cli.py episodes --podcast my-podcast
python podbean_cli.py episodes --podcast my-podcast --limit 50 --offset 0
python podbean_cli.py episodes --json
```

### Get Episode Detail

```bash
python podbean_cli.py episode-get --episode-id EPISODE_ID
python podbean_cli.py episode-get --episode-id EPISODE_ID --json
```

### Upload & Create Episode

Three-step process: authorize upload, upload to S3, create episode. Episodes are created as **draft** by default for safety.

```bash
# Create as draft (default, safe)
python podbean_cli.py upload \
  --file /path/to/episode.mp3 \
  --title "Episode Title" \
  --description "<p>Episode description in HTML</p>" \
  --podcast my-podcast

# Create and publish immediately
python podbean_cli.py upload \
  --file /path/to/episode.mp3 \
  --title "Episode Title" \
  --podcast my-podcast \
  --status publish

# With Apple Podcasts episode type
python podbean_cli.py upload \
  --file /path/to/episode.mp3 \
  --title "Episode Title" \
  --podcast my-podcast \
  --apple-episode-type full
```

### Update Episode

```bash
python podbean_cli.py episode-update --episode-id EPISODE_ID --title "New Title"
python podbean_cli.py episode-update --episode-id EPISODE_ID --status publish
python podbean_cli.py episode-update --episode-id EPISODE_ID --description "<p>Updated</p>"
```

### Delete Episode

Requires `--confirm` flag for safety:

```bash
python podbean_cli.py episode-delete --episode-id EPISODE_ID --confirm
```

### JSON Output

All commands support `--json` for machine-readable output, which is useful for AI agent orchestration:

```bash
python podbean_cli.py episodes --podcast my-podcast --json
```

## Multilingual Workflow (CZ/EN)

A typical bilingual podcast workflow orchestrated by Claude Code:

```
1. Record podcast episode (CZ or EN)
2. Transcribe with whisper-cz-en → .md transcript
3. Translate transcript (CZ↔EN) using Claude
4. Generate episode descriptions in both languages
5. Generate cover art with nanobonana-agent
6. Upload CZ version → podbean-app (draft)
7. Upload EN version → podbean-app (draft)
8. Review drafts, then publish
```

Each step can be a Claude Code skill, chained together in a single conversation.

## Automation Chain

This CLI is designed to work as part of a larger AI-powered podcast pipeline:

| Step | Tool | What It Does |
|------|------|-------------|
| Transcription | [whisper-cz-en](https://github.com/faborsky/whisper-cz-en) | Local transcription with Whisper Large V3 (CZ/EN) |
| Translation | Claude Code | Translate transcripts between CZ and EN |
| Show notes | Claude Code | Generate descriptions, titles, summaries |
| Cover art | [nanobonana-agent](https://github.com/faborsky/nanobonana-agent-public) | Generate episode artwork with AI |
| Publishing | **podbean-app** (this repo) | Upload audio, create episodes, manage metadata |

## Project Structure

```
podbean_cli.py        # Main CLI (single file)
.env.example          # Template for API credentials
.env                  # Your credentials (git-ignored)
.token_cache.json     # Cached OAuth token (auto-generated, git-ignored)
.podcast_cache.json   # Slug → podcast_id mapping (auto-generated, git-ignored)
requirements.txt      # Python dependencies
CLAUDE.md             # Instructions for Claude Code
```

## About

Built by [Jindrich Faborsky](https://github.com/faborsky) as part of the podcast automation toolkit. Used in production for managing multiple Czech podcasts.

This project is part of the curriculum for:
- **[Vibe Coding for Marketers](https://vibecodingformarketers.com)** — an international course teaching marketers to build tools with AI
- **[AI First](https://www.aifirst.cz)** — a Czech course on AI-first thinking for entrepreneurs and marketers

---

## Česky

### Co to je

CLI nástroj pro správu podcastů na Podbeanu přes jejich API. Navržený tak, aby ho mohl ovládat Claude Code nebo jiný AI agent — vy se věnujete tvorbě, AI udělá administrativu.

### Proč to existuje

Publikování podcastu zahrnuje spoustu opakující se práce: nahrávání souborů, vyplňování metadat, správa drafů. Tohle CLI to automatizuje a dá se řetězit s dalšími nástroji do kompletního podcastového workflow:

1. **Nahrát** podcast
2. **Přepsat a přeložit** přes [whisper-cz-en](https://github.com/faborsky/whisper-cz-en)
3. **Vygenerovat grafiku** přes [nanobonana-agent](https://github.com/faborsky/nanobonana-agent-public)
4. **Nahrát a publikovat** přes toto CLI

Vše orchestrované Claude Codem v jedné konverzaci.

### Instalace

```bash
git clone https://github.com/faborsky/podbean-app.git
cd podbean-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Upravte .env a vložte své Podbean credentials
```

Pro získání API přístupů jděte na [Podbean Developer Portal](https://developers.podbean.com/), zaregistrujte aplikaci a zkopírujte App ID a App Secret.

### Kde se to učí

- **[Vibe Coding for Marketers](https://vibecodingformarketers.com)** — mezinárodní kurz (EN), kde se marketéři učí stavět nástroje s AI
- **[AI First](https://www.aifirst.cz)** — český kurz o AI-first přístupu pro podnikatele a marketéry

---

## License

MIT
