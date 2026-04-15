---
title: Python Tips
tags: [python, programming]
---

# Python メモ

[[Getting Started|← はじめに]] に戻る。

## リスト内包表記

```python
# 偶数だけ抽出
evens = [x for x in range(20) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

## 型ヒント

```python
from typing import Optional

def greet(name: str, times: int = 1) -> list[str]:
    return [f"Hello, {name}!"] * times
```

## f-string フォーマット

```python
score = 98.567
print(f"スコア: {score:.1f}%")   # スコア: 98.6%
print(f"16進: {255:#010x}")       # 16進: 0x000000ff
```

> [!DANGER] 注意点
> `eval()` や `exec()` の使用は ==セキュリティリスク== があります。
> 信頼できない入力には **絶対に使わない** こと。

## 参考リンク

- [[guides/Markdown Guide]] — Markdownの書き方
- [[index]] — トップへ

タグ: #python #tips #programming
