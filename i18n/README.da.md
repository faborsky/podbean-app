# Podbean CLI

[🇬🇧 English](../README.md) · [🇨🇿 Čeština](../README.cs.md) · [🇪🇸 Español](README.es.md) · [🇧🇷 Português](README.pt-BR.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇯🇵 日本語](README.ja.md) · [🇸🇪 Svenska](README.sv.md) · [🇳🇴 Norsk](README.nb.md) · **🇩🇰 Dansk**

Et Python-CLI, der uploader og administrerer podcastafsnit via [Podbeans](https://www.podbean.com/) REST-API. Til podcastere, der udgiver jævnligt eller på flere sprog og ikke vil klikke sig gennem Podbeans kontrolpanel hver gang.

Bare ét afsnit kræver en masse gentaget arbejde: uploade filen, udfylde metadata, ændre status, holde styr på kladder. Værktøjet er bygget til at blive styret af [Claude Code](https://docs.anthropic.com/en/docs/claude-code) eller en anden AI-agent: du koncentrerer dig om podcasten, AI'en tager sig af administrationen.

Forfatter: [Jindřich Fáborský](https://www.faborsky.com)

## Hvad det gør

- `upload`: uploader lyden og opretter afsnittet. Som kladde som standard, med `--status publish` udgives det med det samme.
- `episode-update`: ændrer titel, beskrivelse eller status for et afsnit.
- `episode-set-logo`: giver et enkelt afsnit sit eget coverbillede (kvadratisk JPG/PNG, 1400–3000 px).
- `podcasts`, `episodes`, `episode-get`: viser dine podcasts og afsnit. `episode-delete` sletter kun med `--confirm`.
- Alle kommandoer understøtter `--json`, så en AI-agent kan kæde dem sammen med andre værktøjer.

## Hurtig start

```bash
git clone https://github.com/faborsky/podbean-app.git && cd podbean-app
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cp .env.example .env        # PODBEAN_CLIENT_ID + PODBEAN_CLIENT_SECRET

python podbean_cli.py podcasts
python podbean_cli.py upload --file /path/to/episode.mp3 --title "Episode Title" --podcast my-podcast
```

Den fulde dokumentation (Podbean-API-adgang, alle kommandoer, tosproget arbejdsgang) er på engelsk: **[README.md](../README.md)**.

## Licens

MIT · [LICENSE](../LICENSE)

## Forfatter

[Jindřich Fáborský](https://www.faborsky.com), marketingmand og underviser fra Prag. Jeg lærer marketingfolk at bygge deres egne værktøjer med AI.
