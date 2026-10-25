# Podbean CLI

[🇬🇧 English](../README.md) · [🇨🇿 Čeština](../README.cs.md) · [🇪🇸 Español](README.es.md) · [🇧🇷 Português](README.pt-BR.md) · **🇩🇪 Deutsch** · [🇫🇷 Français](README.fr.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇯🇵 日本語](README.ja.md) · [🇸🇪 Svenska](README.sv.md) · [🇳🇴 Norsk](README.nb.md) · [🇩🇰 Dansk](README.da.md)

Python-CLI, das Podcast-Episoden über die REST-API von [Podbean](https://www.podbean.com/) hochlädt und verwaltet. Für Podcaster, die regelmäßig oder in mehreren Sprachen veröffentlichen und sich nicht jedes Mal durch das Podbean-Dashboard klicken wollen.

Schon eine einzige Episode bedeutet viel Routinearbeit: Datei hochladen, Metadaten ausfüllen, Status setzen, Entwürfe im Blick behalten. Das CLI ist dafür gebaut, dass [Claude Code](https://docs.anthropic.com/en/docs/claude-code) oder ein anderer KI-Agent es steuert: Du kümmerst dich um die Sendung, die KI um die Verwaltung.

Autor: [Jindřich Fáborský](https://www.faborsky.com)

## Was es kann

- `upload`: lädt das Audio hoch und legt die Episode an. Standardmäßig als Entwurf, mit `--status publish` direkt veröffentlicht.
- `episode-update`: ändert Titel, Beschreibung oder Status einer Episode.
- `episode-set-logo`: setzt ein eigenes Cover für eine einzelne Episode (quadratisches JPG/PNG, 1400–3000 px).
- `podcasts`, `episodes`, `episode-get`: listet deine Podcasts und Episoden. `episode-delete` löscht nur mit `--confirm`.
- Alle Befehle unterstützen `--json`, damit ein KI-Agent sie mit anderen Tools verketten kann.

## Schnellstart

```bash
git clone https://github.com/faborsky/podbean-app.git && cd podbean-app
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cp .env.example .env        # PODBEAN_CLIENT_ID + PODBEAN_CLIENT_SECRET

python podbean_cli.py podcasts
python podbean_cli.py upload --file /path/to/episode.mp3 --title "Episode Title" --podcast my-podcast
```

Die vollständige Dokumentation (Podbean-API-Zugang, alle Befehle, zweisprachiger Workflow) gibt es auf Englisch: **[README.md](../README.md)**.

## Lizenz

MIT · [LICENSE](../LICENSE)

## Autor

[Jindřich Fáborský](https://www.faborsky.com), Marketer und Dozent aus Prag. Ich bringe Marketern bei, mit KI eigene Tools zu bauen.
