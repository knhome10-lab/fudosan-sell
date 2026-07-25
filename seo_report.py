"""
Search Console SEO 週次レポート生成スクリプト
=============================================
【初回のみ】
1. 必要ライブラリをインストール:
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

2. 初回実行時にブラウザが開きGoogleログイン画面が表示されます。
   knhome10@gmail.com でログインして許可してください。
   （2回目以降は自動認証されます）

【実行方法】
   python seo_report.py

【出力】
   seo_report_YYYYMMDD.html が生成されます。
"""

import os
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ============================================================
# 設定
# ============================================================
SITE_URL      = "https://www.knhome.jp/fudosan-sell/"
CLIENT_SECRET = os.path.join(os.path.dirname(__file__), "client_secret.json")
TOKEN_FILE    = os.path.join(os.path.dirname(__file__), "token.json")
SCOPES        = ["https://www.googleapis.com/auth/webmasters.readonly"]

# 監視キーワード
TARGET_KEYWORDS = [
    "春日部 不動産売却",
    "春日部 空き家 売却",
    "春日部 相続 不動産",
    "春日部 不動産 査定",
    "春日部 空き家 買取",
    "春日部 土地 売却",
    "埼玉 空き家 売却",
    "相続 不動産 売却 春日部",
]

# ============================================================

def authenticate():
    """Google OAuth2認証"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return creds


def fetch_keyword_data(service, keyword, days=28):
    """指定キーワードを含む検索クエリを合算して取得（部分一致・語順非依存）

    旧実装は operator="equals" で完全一致のみを見ていたため、実際のユーザーの
    検索語（スペースの有無・語順が異なる）とほぼ一致せず、常に0件になっていた。
    キーワードをスペースで分割し、すべての語を含むクエリ（AND条件・部分一致）を
    複数取得して合算する方式に変更。
    """
    end_date   = datetime.now() - timedelta(days=3)  # Search Consoleは3日前まで
    start_date = end_date - timedelta(days=days)

    terms = [t for t in keyword.split() if t]
    filters = [
        {"dimension": "query", "operator": "contains", "expression": term}
        for term in terms
    ]

    try:
        response = service.searchanalytics().query(
            siteUrl=SITE_URL,
            body={
                "startDate":  start_date.strftime("%Y-%m-%d"),
                "endDate":    end_date.strftime("%Y-%m-%d"),
                "dimensions": ["query"],
                "dimensionFilterGroups": [{"filters": filters}],
                "rowLimit": 25,
            }
        ).execute()

        rows = response.get("rows", [])
        if rows:
            total_clicks      = sum(int(r.get("clicks", 0)) for r in rows)
            total_impressions = sum(int(r.get("impressions", 0)) for r in rows)
            if total_impressions > 0:
                weighted_position = sum(
                    r.get("position", 0) * r.get("impressions", 0) for r in rows
                ) / total_impressions
                ctr = round((total_clicks / total_impressions) * 100, 1)
            else:
                weighted_position = sum(r.get("position", 0) for r in rows) / len(rows)
                ctr = 0
            return {
                "clicks":          total_clicks,
                "impressions":     total_impressions,
                "position":        round(weighted_position, 1),
                "ctr":             ctr,
                "matched_queries": len(rows),
            }
    except Exception as e:
        print(f"  キーワード取得エラー ({keyword}): {e}")

    return {"clicks": 0, "impressions": 0, "position": 0, "ctr": 0, "matched_queries": 0}


def fetch_top_pages(service, days=28):
    """上位ページ別パフォーマンスを取得"""
    end_date   = datetime.now() - timedelta(days=3)
    start_date = end_date - timedelta(days=days)

    try:
        response = service.searchanalytics().query(
            siteUrl=SITE_URL,
            body={
                "startDate":  start_date.strftime("%Y-%m-%d"),
                "endDate":    end_date.strftime("%Y-%m-%d"),
                "dimensions": ["page"],
                "rowLimit":   10,
                "orderBy":    [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
            }
        ).execute()
        return response.get("rows", [])
    except Exception as e:
        print(f"  ページ取得エラー: {e}")
        return []


def generate_html(keyword_data, top_pages, generated_at):
    """HTMLレポートを生成"""

    # キーワードテーブル行
    kw_rows = ""
    for kw, d in keyword_data.items():
        pos = d["position"]
        if pos == 0:
            pos_badge = '<span style="color:#9ca3af">データなし</span>'
        elif pos <= 3:
            pos_badge = f'<span style="background:#dcfce7;color:#16a34a;padding:2px 8px;border-radius:999px;font-weight:700">{pos}位</span>'
        elif pos <= 10:
            pos_badge = f'<span style="background:#fef9c3;color:#ca8a04;padding:2px 8px;border-radius:999px;font-weight:700">{pos}位</span>'
        elif pos <= 20:
            pos_badge = f'<span style="background:#fee2e2;color:#dc2626;padding:2px 8px;border-radius:999px;font-weight:700">{pos}位</span>'
        else:
            pos_badge = f'<span style="color:#6b7280">{pos}位</span>'

        kw_rows += f"""
        <tr>
          <td style="padding:10px 14px;border-bottom:1px solid #f3f4f6;font-weight:600">{kw}</td>
          <td style="padding:10px 14px;border-bottom:1px solid #f3f4f6;text-align:center">{pos_badge}</td>
          <td style="padding:10px 14px;border-bottom:1px solid #f3f4f6;text-align:center;color:#1e3a8a;font-weight:700">{d['clicks']}</td>
          <td style="padding:10px 14px;border-bottom:1px solid #f3f4f6;text-align:center;color:#6b7280">{d['impressions']}</td>
          <td style="padding:10px 14px;border-bottom:1px solid #f3f4f6;text-align:center;color:#6b7280">{d['ctr']}%</td>
        </tr>"""

    # ページテーブル行
    page_rows = ""
    for r in top_pages:
        url   = r.get("keys", [""])[0].replace(SITE_URL, "/")
        page_rows += f"""
        <tr>
          <td style="padding:10px 14px;border-bottom:1px solid #f3f4f6;font-size:12px;color:#374151">{url}</td>
          <td style="padding:10px 14px;border-bottom:1px solid #f3f4f6;text-align:center;color:#1e3a8a;font-weight:700">{int(r.get('clicks',0))}</td>
          <td style="padding:10px 14px;border-bottom:1px solid #f3f4f6;text-align:center;color:#6b7280">{int(r.get('impressions',0))}</td>
          <td style="padding:10px 14px;border-bottom:1px solid #f3f4f6;text-align:center;color:#6b7280">{round(r.get('position',0),1)}位</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SEOレポート {generated_at} | KNホーム</title>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:'Hiragino Sans','Yu Gothic',sans-serif; background:#f4f6fb; color:#1f2937; }}
  header {{ background:#1e3a8a; padding:20px 32px; }}
  header h1 {{ color:#fff; font-size:18px; font-weight:800; }}
  header p  {{ color:rgba(255,255,255,.7); font-size:12px; margin-top:4px; }}
  .container {{ max-width:900px; margin:0 auto; padding:24px 16px; }}
  .card {{ background:#fff; border-radius:12px; border:1px solid #e5e7eb;
           padding:20px 24px; margin-bottom:24px; box-shadow:0 1px 4px rgba(0,0,0,.06); }}
  .card h2 {{ font-size:15px; font-weight:700; color:#374151; margin-bottom:16px;
              padding-bottom:10px; border-bottom:1px solid #f3f4f6; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th {{ background:#f9fafb; text-align:left; padding:10px 14px;
        font-size:11px; font-weight:700; color:#6b7280;
        border-bottom:1px solid #e5e7eb; white-space:nowrap; }}
  footer {{ text-align:center; font-size:11px; color:#9ca3af; padding:20px; }}
</style>
</head>
<body>
<header>
  <h1>📊 SEOレポート</h1>
  <p>サイト：{SITE_URL}　|　生成日：{generated_at}　|　集計期間：直近28日</p>
</header>
<div class="container">

  <div class="card">
    <h2>🎯 ターゲットキーワード 順位・パフォーマンス</h2>
    <table>
      <thead>
        <tr>
          <th>キーワード</th>
          <th style="text-align:center">平均順位</th>
          <th style="text-align:center">クリック数</th>
          <th style="text-align:center">表示回数</th>
          <th style="text-align:center">CTR</th>
        </tr>
      </thead>
      <tbody>{kw_rows}</tbody>
    </table>
  </div>

  <div class="card">
    <h2>📄 クリック数上位ページ</h2>
    <table>
      <thead>
        <tr>
          <th>URL</th>
          <th style="text-align:center">クリック数</th>
          <th style="text-align:center">表示回数</th>
          <th style="text-align:center">平均順位</th>
        </tr>
      </thead>
      <tbody>{page_rows}</tbody>
    </table>
  </div>

</div>
<footer>出典：Google Search Console API ／ KNホーム SEO自動レポート</footer>
</body>
</html>"""


def main():
    print("Search Console 認証中...")
    creds   = authenticate()
    service = build("searchconsole", "v1", credentials=creds)
    print("認証完了\n")

    print("キーワードデータ取得中...")
    keyword_data = {}
    for kw in TARGET_KEYWORDS:
        data = fetch_keyword_data(service, kw)
        keyword_data[kw] = data
        pos_str = f"{data['position']}位" if data['position'] > 0 else "データなし"
        print(f"  {kw}: {pos_str}　クリック:{data['clicks']}")

    print("\nページデータ取得中...")
    top_pages = fetch_top_pages(service)
    print(f"  {len(top_pages)}ページ取得")

    generated_at = datetime.now().strftime("%Y年%m月%d日")
    html = generate_html(keyword_data, top_pages, generated_at)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # HTMLレポート保存
    filename  = f"seo_report_{datetime.now().strftime('%Y%m%d')}.html"
    out_path  = os.path.join(script_dir, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    # JSONデータ保存（Coworkの自動分析用）
    json_data = {
        "generated_at": generated_at,
        "site_url": SITE_URL,
        "keywords": keyword_data,
        "top_pages": [
            {
                "url":         r.get("keys", [""])[0],
                "clicks":      int(r.get("clicks", 0)),
                "impressions": int(r.get("impressions", 0)),
                "position":    round(r.get("position", 0), 1),
                "ctr":         round(r.get("ctr", 0) * 100, 1),
            }
            for r in top_pages
        ],
    }
    json_path = os.path.join(script_dir, "seo_latest.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ レポート生成完了 → {out_path}")
    print(f"✅ JSONデータ保存  → {json_path}")


if __name__ == "__main__":
    main()
