# 概要

Gramine-EIM-Synthの状態を把握するためのステータスについて記載.

# 確認方法

// TODO: 準備中につき順次共有

# レスポンス形式（変更可能性あり）

```json
{
	"health": "healthy",
	"server_state": {
        "message": "Server Initialized",
        "status_code": 0
	},
	"version": "v1.2.3"
}
```

# ステータス一覧（変更可能性あり）

| status_code | message | 意味 |
| ---- | ---- | ---- |
| 0 | Server Initialized | 初期状態 |
| 1 | First-File Received | 1つ目のファイルが受理された |
| 2 | First-File Saved | 1つ目のファイルが保存され、2つ目のファイルを受理する準備が整った |
| 3 | Second-File Received | 2つ目のファイルが受理された |
| 4 | ID Matched | 1つ目のファイルと2つ目のファイルのIDマッチングが完了し、学習の準備が整った |
| 5 | Model Trained | マッチング済みデータを元に学習が完了し、学習モデルダウンロードの準備が整った |
