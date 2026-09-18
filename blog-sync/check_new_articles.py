#!/usr/bin/env python3
"""
戸建てリノベINFO (smile.re-agent.info/blog) 新着記事チェッカー

使い方:
  1. Claudeが web_fetch で https://smile.re-agent.info/blog/?m=YYYYMM
     (当月、および月初1週間以内なら前月も) を取得する。
  2. 取得したテキストを archive_YYYYMM.txt として保存する。
  3. 本スクリプトを実行し、log.json に無い post_id を新着として抽出する。

  python3 check_new_articles.py --log log.json archive_202609.txt [archive_202608.txt ...]

出力: 新着記事の一覧 (post_id, date, url) を古い順にJSON配列で標準出力に出す。
      新着が無ければ空配列 [] を出力する。
"""
import argparse
import json
import re
import sys

# アーカイブページの1記事ブロックは概ね以下の形式:
# [カテゴリ タイトル本文...本文...2026.09.14](https://smile.re-agent.info/blog/?p=13711)
ARTICLE_PATTERN = re.compile(
    r"\[([^\[\]]*?(\d{4})\.(\d{2})\.(\d{2}))\]\(https://smile\.re-agent\.info/blog/\?p=(\d+)\)"
)


def parse_archive_text(text):
    """アーカイブページのテキストから (post_id, date, raw_snippet) のリストを抽出する"""
    results = []
    for m in ARTICLE_PATTERN.finditer(text):
        snippet, year, month, day, post_id = m.groups()
        date = f"{year}-{month}-{day}"
        results.append({"post_id": int(post_id), "date": date, "snippet": snippet.strip()})
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True, help="log.json のパス")
    ap.add_argument("archive_files", nargs="+", help="保存済みアーカイブページのテキストファイル")
    args = ap.parse_args()

    with open(args.log, encoding="utf-8") as f:
        log = json.load(f)
    known_ids = {a["post_id"] for a in log["articles"]}

    found = {}
    for path in args.archive_files:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for item in parse_archive_text(text):
            found[item["post_id"]] = item

    new_items = [v for k, v in found.items() if k not in known_ids]
    new_items.sort(key=lambda x: (x["date"], x["post_id"]))  # 古い順

    for item in new_items:
        item["url"] = f"https://smile.re-agent.info/blog/?p={item['post_id']}"

    print(json.dumps(new_items, ensure_ascii=False, indent=2))

    if not new_items:
        print("# 新着記事はありませんでした。", file=sys.stderr)
    else:
        print(f"# 新着記事 {len(new_items)} 件を検出しました。", file=sys.stderr)


if __name__ == "__main__":
    main()
