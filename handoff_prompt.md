# 引き継ぎプロンプト：KNホーム 反響獲得プロジェクト

## このプロジェクトの目的
株式会社KNホーム（埼玉県春日部市の不動産会社）の不動産売却LP「https://www.knhome.jp/fudosan-sell/」からの売却相談反響を増やすこと。SEO改善・相場情報コンテンツ・自動化の3本柱で進めている。

---

## 会社情報
- **会社名**: 株式会社KNホーム
- **所在地**: 埼玉県春日部市粕壁東2-9-20
- **電話**: 0800-919-5566（通話無料）
- **メール**: info@knhome.jp / knhome10@gmail.com
- **営業時間**: 10:00〜18:00（定休：火・水曜）
- **対応エリア**: 埼玉県・東京都・千葉県・茨城県・栃木県
- **免許**: 宅地建物取引業 埼玉県知事（5）第20171号
- **実績**: 売買500件超

---

## 作業済みファイル一覧

| ファイル | 場所 | 内容 |
|---|---|---|
| index.html | C:\Users\yukin\KNホーム\fudosan-sell\ | LP本体（修正済み） |
| market_widget.js | C:\Users\yukin\KNホーム\fudosan-sell\ | 埼玉県相場ウィジェット（現在サンプルデータ） |
| seo_report.py | C:\Users\yukin\KNホーム\fudosan-sell\ | Search Console自動レポートスクリプト |
| seo_latest.json | C:\Users\yukin\KNホーム\fudosan-sell\ | 最新SEOデータ（毎週更新） |
| run_seo.bat | C:\Users\yukin\KNホーム\fudosan-sell\ | SEOスクリプト自動起動バッチ |
| client_secret.json | C:\Users\yukin\KNホーム\fudosan-sell\ | Google OAuth認証情報（機密） |
| token.json | C:\Users\yukin\KNホーム\fudosan-sell\ | Google認証トークン（自動更新） |
| saitama_fetch.py | C:\Users\yukin\KNホーム\fudosan-sell\ | reinfolib API取得・ウィジェット生成スクリプト |

---

## 自動化の仕組み（設定済み）

### ① Windowsタスクスケジューラ
- **タスク名**: KNホームSEOレポート
- **実行**: 毎週月曜 08:00
- **内容**: run_seo.bat → seo_report.py を実行 → seo_latest.json と seo_report_YYYYMMDD.html を生成

### ② Coworkスケジュールタスク
- **タスクID**: seo-weekly-report
- **実行**: 毎週月曜 09:00
- **内容**: seo_latest.json を読み込み → 分析 → index.html の改善（メタ説明・FAQ・見出し等）を自動実行 → レポートをチャットに出力

> ※ PCが起動している場合のみ動作。未起動の場合は次回起動時に実行。

---

## 相場ウィジェット（market_widget.js）

### 現状
- 埼玉県内45市区町村のサンプルデータが入っている
- index.html の「春日部市の不動産売却相場情報」セクションに埋め込み済み
- `data-city="春日部市"` で春日部市のデータを表示

### 実データへの切り替え方法（APIキー待ち）
1. reinfolib APIキーが届いたら `saitama_fetch.py` の `API_KEY = "YOUR_API_KEY_HERE"` を書き換える
2. `python saitama_fetch.py` を実行
3. 生成された `market_widget.js` をサーバー（knhome.jp）にアップロード
4. `saitama_market.html` も同時生成される（市区町村別閲覧ページ）

### reinfolib APIの申請状況
- 申請完了済み（5営業日以内にメールで届く）
- 申請URL: https://www.reinfolib.mlit.go.jp/api/request/

### ウィジェット表示フォーマット
```
春日部市の売却相場
2025年12月時点　|　出典：国土交通省 不動産情報ライブラリ
🏠 中古戸建  ¥2,350万  ¥23.5万/100㎡
🏢 マンション ¥1,890万  ¥31.5万/60㎡
🟫 土地      ¥1,940万  ¥19.4万/100㎡
```

---

## SEO現状（2026年7月12日時点）

### 直近28日のSearch Consoleデータ
| URL | 表示回数 | 平均順位 | クリック数 | CTR |
|---|---|---|---|---|
| /fudosan-sell/（LP本体） | 42回 | 15位 | 0 | 0% |
| column/akiya-kasukabe.html | 74回 | 10.3位 | 2 | 2.7% |
| column/akiya-zanchibutsu.html | 54回 | 7.5位 | 0 | 0% |
| column/sozoku-toki-gimuuka.html | 57回 | 57.1位 | 0 | 0% |

### ターゲットキーワード
すべて0表示（まだインデックス未登録または圏外）
- 春日部 不動産売却 / 春日部 空き家 売却 / 春日部 相続 不動産
- 春日部 不動産 査定 / 春日部 空き家 買取 / 埼玉 空き家 売却

### 実施済みSEO改善
1. メタディスクリプション更新（電話番号・差別化ポイントを前半に）
2. FAQ2項目追加（「春日部で不動産売却する場合まず何をすべきか」「売却費用の目安」）
3. schema.org FAQPageに同内容追記

---

## 今後の優先タスク

### 直近（今すぐできること）
- [ ] `column/akiya-zanchibutsu.html` のメタディスクリプション改善（7.5位で0クリックは要対策）
- [ ] Google Search Consoleで「実際にどんなキーワードでLPが表示されているか」確認 → 監視キーワードを追加

### reinfolib APIキー到着後
- [ ] `saitama_fetch.py` にAPIキーをセット → 実行 → market_widget.js を実データに更新 → サーバーにアップロード

### 中期（1〜2ヶ月）
- [ ] コラムページの追加（「春日部市の空き家売却完全ガイド」等）
- [ ] 内部リンク強化（LP ↔ コラムページ間）
- [ ] LINEでの相談導線追加（index.html内にコメントアウトで準備済み）

---

## Google OAuth認証情報
- **プロジェクト**: My First Project（Google Cloud Console）
- **クライアントID**: 330041231282-r5874u8dggsql0los5fglpkbsfrg9vsp.apps.googleusercontent.com
- **token.json**: 認証済み・自動更新（knhome10@gmail.com）
- **スコープ**: webmasters.readonly（Search Console読み取り専用）

---

## 技術メモ

### index.html の構造
```
nav → hero → worries → voices → features → cases → flow → targets
→ price-info（相場ウィジェット埋め込み済み） → faq → cta/contact → footer
```

### CSSカラー変数
```css
--navy: #1a3a2a  --navy-mid: #2d6a4f  --gold: #c8981a
```

### market_widget.js の埋め込み方法
```html
<!-- 表示したい場所に設置 -->
<div class="kn-market" data-city="川口市"></div>
<!-- bodyの閉じタグ直前 -->
<script src="market_widget.js"></script>
```

### seo_latest.json のデータ構造
```json
{
  "generated_at": "YYYY年MM月DD日",
  "site_url": "https://www.knhome.jp/fudosan-sell/",
  "keywords": { "キーワード": { "clicks": 0, "impressions": 0, "position": 0, "ctr": 0 } },
  "top_pages": [ { "url": "...", "clicks": 0, "impressions": 0, "position": 0, "ctr": 0 } ]
}
```
