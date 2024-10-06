# 概要
Gramine-EIM-Synthを実行する方法について記載。
Gramine Serverが立ち上がっている状態で2つのClientがそれぞれ実行する必要があることに注意。

# 前準備
## 設定ファイルの用意

通信や認証の設定を記載した設定ファイルを用意する。
設定ファイルは事業者ごとに用意する。

フォーマットはdemo_dockerの設定ファイルを参照。
- [settings.ini](../demo_docker/bind/Client0/settings.ini)

設定ファイルのうち以下の値はGramine Serverに依存して決まるため、検証用Gramine Serverを利用したい場合はAcompanyの担当者から配布された値を設定する。

```ini
[sp]
; Gramine Serverのポートとホスト名を設定する。
SERVER_PORT = ; 検証用環境の`SERVER_PORT`が必要な場合はAcompanyの担当者に問い合わせてください。
SERVER_NAME = ; 検証用環境の`SERVER_NAME`が必要な場合はAcompanyの担当者に問い合わせてください。

; Gramine Serverで動作するEnclaveのMRENCLAVEとMRSIGNERを指定する。
REQUIRED_MRENCLAVE = ; 検証用環境の`REQUIRED_MRENCLAVE`が必要な場合はAcompanyの担当者に問い合わせてください。
REQUIRED_MRSIGNER = ; 検証用環境の`REQUIRED_MRSIGNER`が必要な場合はAcompanyの担当者に問い合わせてください。
```

以下のRAに関する設定は各Firmが個別で行う必要がある。
いくつかの値については推奨値が書き込まれているので基本的には変更不要。
```ini
; Gramine Serverに要求するEnclaveの最小Gramine ServerSVN（Security Version Number）を設定。
; Gramine Server側はEnclave設定XMLでこれを設定できる。
MINIMUM_Gramine ServerSVN = 0

; Gramine Serverに要求するEnclaveのProduct IDを設定。
; Gramine Server側はEnclave設定XMLでこれを設定できる。
REQUIRED_Gramine Server_PROD_ID = 0

; TCBステータスについてのRA受理条件の設定を行う。0で不許可とし、1で許可する。
;; DEBUG版Enclaveの許可
ALLOW_DEBUG_ENCLAVE_INSECURE = 1
;; TCBレベルがOut-of-DateであるようなEnclaveの許可
ALLOW_OUTDATED_TCB_INSECURE = 1
;; CONFIGURATION_NEEDEDであるようなEnclaveの許可
ALLOW_HW_CONFIG_NEEDED = 1
;; SW_HARDENING_NEEDEDであるようなEnclaveの許可
ALLOW_SW_HARDENING_NEEDED = 1
```

## データの用意
1. 各事業者ごとにGramine-EIM-Synthを取得するためのデータを用意
2. `demo_docker/bind/Client0/data/`直下に `*.csv`の形式で配置
3. `demo_docker/docker-compose.yaml`内にある`source: bind/data/100_a.csv`を、入力したいcsvファイルのパスに変更

データの形式: [data_in_out.md](../docs/data_in_out.md)  
データの詳しい動作保証要件: [guarantee.md](../docs/guarantee.md)

# 実行
## Dockerでの実行
**※ 実際にGramine Serverに対して通信しにいくため事前にGramine Serverが起動していることをGramine Server管理者に確認する。**

```bash
$ cd demo_docker
$ make run # `docker compose down -v && docker compose up`と同じ
```

なお、ctrl+c等で途中で中断すると、server_statusが `Server Initialized` ではない状態で異常終了してしまうため注意。
異常終了した場合は、以下の `/stop`を叩くことでserverを再起動することにより初期化可能。（成果物も全て削除されます）

```bash
$ curl http://<IP>:8080/info
{"health":"healthy","server_state":{"message":"Model Training","status_code":5},"version":"v0.0.1"}
$ curl http://<IP>:8080/stop
receive stop
$ curl http://<IP>:8080/info # しばらく待ってから/infoを叩くと以下のようになる
{"health":"healthy","server_state":{"message":"Server Initialized","status_code":0},"version":"v0.0.1"}
```

## バイナリでの実行
// TODO: バイナリ形式での利用は将来的にサポート予定  
// 以下は現在予定している実行手順
`./matching <設定ファイルのパス> <入力csvのパス>` でcsvを送信   
`./synth <設定ファイルのパス> <出力modelのパス>` で学習を行いモデルを取得  
[シーケンス図](../docs/server_state.md#ステータスの遷移イメージ)も参照

### 実行中の処理を強制終了した場合
クライエントがCtrl+Cなどによって処理を途中で終了させた場合、サーバがリクエストを正しく捌けなくなることがある。
異常な挙動が起きた場合は、[/stop](#stop) API を用いてサーバを停止させる。
停止したサーバは自動で再起動されて正常状態に戻る。

このリクエストも通らない場合は手動でサーバを再起動させる必要があるため管理者に連絡する。

# API
## /info
**※ 適切な証明書があればinsecureオプションはつけなくて良い**  
```console
$ curl <IP>:8080/info
```
Server が正常に動いていれば
```
{"health":"healthy","server_state":{"message":"Model Training","status_code":5},"version":"v0.0.1"}
```
という文章が返ってくる。

server_stateの取り得る値については、[server_state.md](server_state.md) を参照。

## /healthcheck
**※ 適切な証明書があればinsecureオプションはつけなくて良い**  
```console
$ curl <IP>:8080/healthcheck
```
Server が正常に動いていれば
```
Gramine-EIM-Synth Server is Running.
```
という文章が返ってくる。

## /stop
Gramine Serverを停止できる。
停止したサーバは自動で再起動されるため、[実行中の処理を強制終了した場合](#実行中の処理を強制終了した場合) などサーバの状態をリセットしたい時に使う。
```console
$ curl <IP>:8080/stop
```

# 備考
> <font color="Red">[!IMPORTANT]</font>  
> `make run`実行時、標準出力とファイル出力でログを出力するが、障害調査時に`.logs/`の提出を依頼する可能性がある。
