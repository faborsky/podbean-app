# Podbean CLI

Python CLI na správu podcastů na [Podbeanu](https://www.podbean.com/) přes jejich REST API. Postavené tak, aby ho řídil [Claude Code](https://docs.anthropic.com/en/docs/claude-code) nebo jiný AI agent. Ty se věnuješ tvorbě, AI za tebe odbaví administrativu.

> [!TIP]
> **Appka je zdarma a je tvoje.** Naklonuj si ji, používej ji, přestav si ji po svém.
>
> Nevíš, jak ji rozjet? Nebo chceš AI v marketingu používat systematicky: řídit z jednoho místa všechny kanály, automatizovat rutinu, postavit si vlastní znalostní bázi a vibe codovat si nástroje na míru své firmě? To učím v kurzu **[AI First](https://aifirst.cz)**. Tahle appka je v něm vysvětlená i s tím, jak si postavit vlastní.

## Proč to vzniklo

Vydat jednu epizodu podcastu znamená překvapivě moc opakované práce: nahrát soubor, vyplnit metadata, nastavit stav, pohlídat drafty. Vynásob si to počtem pořadů a jazyků a utrácíš kreativní energii za administrativu.

Tohle CLI podbeanovské operace zautomatizuje, takže se dají zřetězit s dalšími nástroji do celého podcastového workflow:

1. **Natoč** podcast
2. **Přepiš a přelož** přes [whisper-cz-en](https://github.com/faborsky/whisper-cz-en)
3. **Vygeneruj obálku** přes [nanobanana-app](https://github.com/faborsky/nanobanana-app)
4. **Nahraj a vydej** přes tohle CLI

Všechno řídí Claude Code v jedné konverzaci. Ty mluvíš, AI dělá papírování.

## Co potřebuješ

- **Python 3.9+**
- **Účet na Podbeanu** s podcastem
- **API přístupy k Podbeanu** (client ID a secret)

### Jak získat API přístupy k Podbeanu

1. Jdi na [Podbean Developer Portal](https://developers.podbean.com/)
2. Klikni na **Register a New App**
3. Vyplň údaje o aplikaci (název, kontaktní e-mail, logo)
4. Po schválení jdi do **My Apps** a klikni na **Manage App**
5. Zkopíruj si **App ID** (client ID) a **App Secret** (client secret)

Dokumentace API: [developers.podbean.com/podbean-api-docs](https://developers.podbean.com/podbean-api-docs/)

## Instalace

```bash
git clone https://github.com/faborsky/podbean-app.git
cd podbean-app

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# uprav .env a doplň přístupy k Podbeanu
```

## Konfigurace

Do `.env` doplň své API přístupy k Podbeanu:

```
PODBEAN_CLIENT_ID=your-client-id-here
PODBEAN_CLIENT_SECRET=your-client-secret-here
```

OAuth tokeny si CLI spravuje samo (cachuje je do `.token_cache.json`).

## Používání

Vždycky si nejdřív aktivuj virtuální prostředí:

```bash
source venv/bin/activate
```

### Výpis podcastů

Tohle spusť jako první, naplní se tím lokální cache slugů podcastů:

```bash
python podbean_cli.py podcasts
python podbean_cli.py podcasts --json
```

### Výpis epizod

```bash
python podbean_cli.py episodes --podcast my-podcast
python podbean_cli.py episodes --podcast my-podcast --limit 50 --offset 0
python podbean_cli.py episodes --json
```

### Detail epizody

```bash
python podbean_cli.py episode-get --episode-id EPISODE_ID
python podbean_cli.py episode-get --episode-id EPISODE_ID --json
```

### Nahrání a vytvoření epizody

Tři kroky: autorizace uploadu, upload na S3, vytvoření epizody. Epizoda se pro jistotu vytvoří jako **draft**.

```bash
# vytvoří draft (výchozí, bezpečné)
python podbean_cli.py upload \
  --file /path/to/episode.mp3 \
  --title "Episode Title" \
  --description "<p>Episode description in HTML</p>" \
  --podcast my-podcast

# vytvoří a rovnou publikuje
python podbean_cli.py upload \
  --file /path/to/episode.mp3 \
  --title "Episode Title" \
  --podcast my-podcast \
  --status publish

# s typem epizody pro Apple Podcasts
python podbean_cli.py upload \
  --file /path/to/episode.mp3 \
  --title "Episode Title" \
  --podcast my-podcast \
  --apple-episode-type full
```

### Úprava epizody

```bash
python podbean_cli.py episode-update --episode-id EPISODE_ID --title "New Title"
python podbean_cli.py episode-update --episode-id EPISODE_ID --status publish
python podbean_cli.py episode-update --episode-id EPISODE_ID --description "<p>Updated</p>"
```

### Vlastní obálka konkrétní epizody

Nahraje lokální obrázek a nastaví ho jako obálku epizody, což je jiná věc než logo
celého pořadu. Apple chce čtverec JPG/PNG, 1400–3000 px. Název a stav epizody
zůstanou beze změny.

```bash
python podbean_cli.py episode-set-logo --episode-id EPISODE_ID --image /path/to/cover.jpg --podcast my-podcast
```

### Smazání epizody

Kvůli bezpečnosti to chce flag `--confirm`:

```bash
python podbean_cli.py episode-delete --episode-id EPISODE_ID --confirm
```

### JSON výstup

Všechny příkazy umí `--json` pro strojově čitelný výstup. Hodí se to, když je orchestruje AI agent:

```bash
python podbean_cli.py episodes --podcast my-podcast --json
```

## Dvojjazyčné workflow (CZ/EN)

Typický průběh dvojjazyčného podcastu, který řídí Claude Code:

```
1. Natočíš epizodu (CZ nebo EN)
2. Přepis přes whisper-cz-en → .md přepis
3. Překlad přepisu (CZ↔EN) v Claude
4. Popisy epizody v obou jazycích
5. Obálka přes nanobanana-app
6. Upload CZ verze → podbean-app (draft)
7. Upload EN verze → podbean-app (draft)
8. Projdeš drafty a publikuješ
```

Každý krok může být samostatný skill pro Claude Code a všechny se dají zřetězit v jedné konverzaci.

## Řetěz automatizace

Tohle CLI je poslední článek většího podcastového pipelinu poháněného AI:

| Krok | Nástroj | Co dělá |
|------|------|-------------|
| Přepis | [whisper-cz-en](https://github.com/faborsky/whisper-cz-en) | Lokální přepis přes Whisper Large V3 (CZ/EN) |
| Překlad | Claude Code | Překlad přepisů mezi češtinou a angličtinou |
| Show notes | Claude Code | Popisy, názvy a shrnutí |
| Obálka | [nanobanana-app](https://github.com/faborsky/nanobanana-app) | Grafika k epizodě přes AI |
| Publikace | **podbean-app** (tohle repo) | Upload audia, vytvoření epizody, správa metadat |

## Struktura projektu

```
podbean_cli.py        # hlavní CLI (jeden soubor)
.env.example          # šablona pro API přístupy
.env                  # tvoje přístupy (mimo git)
.token_cache.json     # cachovaný OAuth token (generuje se sám, mimo git)
.podcast_cache.json   # mapování slug → podcast_id (generuje se samo, mimo git)
requirements.txt      # Python závislosti
CLAUDE.md             # instrukce pro Claude Code
```

## O projektu

Postavil [Jindřich Fáborský](https://github.com/faborsky) jako součást toolkitu na automatizaci podcastů. Běží v produkci na správě několika českých podcastů.

Projekt je zároveň součástí osnovy mezinárodního kurzu [Vibe Coding for Marketers](https://vibecodingformarketers.com), kde se marketéři učí stavět si nástroje s AI.

---

## Licence

MIT
