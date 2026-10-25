# Podbean CLI

[🇬🇧 English](../README.md) · [🇨🇿 Čeština](../README.cs.md) · [🇪🇸 Español](README.es.md) · [🇧🇷 Português](README.pt-BR.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇨🇳 简体中文](README.zh-CN.md) · **🇯🇵 日本語** · [🇸🇪 Svenska](README.sv.md) · [🇳🇴 Norsk](README.nb.md) · [🇩🇰 Dansk](README.da.md)

[Podbean](https://www.podbean.com/) の REST API を使って、ポッドキャストのエピソードをアップロード・管理する Python 製 CLI です。定期的に、あるいは複数の言語で配信していて、毎回 Podbean の管理画面を操作したくないポッドキャスター向け。

エピソードを 1 本公開するだけでも、ファイルのアップロード、メタデータの入力、ステータスの設定、下書きの管理と、繰り返しの作業が多くあります。[Claude Code](https://docs.anthropic.com/en/docs/claude-code) などの AI エージェントが操作する前提で作っているので、あなたは番組づくりに集中し、事務作業は AI に任せられます。

作者：[Jindřich Fáborský](https://www.faborsky.com)

## できること

- `upload`：音声をアップロードしてエピソードを作成します。デフォルトは下書きで、`--status publish` を付けるとすぐ公開します。
- `episode-update`：エピソードのタイトル、説明、ステータスを変更します。
- `episode-set-logo`：エピソード単位で独自のカバー画像を設定します（正方形の JPG/PNG、1400–3000 px）。
- `podcasts`・`episodes`・`episode-get`：ポッドキャストとエピソードを一覧表示します。`episode-delete` は `--confirm` を付けたときだけ削除します。
- すべてのコマンドが `--json` に対応しているので、AI エージェントが他のツールとつなげて使えます。

## クイックスタート

```bash
git clone https://github.com/faborsky/podbean-app.git && cd podbean-app
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cp .env.example .env        # PODBEAN_CLIENT_ID + PODBEAN_CLIENT_SECRET

python podbean_cli.py podcasts
python podbean_cli.py upload --file /path/to/episode.mp3 --title "Episode Title" --podcast my-podcast
```

完全なドキュメント（Podbean API の認証情報、全コマンド、2 言語ワークフロー）は英語です：**[README.md](../README.md)**

## ライセンス

MIT · [LICENSE](../LICENSE)

## 作者

[Jindřich Fáborský](https://www.faborsky.com)、プラハ在住のマーケター・講師。マーケターが AI で自分のツールを作れるよう教えています。
