## Obsidian Vault → Single HTML Converter

Obsidian のボルトフォルダを **単一の自己完結型 HTML ファイル** に変換する Python ツール。

---

## セットアップ

```bash
pip install -r requirements.txt
```

## 使い方

```bash
# 基本（output.html に出力）
python convert.py ./my_vault

# 出力先・タイトルを指定
python convert.py ./my_vault -o my_notes.html --title "My Notes"
```

## ファイル構成

```
.
├── convert.py        # CLI エントリーポイント
├── requirements.txt  # 依存ライブラリ (markdown, pygments, pyyaml)
└── src/
    ├── parser.py     # Obsidian Markdown パーサー
    └── template.py   # HTML テンプレート（CSS/JS 埋め込み）
```

## 対応している Obsidian 記法

| 記法 | 内容 |
|------|------|
| `[[Page]]` | wikilink（内部リンク） |
| `[[Page\|別名]]` | エイリアス付き wikilink |
| `![[image.png]]` | 画像/ファイル埋め込み |
| `==highlight==` | ハイライト |
| `#tag` | タグ |
| `> [!NOTE]` など | 13種類の Callout |
| `- [x]` / `- [ ]` | チェックリスト |
| YAML frontmatter | title 等のメタデータ |
| フォルダ構造 | サイドバーに折りたたみ表示 |

対応 Callout タイプ: `note` `info` `tip` `warning` `danger` `success` `question` `quote` `abstract` `todo` `bug` `example`

## 出力 HTML の機能

- ダーク / ライトテーマ切替（設定は localStorage に保存）
- サイドバーで全ページ一覧（フォルダ階層、折りたたみ可能）
- タイトル検索（サイドバー内フィルタ）
- ハッシュベースルーティング（`#page-slug`）
- シンタックスハイライト（Pygments 内蔵、外部依存なし）
- レスポンシブ対応（スマホではハンバーガーメニュー）
