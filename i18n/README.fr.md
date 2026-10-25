# Podbean CLI

[🇬🇧 English](../README.md) · [🇨🇿 Čeština](../README.cs.md) · [🇪🇸 Español](README.es.md) · [🇧🇷 Português](README.pt-BR.md) · [🇩🇪 Deutsch](README.de.md) · **🇫🇷 Français** · [🇨🇳 简体中文](README.zh-CN.md) · [🇯🇵 日本語](README.ja.md) · [🇸🇪 Svenska](README.sv.md) · [🇳🇴 Norsk](README.nb.md) · [🇩🇰 Dansk](README.da.md)

CLI en Python qui envoie et gère des épisodes de podcast via l'API REST de [Podbean](https://www.podbean.com/). Pour les podcasteurs qui publient régulièrement ou en plusieurs langues et ne veulent pas repasser à chaque fois par le tableau de bord Podbean.

Publier un seul épisode demande beaucoup de travail répétitif : envoyer le fichier, remplir les métadonnées, changer le statut, suivre les brouillons. Le CLI est conçu pour être piloté par [Claude Code](https://docs.anthropic.com/en/docs/claude-code) ou un autre agent IA : tu t'occupes de l'émission, l'IA s'occupe de l'administratif.

Auteur: [Jindřich Fáborský](https://www.faborsky.com)

## Ce qu'il fait

- `upload` : envoie l'audio et crée l'épisode. En brouillon par défaut ; avec `--status publish`, il est publié tout de suite.
- `episode-update` : modifie le titre, la description ou le statut d'un épisode.
- `episode-set-logo` : définit une pochette propre à un seul épisode (JPG/PNG carré, 1400–3000 px).
- `podcasts`, `episodes`, `episode-get` : liste tes podcasts et tes épisodes. `episode-delete` ne supprime qu'avec `--confirm`.
- Toutes les commandes acceptent `--json`, pour qu'un agent IA puisse les enchaîner avec d'autres outils.

## Démarrage rapide

```bash
git clone https://github.com/faborsky/podbean-app.git && cd podbean-app
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cp .env.example .env        # PODBEAN_CLIENT_ID + PODBEAN_CLIENT_SECRET

python podbean_cli.py podcasts
python podbean_cli.py upload --file /path/to/episode.mp3 --title "Episode Title" --podcast my-podcast
```

La documentation complète (identifiants de l'API Podbean, toutes les commandes, workflow bilingue) est en anglais : **[README.md](../README.md)**.

## Licence

MIT · [LICENSE](../LICENSE)

## Auteur

[Jindřich Fáborský](https://www.faborsky.com), marketeur et formateur à Prague. J'apprends aux marketeurs à créer leurs propres outils avec l'IA.
