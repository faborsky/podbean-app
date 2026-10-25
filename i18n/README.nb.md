# Podbean CLI

[🇬🇧 English](../README.md) · [🇨🇿 Čeština](../README.cs.md) · [🇪🇸 Español](README.es.md) · [🇧🇷 Português](README.pt-BR.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇯🇵 日本語](README.ja.md) · [🇸🇪 Svenska](README.sv.md) · **🇳🇴 Norsk** · [🇩🇰 Dansk](README.da.md)

Et Python-CLI som laster opp og administrerer podkastepisoder via REST-API-et til [Podbean](https://www.podbean.com/). For podkastere som publiserer jevnlig eller på flere språk og ikke vil klikke seg gjennom Podbean-panelet hver gang.

Å publisere én enkelt episode betyr mye gjentakende arbeid: laste opp filen, fylle inn metadata, endre status, holde styr på utkast. Verktøyet er laget for å styres av [Claude Code](https://docs.anthropic.com/en/docs/claude-code) eller en annen AI-agent: du konsentrerer deg om podkasten, AI-en tar seg av administrasjonen.

Forfatter: [Jindřich Fáborský](https://www.faborsky.com)

## Hva det gjør

- `upload`: laster opp lyden og oppretter episoden. Som utkast som standard, med `--status publish` publiseres den med en gang.
- `episode-update`: endrer tittel, beskrivelse eller status for en episode.
- `episode-set-logo`: gir én enkelt episode et eget omslagsbilde (kvadratisk JPG/PNG, 1400–3000 px).
- `podcasts`, `episodes`, `episode-get`: lister podkastene og episodene dine. `episode-delete` sletter bare med `--confirm`.
- Alle kommandoer støtter `--json`, slik at en AI-agent kan koble dem sammen med andre verktøy.

## Hurtigstart

```bash
git clone https://github.com/faborsky/podbean-app.git && cd podbean-app
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cp .env.example .env        # PODBEAN_CLIENT_ID + PODBEAN_CLIENT_SECRET

python podbean_cli.py podcasts
python podbean_cli.py upload --file /path/to/episode.mp3 --title "Episode Title" --podcast my-podcast
```

Den fullstendige dokumentasjonen (Podbean-API-tilgang, alle kommandoer, tospråklig arbeidsflyt) er på engelsk: **[README.md](../README.md)**.

## Lisens

MIT · [LICENSE](../LICENSE)

## Forfatter

[Jindřich Fáborský](https://www.faborsky.com), markedsfører og underviser fra Praha. Jeg lærer markedsførere å bygge egne verktøy med AI.
