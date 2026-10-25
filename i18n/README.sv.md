# Podbean CLI

[🇬🇧 English](../README.md) · [🇨🇿 Čeština](../README.cs.md) · [🇪🇸 Español](README.es.md) · [🇧🇷 Português](README.pt-BR.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇯🇵 日本語](README.ja.md) · **🇸🇪 Svenska** · [🇳🇴 Norsk](README.nb.md) · [🇩🇰 Dansk](README.da.md)

Ett Python-CLI som laddar upp och hanterar poddavsnitt via [Podbeans](https://www.podbean.com/) REST-API. För poddare som publicerar regelbundet eller på flera språk och inte vill klicka sig igenom Podbeans gränssnitt varje gång.

Att publicera ett enda avsnitt innebär mycket upprepat arbete: ladda upp filen, fylla i metadata, ändra status, hålla koll på utkast. Verktyget är byggt för att styras av [Claude Code](https://docs.anthropic.com/en/docs/claude-code) eller en annan AI-agent: du fokuserar på podden, AI:n tar hand om administrationen.

Författare: [Jindřich Fáborský](https://www.faborsky.com)

## Vad det gör

- `upload`: laddar upp ljudet och skapar avsnittet. Som utkast som standard, med `--status publish` publiceras det direkt.
- `episode-update`: ändrar titel, beskrivning eller status för ett avsnitt.
- `episode-set-logo`: ger ett enskilt avsnitt en egen omslagsbild (kvadratisk JPG/PNG, 1400–3000 px).
- `podcasts`, `episodes`, `episode-get`: listar dina poddar och avsnitt. `episode-delete` raderar bara med `--confirm`.
- Alla kommandon stöder `--json`, så att en AI-agent kan kedja ihop dem med andra verktyg.

## Snabbstart

```bash
git clone https://github.com/faborsky/podbean-app.git && cd podbean-app
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cp .env.example .env        # PODBEAN_CLIENT_ID + PODBEAN_CLIENT_SECRET

python podbean_cli.py podcasts
python podbean_cli.py upload --file /path/to/episode.mp3 --title "Episode Title" --podcast my-podcast
```

Den fullständiga dokumentationen (Podbean-API-uppgifter, alla kommandon, tvåspråkigt arbetsflöde) finns på engelska: **[README.md](../README.md)**.

## Licens

MIT · [LICENSE](../LICENSE)

## Författare

[Jindřich Fáborský](https://www.faborsky.com), marknadsförare och utbildare från Prag. Jag lär marknadsförare att bygga egna verktyg med AI.
