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
**※ 実際にserverに対して通信しにいくため、接続先環境と接続情報は管理者に連絡し、[前準備](#前準備) を参考に設定を行うこと。**

## Dockerでの実行方法
```bash
$ cd demo_docker
$ make run
```

### 注意事項
amd64でコンパイルしたバイナリを実行するために、platformを`linux/amd64`に指定しています。この指定下でarm64ベースのmacを使用する場合[Dockerイメージのビルドに失敗するため、Docker DesktopにおいてRossetaを無効化](https://github.com/docker/for-mac/issues/7255)してください。



## バイナリでの実行方法
### 前準備
※ 以下、`${VERSION}`部分は`x.x.x`の形式で有効なバージョンを指定してください。有効なバージョン一覧は[こちら](https://github.com/acompany-develop/Gramine-EIM-Synth-DEMO/tags)を参照。

以下のzipをダウンロードして展開し、依存ライブラリを環境内に配置する。
```bash
$ wget https://github.com/acompany-develop/Gramine-EIM-Synth-DEMO/releases/download/${VERSION}/lib-v${VERSION}-linux-x64.zip
$ unzip lib-v${VERSION}-linux-x64.zip
$ cp sgx_default_qcnl.conf /etc/sgx_default_qcnl.conf
$ mkdir -p /usr/lib/x86_64-linux-gnu/ && cp -r usr-lib-x86_64-linux-gnu/* /usr/lib/x86_64-linux-gnu/
$ mkdir -p /usr/local/lib/x86_64-linux-gnu/ && cp -r usr-local-lib-x86_64-linux-gnu/* /usr/local/lib/x86_64-linux-gnu/
```

以下のzipをダウンロードして展開し、実行用バイナリを配置する。
```bash
$ wget https://github.com/acompany-develop/Gramine-EIM-Synth-DEMO/releases/download/${VERSION}/Gramine-EIM-Synth-v${VERSION}-linux-x64.zip
$ unzip Gramine-EIM-Synth-v${VERSION}-linux-x64.zip
```

### 実行方法
```bash
# csv送信
$ ./matching <設定ファイルのパス> <入力csvのパス> 
# 学習&モデル取得
$ ./synth <設定ファイルのパス> <出力modelのパス(任意)>
```

### 注意事項
arm64ベースのmacを使用する場合、SIP(System Integrity Protection)が有効なため、後述の`/usr`ディレクトリにファイルを配置することはできません。クラウドでamd64ベースのインスタンスを立てるか、上記のDockerを用いる方法を利用してください。

## 全体注意事項
### 実行中の処理を中断した場合
クライエントがCtrl+Cなどによって処理を途中で終了させた場合、サーバがリクエストを正しく捌けなくなることがある。
異常な挙動が起きた場合は、[/stop](#stop) API を用いてサーバを停止させる。
停止したサーバは自動で再起動されて正常状態に戻る。

```bash
# serverの状態を確認
$ curl http://<IP>:8080/info
{"health":"healthy","server_state":{"message":"Model Training","status_code":5},"version":"v0.0.1"}
# serverを強制再起動
$ curl http://<IP>:8080/stop
receive stop
# serverの状態を確認（しばらく待ってから/infoを叩くと以下のようになる）
$ curl http://<IP>:8080/info
{"health":"healthy","server_state":{"message":"Server Initialized","status_code":0},"version":"v0.0.1"}
```

このリクエストも通らない場合は手動でサーバを再起動させる必要があるため管理者に連絡する。

### docker-composeを複数端末で実行した場合
同じマシン内で複数terminalで同時に実行すると、リソース名が競合し、想定外挙動になる。そのため、必ずリnetwork名、service名、volume名等を全て変更して実行すること。

### 想定外の問題が発生した場合
`make run`実行時、標準出力とファイル出力でログを出力している。
障害調査時には`demo_docker/.logs/`の提出を依頼する可能性がある。

# server操作用API仕様
## /info
```console
$ curl <IP>:8080/info
```
Server が正常に動いていれば
```
{"health":"healthy","server_state":{"message":"Model Training","status_code":5},"version":"v0.0.1"}
```
という文章が返ってくる。

server_stateの取り得る値については、[ステータス一覧](../docs/server_state.md#ステータス一覧（変更可能性あり）)を参照

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

## 注意事項
> <font color="Red">[!IMPORTANT]</font>  
> `/info`, `/healthcheck`, `/stop`をリクエストする際は、想定外の挙動が起きる可能性があるためhttpsではなくhttpを利用してください。
