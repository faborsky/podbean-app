# Podbean CLI

[🇬🇧 English](../README.md) · [🇨🇿 Čeština](../README.cs.md) · [🇪🇸 Español](README.es.md) · **🇧🇷 Português** · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇯🇵 日本語](README.ja.md) · [🇸🇪 Svenska](README.sv.md) · [🇳🇴 Norsk](README.nb.md) · [🇩🇰 Dansk](README.da.md)

CLI em Python que envia e gerencia episódios de podcast pela API REST do [Podbean](https://www.podbean.com/). Para podcasters que publicam com frequência ou em vários idiomas e não querem passar pelo painel do Podbean toda vez.

Publicar um único episódio dá muito trabalho repetitivo: enviar o arquivo, preencher os metadados, mudar o status, acompanhar os rascunhos. Foi feito para ser controlado pelo [Claude Code](https://docs.anthropic.com/en/docs/claude-code) ou outro agente de IA: você cuida do programa e a IA cuida da parte administrativa.

Autor: [Jindřich Fáborský](https://www.faborsky.com)

## O que ele faz

- `upload`: envia o áudio e cria o episódio. Por padrão como rascunho; com `--status publish` publica na hora.
- `episode-update`: altera o título, a descrição ou o status de um episódio.
- `episode-set-logo`: define uma capa própria para um único episódio (JPG/PNG quadrado, 1400–3000 px).
- `podcasts`, `episodes`, `episode-get`: lista seus podcasts e episódios. `episode-delete` só apaga com `--confirm`.
- Todos os comandos aceitam `--json`, então um agente de IA pode encadeá-los com outras ferramentas.

## Início rápido

```bash
git clone https://github.com/faborsky/podbean-app.git && cd podbean-app
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cp .env.example .env        # PODBEAN_CLIENT_ID + PODBEAN_CLIENT_SECRET

python podbean_cli.py podcasts
python podbean_cli.py upload --file /path/to/episode.mp3 --title "Episode Title" --podcast my-podcast
```

A documentação completa (credenciais da API do Podbean, todos os comandos, fluxo bilíngue) está em inglês: **[README.md](../README.md)**.

## Licença

MIT · [LICENSE](../LICENSE)

## Autor

[Jindřich Fáborský](https://www.faborsky.com), profissional de marketing e educador de Praga. Ensino profissionais de marketing a criar suas próprias ferramentas com IA.
