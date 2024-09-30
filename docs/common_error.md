# 概要
Client 側に出るエラーメッセージとその考えられる原因について解説する。

原因を示す行は`ERROR:`を含む以下のformatで出力される。
```
<timestamp> | ERROR: | <type> | <file>:<function> - <target> | <error message>
```
以下では`<error message>`のみ抜粋する。
# エラーメッセージ
準備中