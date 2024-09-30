# 概要
Gramine-EIM-Synthを実行する方法について記載．  

Gramine Serverが立ち上がっている状態で2つのClientがそれぞれ実行する必要があることに注意．

# 実行手順
demo_dockerの[前準備](../demo_docker/README.md#前準備)、[実行](../demo_docker/README.md#実行) を参考．

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
