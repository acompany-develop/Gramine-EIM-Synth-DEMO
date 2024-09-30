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
1. 各事業者ごとにGramine-EIM-Synthを取得するためのデータを用意する。
2. `demo_docker/bind/Client0/data/`直下に `*.csv`の形式で配置しておく。
3. `demo_docker/docker-compose.yaml`内にある`source: bind/Client{0,1}/data/sample_data.csv`部分の`sample_data.csv`を、新たに配置したcsvの名前に変更。

データの形式: [data_in_out.md](../docs/data_in_out.md)  
データの詳しい動作保証要件: [guarantee.md](../docs/guarantee.md)

# 実行
## Dockerでの実行
**※ 実際にGramine Serverに対して通信しにいくため事前にGramine Serverが起動していることをGramine Server管理者に確認する。**

```bash
$ cd demo_docker
$ docker compose up
```

## バイナリでの実行
// TODO: バイナリ形式での利用は将来的にサポート予定
