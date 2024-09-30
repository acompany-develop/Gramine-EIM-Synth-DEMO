# 入力形式

- カンマ(,)区切りのCSV
- 1行目にはheaderを記載
- 1列目にはマッチングで突合に用いるID列を記載
- 2列目以降には属性を記載

### 例
```csv
ID,height,weight
id1,170,70
id2,180,60
id3,170,60
```

入力ファイルの動作保証要件については[guarantee.md](guarantee.md)を参照  

# 出力形式
## 保存対象
連合学習による継続学習を行えるように改修された synthcity で定義された `CustomCTGANPlugin` のインスタンス
## 保存形式
pickle (cloudpickle)
## 保存方法
`synthcity.utils.serialization.save_to_file` を使用
## 読込方法 (推奨)
`synthcity.utils.serialization.load_from_file` を使用

読込に成功すれば CustomCTGANPlugin のインスタンスが一部のインスタンス変数を除いて復元される (注意点も参照)。
## 注意点
### モジュールの階層について
`synthcity.utils.serialization.load_from_file` を用いてモデルを読み込む際は、読込み操作の実装が書かれたファイルと同じ階層に、改修コードのファイルを配置する必要がある。  
特に読込が実装されているファイルでは、`from custom_plugin_ctgan import CustomCTGANPlugin` で `CustomCTGANPlugin` を import する必要がある(相対importは使用できない)。  
改修コードのファイル名は次のとおり。
* `custom_gan.py`
    * `synthcity.plugins.core.models.gan.GAN` の改修版の `CustomGAN` が実装されている
* `custom_tabular_gan.py`
    * `synthcity.plugins.core.models.tabular_gan.TabularGAN` の改修版の `CustomTabularGAN` が実装されている
* `custom_plugin_ctgan.py`
    * `synthcity.plugins.generic.plugin_ctgan.CTGANPlugin` の改修版の `CustomCTGANPlugin` が実装されている

### 保存設定について
モデル保存時にインスタンスの次の変数が None にされている
* `self.dataloader_sampler`
* `self.model.model._original_cond`
* `self._schema` と `self._training_schema`  (s とする) 内の以下
    * s.data
    * `s.domain` の各 value d について
        * `d.data`
        * `d.marginal_distribution`
* `self.model.dataloader_sampler` (s とする) 内の以下
    * `s._dataset_conditional`
    * `s._train_idx`
    * `s._train_mapping`
    * `s._test_idx`
    * `s._categorical_value_to_row_`
### バージョンについて
互換性維持のため、保存実行環境と読込実行環境上で `CustomCTGANPlugin` のベースとなる synthcity のバージョンを合わせることを推奨する。

現在の保存実行環境（Gramine Server）で利用しているバージョンは以下  
* Python:3.10  
* synthcity:0.2.10

# 入出力例
準備中