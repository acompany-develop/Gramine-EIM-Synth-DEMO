# 概要

Gramine-EIM-Synthの状態を把握するためのステータスについて記載。

# 確認方法
```
$ curl <IP>:8080/info
```
※ http未対応につきhttpsで叩くと想定外挙動になるため注意

# レスポンス形式（変更可能性あり）
以下の形式のjson文字列が返ってくる。（実際は改行なし）
```json
{
    "health": "healthy",
    "server_state": 
    {
        "message": "Server Initialized",
        "status_code": 0
    },
    "version": "v1.0.5"
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
| 5 | Model Training | マッチング済みデータを元に学習が実行中 |
| 6 | Model Trained | マッチング済みデータを元に学習が完了し、学習モデルダウンロードの準備が整った |
| -1 | Status Unknown | 想定外の状態 |

## ステータスの遷移イメージ（変更可能性あり）
Clientが `matching`, `synth` バイナリを実行した時のServerの状態遷移図。  
```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant DB

    note left of Client: ./matching csv1
    Client->>+Server: GET /info (Check Server Status)
    Server->>DB: Get STATUS
    alt STATUS = Server Initialized
        Server-->>Client: STATUS = Server Initialized
        Client->>Server: POST /matching/send_data (First CSV)
        Server->>DB: Update STATUS to FIRST_FILE_RECEIVED
        Server->>DB: Save CSV1
        Server->>DB: Update STATUS to FIRST_FILE_SAVED
        Server-->>Client: 200 OK
    else STATUS != Server Initialized
        Server-->>-Client: Error or Different Status
    end

    note left of Client: ./matching csv2
    Client->>+Server: GET /info (Check Server Status)
    Server->>DB: Get STATUS
    alt STATUS = FIRST_FILE_SAVED
        Client->>Server: POST /matching/send_data (Second CSV)
        Server->>DB: Update STATUS to SECOND_FILE_RECEIVED
        Server-->>Client: STATUS = FIRST_FILE_SAVED
        DB->>Server: Read CSV1
        Server->>Server: Perform Matching
        Server->>DB: Save Matching Result
        Server->>DB: Update STATUS to ID_MATCHED
        Server-->>Client: 200 OK
    else STATUS = FIRST_FILE_RECEIVED
        loop until STATUS = FIRST_FILE_SAVED
            Client->>Server: GET /info (Check if First-File Saved)
            Server->>DB: Get STATUS
            Server-->>Client: STATUS = FIRST_FILE_RECEIVED
        end
        Server-->>Client: STATUS = FIRST_FILE_SAVED
        Client->>Server: POST /matching/send_data (Second CSV)
        Server->>DB: Update STATUS to SECOND_FILE_RECEIVED
        DB->>Server: Read CSV1
        Server->>Server: Perform Matching
        Server->>DB: Save Matching Result
        Server->>DB: Update STATUS to ID_MATCHED
        Server-->>Client: 200 OK
    else STATUS != FIRST_FILE_SAVED
        Server-->>-Client: Error or Different Status
    end

    note left of Client: ./synth
    Client->>+Server: GET /info (Check for ID Matched)
    Server->>DB: Get STATUS
    alt STATUS = ID_MATCHED
        Server-->>Client: STATUS = ID_MATCHED
        Client->>Server: GET /synth/train
        Server->>DB: Update STATUS to TRAINING
        Server->>Server: Start Model Training
    else STATUS != ID_MATCHED
        Server-->>Client: Error or Different Status
    end

    loop until status = TRAINED
        Client->>Server: GET /info (Check for Model Training)
        Server-->>Client: STATUS = TRAINING
    end

    Client->>Server: GET /synth/model
    Server->>DB: Retrieve Model
    Server->>Client: Return Model (Base64 Encoded)
    Server->>-DB: Clear DB and Intermediate Files
```