---
title: Getting Started
---

# はじめに

[[index|トップページ]] に戻る。

## このツールについて

このツールは Obsidian のボルトフォルダを **単一の HTML ファイル** に変換します。

### 対応している記法

| 記法 | 説明 |
|------|------|
| `[[Page]]` | 内部リンク（wikilink） |
| `[[Page\|別名]]` | エイリアス付きwikilink |
| `![[image.png]]` | 画像埋め込み |
| `==text==` | ハイライト |
| `#tag` | タグ |
| `> [!NOTE]` | コールアウト |

## コードブロック

```python
def hello(name: str) -> str:
    return f"Hello, {name}!"

print(hello("Obsidian"))
```

```bash
python convert.py ./my_vault -o output.html --title "My Notes"
```

> [!SUCCESS] 完了
> セットアップ完了！[[Python Tips]] も参照してください。
