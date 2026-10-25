# Podbean CLI

[🇬🇧 English](../README.md) · [🇨🇿 Čeština](../README.cs.md) · [🇪🇸 Español](README.es.md) · [🇧🇷 Português](README.pt-BR.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · **🇨🇳 简体中文** · [🇯🇵 日本語](README.ja.md) · [🇸🇪 Svenska](README.sv.md) · [🇳🇴 Norsk](README.nb.md) · [🇩🇰 Dansk](README.da.md)

一个 Python 命令行工具，通过 [Podbean](https://www.podbean.com/) REST API 上传和管理播客节目。适合定期更新或做多语言节目、不想每次都在 Podbean 后台点来点去的播客主。

发布一期节目就有一堆重复劳动：上传文件、填写元数据、设置状态、盯着草稿。这个工具专为 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 或其他 AI 智能体操作而设计：你专心做节目，后台杂事交给 AI。

作者：[Jindřich Fáborský](https://www.faborsky.com)

## 功能

- `upload`：上传音频并创建单集。默认存为草稿，加 `--status publish` 则直接发布。
- `episode-update`：修改单集的标题、简介或状态。
- `episode-set-logo`：为单独一集设置封面（正方形 JPG/PNG，1400–3000 px）。
- `podcasts`、`episodes`、`episode-get`：列出你的播客和单集。`episode-delete` 必须加 `--confirm` 才会删除。
- 所有命令都支持 `--json`，方便 AI 智能体把它和其他工具串联起来。

## 快速开始

```bash
git clone https://github.com/faborsky/podbean-app.git && cd podbean-app
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cp .env.example .env        # PODBEAN_CLIENT_ID + PODBEAN_CLIENT_SECRET

python podbean_cli.py podcasts
python podbean_cli.py upload --file /path/to/episode.mp3 --title "Episode Title" --podcast my-podcast
```

完整文档（Podbean API 凭证、全部命令、双语工作流）为英文：**[README.md](../README.md)**。

## 许可证

MIT · [LICENSE](../LICENSE)

## 作者

[Jindřich Fáborský](https://www.faborsky.com)，来自布拉格的营销人和讲师，教营销人员用 AI 自己做工具。
