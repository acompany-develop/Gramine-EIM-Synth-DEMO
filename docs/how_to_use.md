# 概要
Gramine-EIM-Synthを実行する方法について記載．  
Dockerによるデモを実行する [demo_docker](../../demo_docker/README.md) も参考．

Gramine Serverが立ち上がっている状態で2つのClientがそれぞれ実行する必要があることに注意．

# 前準備
## 設定ファイルの用意

通信や認証の設定を記載した設定ファイルを用意する．
設定ファイルは事業者ごとに用意する．
ファイル名や配置場所は何でも良い．

フォーマットはdemo_dockerの設定ファイルを参照．
- [settings.ini](../../demo_docker/bind/Client0/settings.ini)

設定ファイルのうち以下の値はGramine Serverに依存して決まるため、検証用Gramine Serverを利用したい場合はAcompanyの担当者から配布された値を設定する．

```ini
[sp]
; Gramine Serverのポートとホスト名を設定する。
SERVER_PORT = ; 検証用環境の`SERVER_PORT`が必要な場合はAcompanyの担当者に問い合わせてください。
SERVER_NAME = ; 検証用環境の`SERVER_NAME`が必要な場合はAcompanyの担当者に問い合わせてください。

; Gramine Serverで動作するEnclaveのMRENCLAVEとMRSIGNERを指定する。
REQUIRED_MRENCLAVE = ; 検証用環境の`REQUIRED_MRENCLAVE`が必要な場合はAcompanyの担当者に問い合わせてください。
REQUIRED_MRSIGNER = ; 検証用環境の`REQUIRED_MRSIGNER`が必要な場合はAcompanyの担当者に問い合わせてください。
```

以下のRAに関する設定は各Firmが個別で行う必要がある．
いくつかの値については推奨値が書き込まれている．
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
各事業者ごとにGramine-EIM-Synthを取得するためのデータを用意する．
ファイル名や配置場所は何でも良い． 

データの形式 : [data_in_out.md](./data_in_out.md)  
データの詳しい動作保証要件 : [guarantee.md](./guarantee.md)

## バイナリなどの取得
// TODO: Docker
# 実行
**※ 実際にGramine Serverに対して通信しにいくため事前にGramine Serverが起動していることをGramine Server管理者に確認する．**  
// TODO: Docker


## ステータスコード

| 項目 | 説明 |
| --- | --- |
| $0$ | クロス集計表が正常に出力されました． |
| $134$ |エラーが発生しました． |

## 実行時の注意
準備中
### 実行中の処理を強制終了した場合
クライエントがCtrl+Cなどによって処理を途中で終了させた場合，サーバがリクエストを正しく捌けなくなることがある．
異常な挙動が起きた場合は，[/stop](#stop) API を用いてサーバを停止させる．
停止したサーバは自動で再起動されて正常状態に戻る．

このリクエストも通らない場合は手動でサーバを再起動させる必要があるため管理者に連絡する．

# API
## /healthcheck
**※ 適切な証明書があればinsecureオプションはつけなくて良い**  
```console
$ curl --insecure <IP>:<port>/healthcheck
```
Server が正常に動いていれば
```
Gramine-EIM-Synth Server is Running.
```
という文章が返ってくる。

## /stop
Gramine Serverを停止できる．
停止したサーバは自動で再起動されるため，[実行中の処理を強制終了した場合](#実行中の処理を強制終了した場合) などサーバの状態をリセットしたい時に使う．
```console
$ curl --insecure <IP>:<port>/stop
```

# 備考
> <font color="Red">[!IMPORTANT]</font>  
> Firmは実行時に標準出力とファイル出力でログを出力するが，ファイル出力先はbinary実行ディレクトリ内の`.logs/`ディレクトリに固定されている．障害調査時に`.logs/`の提出を依頼する可能性がある．
