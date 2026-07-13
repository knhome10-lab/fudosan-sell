"""
埼玉県 不動産取引相場 データ取得スクリプト
================================================
【使い方】
1. reinfolib のAPIキーを取得する
   → https://www.reinfolib.mlit.go.jp/api/request/
   （無料・申請後5営業日でメールにて発行）

2. 下の API_KEY に取得したキーを貼り付ける

3. このスクリプトを実行する（Python 3.8以上が必要）
   > python saitama_fetch.py

4. 同フォルダに以下の2ファイルが生成されます
   - saitama_market.html  : 市区町村別相場閲覧ページ
   - market_widget.js     : LP埋め込みウィジェット
"""

import urllib.request
import gzip
import json
import os
from collections import defaultdict
from datetime import datetime

# ============================================================
# ★ ここにAPIキーを貼り付けてください
API_KEY = "YOUR_API_KEY_HERE"
# ============================================================

PREFECTURE_CODE = "11"   # 埼玉県

# 取得する期間（直近8四半期）
PERIODS = [
    (2024, 1), (2024, 2), (2024, 3), (2024, 4),
    (2025, 1), (2025, 2), (2025, 3), (2025, 4),
]

# 物件種別ラベル
TYPE_MAP = {
    "宅地(土地と建物)": "中古戸建",
    "中古マンション等":  "マンション",
    "土地(住宅地)":     "土地",
    "土地(その他)":     "土地(その他)",
    "農地":            "農地",
    "林地":            "林地",
}

OUTPUT_HTML   = "saitama_market.html"
OUTPUT_WIDGET = "market_widget.js"


def fetch_data():
    all_records = []
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}

    for year, quarter in PERIODS:
        url = (
            f"https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001"
            f"?year={year}&quarter={quarter}&area={PREFECTURE_CODE}&priceClassification=01"
        )
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
                try:
                    data = json.loads(gzip.decompress(raw))
                except Exception:
                    data = json.loads(raw)
            records = data if isinstance(data, list) else data.get("data", [])
            all_records.extend(records)
            print(f"  {year}年Q{quarter}: {len(records):,}件取得")
        except Exception as e:
            print(f"  {year}年Q{quarter}: エラー ({e})")

    return all_records


def aggregate(records):
    """市区町村×物件種別で平均取引価格・㎡単価・面積を集計"""
    bucket = defaultdict(lambda: {"totals": [], "areas": [], "unit_prices": []})

    for r in records:
        muni  = r.get("Municipality", "不明")
        rtype = r.get("Type", "その他")
        label = TYPE_MAP.get(rtype, rtype)

        trade_price = r.get("TradePrice", "") or ""
        area        = r.get("Area", "")       or ""

        try:
            tp = float(str(trade_price).replace(",", ""))
            ar = float(str(area).replace(",", ""))
            if tp > 0 and ar > 0:
                bucket[(muni, label)]["totals"].append(tp / 10000)        # 万円
                bucket[(muni, label)]["areas"].append(ar)                 # ㎡
                bucket[(muni, label)]["unit_prices"].append(tp / ar / 10000)  # 万円/㎡
        except (ValueError, TypeError):
            pass

    result = defaultdict(dict)
    for (muni, label), v in bucket.items():
        if v["totals"]:
            result[muni][label] = {
                "avg_total": round(sum(v["totals"])       / len(v["totals"])),
                "avg_sqm":   round(sum(v["unit_prices"]) / len(v["unit_prices"]), 1),
                "avg_area":  round(sum(v["areas"])        / len(v["areas"])),
                "count":     len(v["totals"]),
            }

    return dict(result)


def get_data_date():
    """最新四半期から「YYYY年MM月時点」を生成"""
    quarter_to_month = {1: 3, 2: 6, 3: 9, 4: 12}
    latest_year, latest_quarter = PERIODS[-1]
    month = quarter_to_month[latest_quarter]
    return f"{latest_year}年{month:02d}月時点"


def generate_widget_js(aggregated_data, generated_at):
    """market_widget.js を生成（LP埋め込み用）"""
    # 中古戸建 / マンション / 土地 のみ抽出
    widget_data = {}
    for muni, types in aggregated_data.items():
        city = {}
        for key in ["中古戸建", "マンション", "土地"]:
            if key in types:
                d = types[key]
                city[key] = {
                    "avg_total": d["avg_total"],
                    "avg_sqm":   d["avg_sqm"],
                    "avg_area":  d["avg_area"],
                }
        if city:
            widget_data[muni] = city

    data_json = json.dumps(widget_data, ensure_ascii=False)
    data_date = get_data_date()

    return f"""/* =====================================================
   不動産相場ウィジェット（埼玉県）
   出典：国土交通省 不動産情報ライブラリ
   更新: {generated_at}
   ===================================================== */
(function() {{
  var DATA = {data_json};
  var DATA_DATE = "{data_date}";

  var TYPES = [
    {{ key: '中古戸建',  icon: '🏠' }},
    {{ key: 'マンション', icon: '🏢' }},
    {{ key: '土地',      icon: '🟫' }},
  ];

  function fmt(n) {{
    return n.toLocaleString('ja-JP');
  }}

  function render(el) {{
    var city = el.getAttribute('data-city') || '';
    var cityData = DATA[city];
    var rows = '';
    if (cityData) {{
      TYPES.forEach(function(t) {{
        var d = cityData[t.key];
        if (!d) return;
        rows += '<tr>' +
          '<td class="kn-type">' + t.icon + '\\u00a0' + t.key + '</td>' +
          '<td class="kn-total">\\u00a5' + fmt(d.avg_total) + '万</td>' +
          '<td class="kn-unit">\\u00a5' + d.avg_sqm.toFixed(1) + '万/' + d.avg_area + '\\u33a1</td>' +
          '</tr>';
      }});
    }} else {{
      rows = '<tr><td colspan="3" class="kn-nodata">データなし</td></tr>';
    }}
    el.innerHTML =
      '<div class="kn-market-wrap">' +
        '<p class="kn-title">' + city + 'の売却相場</p>' +
        '<p class="kn-source">' + DATA_DATE + '\\u3000|\\u3000出典：国土交通省 不動産情報ライブラリ</p>' +
        '<table class="kn-table">' + rows + '</table>' +
      '</div>';
  }}

  function init() {{
    document.querySelectorAll('.kn-market').forEach(render);
  }}

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', init);
  }} else {{
    init();
  }}
}})();
"""


def generate_html(aggregated_data, generated_at):
    data_json = json.dumps(aggregated_data, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>埼玉県 不動産取引相場</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Hiragino Sans', 'Yu Gothic', sans-serif; background: #f4f6fb; color: #1f2937; }}
  header {{
    background: #fff; border-bottom: 2px solid #2563eb;
    padding: 16px 24px; display: flex; align-items: baseline; gap: 16px;
  }}
  header h1 {{ font-size: 18px; font-weight: 800; color: #1e3a8a; }}
  header span {{ font-size: 12px; color: #6b7280; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 20px 16px; }}

  .filters {{
    display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 18px; align-items: center;
  }}
  .filters label {{ font-size: 12px; color: #6b7280; font-weight: 600; }}
  select, input[type=text] {{
    padding: 7px 12px; border: 1px solid #d1d5db; border-radius: 6px;
    font-size: 13px; background: #fff; color: #111827; outline: none; cursor: pointer;
  }}
  select:focus, input:focus {{ border-color: #2563eb; box-shadow: 0 0 0 2px #dbeafe; }}

  .chart-card {{
    background: #fff; border-radius: 12px; border: 1px solid #e5e7eb;
    padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,.06);
  }}
  .chart-card h2 {{ font-size: 14px; font-weight: 700; color: #374151; margin-bottom: 14px; }}
  .chart-wrapper {{ position: relative; height: 320px; }}

  .table-card {{
    background: #fff; border-radius: 12px; border: 1px solid #e5e7eb;
    overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,.06);
  }}
  .table-header {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 14px 20px; border-bottom: 1px solid #e5e7eb;
  }}
  .table-header h2 {{ font-size: 14px; font-weight: 700; color: #374151; }}
  #recordCount {{ font-size: 12px; color: #6b7280; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{
    background: #f9fafb; text-align: left; padding: 10px 14px;
    font-size: 11px; font-weight: 700; color: #6b7280;
    border-bottom: 1px solid #e5e7eb; white-space: nowrap;
  }}
  td {{ padding: 10px 14px; border-bottom: 1px solid #f3f4f6; }}
  tr:hover td {{ background: #f0f7ff; }}
  .price-cell {{ font-weight: 700; color: #1e3a8a; }}
  .count-cell {{ color: #9ca3af; font-size: 12px; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 600; }}
  .badge-high {{ background: #fee2e2; color: #dc2626; }}
  .badge-mid  {{ background: #fef9c3; color: #ca8a04; }}
  .badge-low  {{ background: #dcfce7; color: #16a34a; }}

  footer {{ text-align: center; font-size: 11px; color: #9ca3af; padding: 20px; }}
</style>
</head>
<body>

<header>
  <h1>埼玉県 不動産取引相場</h1>
  <span>出典：国土交通省 不動産情報ライブラリ ／ データ生成：{generated_at}</span>
</header>

<div class="container">

  <div class="filters">
    <label>物件種別</label>
    <select id="typeFilter" onchange="render()">
      <option value="中古戸建">中古戸建</option>
      <option value="マンション">マンション</option>
      <option value="土地">土地</option>
    </select>
    <label>市区町村検索</label>
    <input type="text" id="searchBox" placeholder="例：さいたま市" oninput="render()">
    <label>並び順</label>
    <select id="sortOrder" onchange="render()">
      <option value="total_desc">平均価格（高い順）</option>
      <option value="total_asc">平均価格（安い順）</option>
      <option value="sqm_desc">㎡単価（高い順）</option>
      <option value="name">市区町村名</option>
    </select>
  </div>

  <div class="chart-card">
    <h2 id="chartTitle">平均㎡単価（万円/㎡）上位20市区町村</h2>
    <div class="chart-wrapper">
      <canvas id="myChart"></canvas>
    </div>
  </div>

  <div class="table-card">
    <div class="table-header">
      <h2>市区町村別 取引相場一覧</h2>
      <span id="recordCount"></span>
    </div>
    <div style="overflow-x:auto">
      <table id="dataTable">
        <thead>
          <tr>
            <th>#</th>
            <th>市区町村</th>
            <th>平均成約価格（万円）</th>
            <th>㎡単価（万円/㎡）</th>
            <th>平均面積（㎡）</th>
            <th>取引件数</th>
            <th>水準</th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </div>
</div>

<footer>国土交通省 不動産情報ライブラリ（reinfolib.mlit.go.jp）の取引価格情報を加工して作成</footer>

<script>
const RAW = {data_json};

let chart = null;

function getFilteredData() {{
  const type  = document.getElementById('typeFilter').value;
  const q     = document.getElementById('searchBox').value.trim();
  const sort  = document.getElementById('sortOrder').value;

  let rows = Object.entries(RAW)
    .filter(([muni]) => !q || muni.includes(q))
    .map(([muni, types]) => {{
      const info = types[type];
      return {{
        muni,
        avg_total: info ? info.avg_total : null,
        avg_sqm:   info ? info.avg_sqm   : null,
        avg_area:  info ? info.avg_area  : null,
        count:     info ? info.count     : 0,
      }};
    }})
    .filter(r => r.avg_total !== null);

  if      (sort === 'total_desc') rows.sort((a,b) => b.avg_total - a.avg_total);
  else if (sort === 'total_asc')  rows.sort((a,b) => a.avg_total - b.avg_total);
  else if (sort === 'sqm_desc')   rows.sort((a,b) => b.avg_sqm   - a.avg_sqm);
  else rows.sort((a,b) => a.muni.localeCompare(b.muni, 'ja'));

  return rows;
}}

function priceLevel(val, allVals) {{
  const sorted = [...allVals].sort((a,b)=>a-b);
  const med = sorted[Math.floor(sorted.length/2)];
  if (val > med * 1.3) return '<span class="badge badge-high">高</span>';
  if (val < med * 0.7) return '<span class="badge badge-low">低</span>';
  return '<span class="badge badge-mid">中</span>';
}}

function render() {{
  const rows = getFilteredData();
  const type = document.getElementById('typeFilter').value;
  const allPrices = rows.map(r => r.avg_total);

  const tbody = document.getElementById('tableBody');
  tbody.innerHTML = rows.map((r, i) => `
    <tr>
      <td class="count-cell">${{i+1}}</td>
      <td><b>${{r.muni}}</b></td>
      <td class="price-cell">${{r.avg_total.toLocaleString('ja-JP')}}万</td>
      <td class="price-cell">${{r.avg_sqm.toFixed(1)}}万/㎡</td>
      <td class="count-cell">${{r.avg_area}}㎡</td>
      <td class="count-cell">${{r.count}}件</td>
      <td>${{priceLevel(r.avg_total, allPrices)}}</td>
    </tr>
  `).join('');

  document.getElementById('recordCount').textContent = `${{rows.length}}市区町村`;

  const top20  = rows.slice(0, 20);
  const labels = top20.map(r => r.muni);
  const values = top20.map(r => r.avg_sqm);

  document.getElementById('chartTitle').textContent =
    `平均㎡単価（万円/㎡）上位${{Math.min(rows.length,20)}}市区町村 ー ${{type}}`;

  if (chart) chart.destroy();
  const ctx = document.getElementById('myChart').getContext('2d');
  chart = new Chart(ctx, {{
    type: 'bar',
    data: {{
      labels,
      datasets: [{{
        label: '㎡単価（万円/㎡）',
        data: values,
        backgroundColor: labels.map((_, i) =>
          i === 0 ? '#1d4ed8' : i < 5 ? '#3b82f6' : '#93c5fd'
        ),
        borderRadius: 4,
      }}]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{ callbacks: {{ label: ctx => ` ${{ctx.parsed.y}} 万円/㎡` }} }}
      }},
      scales: {{
        x: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 11 }}, color: '#374151' }} }},
        y: {{
          grid: {{ color: '#f3f4f6' }},
          ticks: {{ font: {{ size: 11 }}, color: '#6b7280', callback: v => v + '万' }},
          title: {{ display: true, text: '万円/㎡', font: {{ size: 11 }}, color: '#6b7280' }}
        }}
      }}
    }}
  }});
}}

render();
</script>
</body>
</html>"""


def main():
    if API_KEY == "YOUR_API_KEY_HERE":
        print("❌ APIキーが設定されていません。")
        print("   スクリプト内の API_KEY = 'YOUR_API_KEY_HERE' を実際のキーに書き換えてください。")
        print("   APIキー取得: https://www.reinfolib.mlit.go.jp/api/request/")
        return

    print("埼玉県 不動産取引データ取得中...")
    records = fetch_data()
    print(f"\n合計 {len(records):,} 件取得")

    print("集計中...")
    aggregated = aggregate(records)
    print(f"{len(aggregated)} 市区町村のデータを集計")

    generated_at = datetime.now().strftime("%Y年%m月%d日")
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # saitama_market.html 生成
    html = generate_html(aggregated, generated_at)
    html_path = os.path.join(script_dir, OUTPUT_HTML)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ {OUTPUT_HTML} を生成しました")

    # market_widget.js 生成
    widget_js = generate_widget_js(aggregated, generated_at)
    widget_path = os.path.join(script_dir, OUTPUT_WIDGET)
    with open(widget_path, "w", encoding="utf-8") as f:
        f.write(widget_js)
    print(f"✅ {OUTPUT_WIDGET} を生成しました")

    print(f"\n完了！ファイルを確認してください:")
    print(f"  {html_path}")
    print(f"  {widget_path}")


if __name__ == "__main__":
    main()
