# 公開ガイド（itch.io ／ Google Play）

ゲームURL： https://yocchandayyo.github.io/parfait-curling/

---

## A. itch.io で公開（一番かんたん・テスター要件なし・今日できる）

itch.io はインディーゲーム定番のプラットフォーム。Webゲームをそのまま公開でき、無料・投げ銭設定も可能。

### 手順
1. https://itch.io/register でアカウント作成（無料）
2. 右上メニュー → **Upload new project**
3. 入力：
   - **Title**： `Fruit Parfait Game`
   - **Short description**： `promo/marketing.md` の itch.io短文をコピー
   - **Classification**： Games
   - **Kind of project**： **HTML**（重要）
   - **Pricing**： `No payments`（無料）or `Donation`（投げ銭）
4. **Uploads**：2通りのどちらか
   - (簡単) 外部リンクにする：Embed しない場合は Description に Play リンクを貼るだけでもOK
   - (推奨) ゲームを zip にしてアップ → itch内で直接プレイ可能にする
     - `food-travel-merge` フォルダの中身（index.html, assets/, *.png, *.js 等）を zip 化してアップロード
     - **This file will be played in the browser** にチェック
     - Embed options：Width `460` / Height `820`（縦長）、`Mobile friendly` ON、`Fullscreen button` ON
5. **Cover image**： `promo_itch_cover.png` をアップロード（630×500）
6. **Screenshots**： `store/store-1〜3.png` をアップロード
7. **Save & view page** → 問題なければ **Visibility を Public** に

> 注意：itch内アップ版は同じドメインで動かないため、オンラインランキング（Firebase）が動くか確認を。動かない場合は「Description に Play リンクを貼って、本体は GitHub Pages で遊んでもらう」形が確実です。

---

## B. Google Play（本人確認の完了後に本番、準備は今から可能）

### 状況
- デベロッパー登録済み（アカウント名 Maccha_ore、個人用）
- **本人確認 審査中**（数日かかることあり、完了でメール）
- **個人アカウントはクローズドテスト（テスター12〜20人・14日間）が本番公開の前提**

### 今からできる準備
1. 電話番号の確認を完了（ホームの「詳細を表示」）
2. **アプリを作成**（最初のアプリの作成 → アプリ名 `Fruit Parfait Game`、言語、無料、ゲーム）
3. **ストアの設定** に素材を登録：
   - アプリ名： `Fruit Parfait Game`
   - 簡単な説明 / 詳しい説明： `promo/marketing.md`・英日の説明文
   - アプリアイコン： `icon-512.png`
   - フィーチャーグラフィック： `feature-graphic.png`
   - スクリーンショット： `store/store-1〜3.png`
   - プライバシーポリシー： https://yocchandayyo.github.io/parfait-curling/privacy.html
4. **アプリのコンテンツ**（必須アンケート）を回答：
   - プライバシーポリシーURL、広告の有無（なし）、データセーフティ（ニックネーム・スコアを収集／Firebase）、対象年齢、コンテンツのレーティング
5. **クローズドテスト**トラックを作成 → **AAB（fruit parfait game.aab）をアップロード**
6. テスターのメールリスト（Googleアカウント）を登録 → **オプトインURL**が発行される
7. テスターに参加してもらう（→ `promo/marketing.md` のテスター募集文）

### 本番公開まで
クローズドテスト（12〜20人・14日継続）→ 「本番アクセスの申請」→ 審査 → 公開

> 正確な必要テスター人数は Play Console の画面に表示されます。そこで確認を。

---

## C. テスターの集め方（友達ゼロでもOK）
- **相互テストコミュニティ**：Reddit `r/googleplaytesters` / `r/androiddev`、Discord・Telegram の "20 testers" 系グループ
- **SNS / note で告知**：Web版で遊んでくれた人に「Playテストも手伝って」と依頼
- 募集文は `promo/marketing.md` の 5・6 を使用
