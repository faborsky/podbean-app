# Podbean CLI

[🇬🇧 English](../README.md) · [🇨🇿 Čeština](../README.cs.md) · **🇪🇸 Español** · [🇧🇷 Português](README.pt-BR.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇯🇵 日本語](README.ja.md) · [🇸🇪 Svenska](README.sv.md) · [🇳🇴 Norsk](README.nb.md) · [🇩🇰 Dansk](README.da.md)

CLI en Python que sube y gestiona episodios de podcast a través de la API REST de [Podbean](https://www.podbean.com/). Para podcasters que publican con regularidad o en varios idiomas y no quieren pasar cada vez por el panel de Podbean.

Publicar un solo episodio implica mucho trabajo repetitivo: subir el archivo, rellenar los metadatos, cambiar el estado, vigilar los borradores. Está pensado para que lo maneje [Claude Code](https://docs.anthropic.com/en/docs/claude-code) u otro agente de IA: tú te dedicas al programa y la IA se encarga de la parte administrativa.

Autor: [Jindřich Fáborský](https://www.faborsky.com)

## Qué hace

- `upload`: sube el audio y crea el episodio. Por defecto como borrador; con `--status publish` lo publica directamente.
- `episode-update`: cambia el título, la descripción o el estado de un episodio.
- `episode-set-logo`: asigna una portada propia a un solo episodio (JPG/PNG cuadrado, 1400–3000 px).
- `podcasts`, `episodes`, `episode-get`: lista tus podcasts y episodios. `episode-delete` solo borra con `--confirm`.
- Todos los comandos aceptan `--json`, así que un agente de IA puede encadenarlos con otras herramientas.

## Inicio rápido

```bash
git clone https://github.com/faborsky/podbean-app.git && cd podbean-app
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cp .env.example .env        # PODBEAN_CLIENT_ID + PODBEAN_CLIENT_SECRET

python podbean_cli.py podcasts
python podbean_cli.py upload --file /path/to/episode.mp3 --title "Episode Title" --podcast my-podcast
```

La documentación completa (credenciales de la API de Podbean, todos los comandos, flujo bilingüe) está en inglés: **[README.md](../README.md)**.

## Licencia

MIT · [LICENSE](../LICENSE)

## Autor

[Jindřich Fáborský](https://www.faborsky.com), marketer y formador de Praga. Enseño a los marketers a crear sus propias herramientas con IA.
