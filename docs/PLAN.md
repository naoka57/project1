# フライト・ホテル予約ツール 計画書

## 概要

出発時に最安値のフライトとホテルを検索・予約できるWebアプリケーション。
ユーザーが出発地・目的地・日程を入力すると、最安の組み合わせを提示し、そのまま予約まで行える。

---

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| 言語 | Python 3.11+ |
| Webフレームワーク | FastAPI |
| フロントエンド | Jinja2テンプレート + HTMX (軽量SPA風) |
| データベース | SQLite (開発) / PostgreSQL (本番) |
| ORM | SQLAlchemy |
| タスクキュー | Celery + Redis (非同期検索用) |
| テスト | pytest |
| パッケージ管理 | pip + requirements.txt |

## 外部API連携

| API | 用途 | 備考 |
|-----|------|------|
| Amadeus for Developers | フライト検索・予約 | 無料テスト環境あり |
| Booking.com Affiliate API | ホテル検索・予約 | アフィリエイト登録が必要 |

※ 開発初期はAmadeus Test APIの無料枠で開発を進める

---

## アーキテクチャ

```
┌─────────────────────────────────────────┐
│            ブラウザ (HTMX)              │
└────────────────┬────────────────────────┘
                 │ HTTP
┌────────────────▼────────────────────────┐
│           FastAPI サーバー               │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ 検索API  │ │ 予約API  │ │ 認証    │ │
│  └────┬─────┘ └────┬─────┘ └─────────┘ │
│       │            │                    │
│  ┌────▼────────────▼──────────────────┐ │
│  │       サービス層                    │ │
│  │  ┌────────────┐ ┌───────────────┐  │ │
│  │  │FlightSvc   │ │ HotelSvc      │  │ │
│  │  └─────┬──────┘ └──────┬────────┘  │ │
│  │        │               │           │ │
│  │  ┌─────▼──────┐ ┌──────▼────────┐  │ │
│  │  │AmadeusAPI  │ │BookingAPI     │  │ │
│  │  │Client      │ │Client         │  │ │
│  │  └────────────┘ └───────────────┘  │ │
│  └────────────────────────────────────┘ │
│       │                                 │
│  ┌────▼────────────────────────────────┐│
│  │     SQLAlchemy (DB)                 ││
│  │  ・検索履歴  ・予約情報  ・ユーザー  ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

---

## ディレクトリ構成

```
project1/
├── docs/
│   └── PLAN.md
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPIアプリ エントリーポイント
│   ├── config.py               # 設定管理 (API キー等)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # ユーザーモデル
│   │   ├── booking.py          # 予約モデル
│   │   └── search.py           # 検索履歴モデル
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── flight.py           # フライト リクエスト/レスポンス
│   │   ├── hotel.py            # ホテル リクエスト/レスポンス
│   │   └── booking.py          # 予約 リクエスト/レスポンス
│   ├── services/
│   │   ├── __init__.py
│   │   ├── flight_service.py   # フライト検索ロジック
│   │   ├── hotel_service.py    # ホテル検索ロジック
│   │   ├── booking_service.py  # 予約処理
│   │   └── optimizer.py        # 最安値最適化ロジック
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── amadeus_client.py   # Amadeus API クライアント
│   │   └── booking_client.py   # Booking.com API クライアント
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── search.py           # 検索エンドポイント
│   │   ├── booking.py          # 予約エンドポイント
│   │   └── auth.py             # 認証エンドポイント
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html          # 検索フォーム
│   │   ├── results.html        # 検索結果一覧
│   │   └── booking.html        # 予約確認画面
│   └── static/
│       ├── css/
│       └── js/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_flight_service.py
│   ├── test_hotel_service.py
│   ├── test_optimizer.py
│   └── test_routers.py
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 機能一覧と開発フェーズ

### Phase 1: 基盤構築（MVP）
1. **プロジェクトセットアップ** - FastAPI, ディレクトリ構成, 設定管理
2. **Amadeus APIクライアント** - フライト検索の実装
3. **フライト検索API** - 出発地・目的地・日付でフライトを検索
4. **最安値ソート** - 価格順でソートして最安を提示
5. **検索UI** - 基本的な検索フォームと結果表示

### Phase 2: ホテル統合
6. **Booking.com APIクライアント** - ホテル検索の実装
7. **ホテル検索API** - 目的地・日付でホテルを検索
8. **フライト+ホテル最安値最適化** - 合計金額が最安の組み合わせを算出
9. **統合検索UI** - フライトとホテルを一覧で表示

### Phase 3: 予約機能
10. **ユーザー認証** - サインアップ・ログイン
11. **予約処理** - フライト・ホテルの予約APIとの連携
12. **予約履歴** - DBへの保存と履歴表示
13. **予約確認メール** - 予約完了通知

### Phase 4: 改善
14. **検索結果キャッシュ** - 同一条件の再検索を高速化
15. **価格アラート** - 指定ルートが値下がりしたら通知
16. **レスポンシブUI** - モバイル対応

---

## データモデル

### SearchHistory (検索履歴)
| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | 主キー |
| user_id | UUID | FK → User |
| origin | VARCHAR(3) | 出発地 (IATA空港コード) |
| destination | VARCHAR(3) | 目的地 (IATA空港コード) |
| departure_date | DATE | 出発日 |
| return_date | DATE | 帰国日 (nullable) |
| adults | INT | 大人の人数 |
| created_at | DATETIME | 検索日時 |

### Booking (予約)
| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | 主キー |
| user_id | UUID | FK → User |
| booking_type | ENUM | "flight" / "hotel" |
| external_booking_id | VARCHAR | 外部API側の予約ID |
| total_price | DECIMAL | 合計金額 |
| currency | VARCHAR(3) | 通貨 (JPY, USD等) |
| status | ENUM | "confirmed" / "cancelled" / "pending" |
| details | JSON | 予約詳細 (フライト情報/ホテル情報) |
| created_at | DATETIME | 予約日時 |

### User (ユーザー)
| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | 主キー |
| email | VARCHAR | メールアドレス |
| hashed_password | VARCHAR | ハッシュ化パスワード |
| name | VARCHAR | 表示名 |
| created_at | DATETIME | 登録日時 |

---

## API エンドポイント

### 検索
| メソッド | パス | 説明 |
|----------|------|------|
| GET | `/api/flights/search` | フライト検索 |
| GET | `/api/hotels/search` | ホテル検索 |
| GET | `/api/search/combined` | フライト+ホテル最安値検索 |

### 予約
| メソッド | パス | 説明 |
|----------|------|------|
| POST | `/api/bookings` | 予約作成 |
| GET | `/api/bookings` | 予約一覧 |
| GET | `/api/bookings/{id}` | 予約詳細 |
| DELETE | `/api/bookings/{id}` | 予約キャンセル |

### 認証
| メソッド | パス | 説明 |
|----------|------|------|
| POST | `/api/auth/register` | ユーザー登録 |
| POST | `/api/auth/login` | ログイン |

### 画面 (HTML)
| メソッド | パス | 説明 |
|----------|------|------|
| GET | `/` | 検索画面 |
| GET | `/results` | 検索結果画面 |
| GET | `/booking/{id}` | 予約確認画面 |
| GET | `/history` | 予約履歴画面 |

---

## 最安値最適化ロジック

```python
# optimizer.py の基本アルゴリズム

def find_cheapest_combination(flights, hotels):
    """
    フライトとホテルの最安組み合わせを返す。

    1. フライトを価格昇順でソート
    2. ホテルを1泊あたりの価格昇順でソート
    3. フライト価格 + (ホテル1泊価格 × 泊数) の合計が最安の組み合わせを選出
    4. 上位N件を返却
    """
    combinations = []
    for flight in flights:
        for hotel in hotels:
            nights = (flight.return_date - flight.departure_date).days
            total = flight.price + (hotel.price_per_night * nights)
            combinations.append({
                "flight": flight,
                "hotel": hotel,
                "total_price": total,
            })
    combinations.sort(key=lambda x: x["total_price"])
    return combinations[:10]  # 上位10件
```

---

## 環境変数 (.env)

```
AMADEUS_API_KEY=your_api_key
AMADEUS_API_SECRET=your_api_secret
BOOKING_API_KEY=your_api_key
DATABASE_URL=sqlite:///./dev.db
SECRET_KEY=your_secret_key
```

---

## 次のステップ

この計画書の承認後、**Phase 1（基盤構築・MVP）** から実装を開始します。
まずはプロジェクトセットアップとAmadeus APIクライアントの構築から着手します。
