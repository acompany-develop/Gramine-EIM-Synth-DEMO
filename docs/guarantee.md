# 概要

# 動作確認済み条件
- OS
    - Ubuntu22.04
- CPU
    - x86/64 Intel Cascade Lake CPU (n2-standard-16)
- メモリ
    - 64GB以上

# 操作要件
* `demo_docker/docker-compose.yaml`経由でのリクエストのみを保証（順次保証範囲を拡張）

# csv要件
* 行数1,000万行以下（header行を除く）
* 列数1列以上10列以下（共通ID列を除く）
* headerに書かれた各属性名の値が1文字以上20文字以下
* headerを除く各属性列の値が1文字以上5文字以下
* headerに書かれた属性名が重複していない
* 共通ID列の値が重複していない
* 利用可能文字を`,`で区切ったCSV形式になっている
* headerを含めた全ての行で`,`の個数が同じ

備考:
* 最左列をマッチングに利用する共通ID列として扱う
* 最上行をheader行として扱う

# 利用可能文字
入力するCSVには以下の文字が利用可能（以下に加えて区切り文字として `,` を利用する）  

```
digits (0123456789)
uppercase letters (ABCDEFGHIJKLMNOPQRSTUVWXYZ)
lowercase letters (abcdefghijklmnopqrstuvwxyz)
punctuation characters (._-)
```
// TODO: 記号のサポート文字は将来的に拡張予定

# 動作保証されていないcsvの例
準備中
