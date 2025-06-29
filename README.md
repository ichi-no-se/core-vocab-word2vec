# core-vocab-word2vec
Wiktionary から日本語の基礎語彙リストを取得し，word2vec モデルに含まれる語彙とその特徴ベクトルを抽出します．

## 構成
```
core-vocab-word2vec/
├── data/
│ ├── vocab.txt # 抽出語彙リスト（1語1行）
│ └── vec.json # 対応ベクトルを保存したJSON
├── extract-vocab.py # Wiktionary などから語彙リストを生成するスクリプト
├── extract-vec.py # Word2Vec モデルからベクトルを抽出するスクリプト
├── requirements.txt # 依存パッケージ
└── README.md # このファイル
```

## 使い方

### 1. 必要なライブラリのインストール
以下のコマンドで依存ライブラリをインストールします．
```bash
pip install -r requirements.txt
```

### 2. 語彙リストの作成
以下のコマンドで Wiktionary の[日本語の基本語彙1000](https://ja.wiktionary.org/wiki/Wiktionary:%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%81%AE%E5%9F%BA%E6%9C%AC%E8%AA%9E%E5%BD%991000)から日本語の基礎語彙リストを取得します．
他のページには対応していません．また，ページ内の構造が変わった場合動作しない可能性があります．

```bash
python extract-vocab.py
```
デフォルトでは，以下の設定で実行されます：
- 対象の品詞：名詞・動詞・形容詞・形容動詞
- 関連語も含める
- 出力先：`data/vocab.txt`
変更するには例えば次のようにします：
```bash
python extract-vocab.py \
  --speech 名詞 動詞 \
  --no-related \
  --output my-vocab.txt
```

### 3. 特徴ベクトルの抽出
以下のコマンドで，指定した Word2Vec モデルから語彙とベクトルを抽出し，`data/vec.json` に保存します：
```bash
python extract-vec.py \
  --model path/to/model.kv
```
`--vocab` と `--output` は省略可能で，デフォルトでは以下のように処理されます：
- `--vocab`：`data/vocab.txt`
- `--output`：`data/vec.json`
必要に応じて，以下のように変更できます：
```bash
python extract-vec.py \
  --model path/to/model.kv \
  --vocab custom_vocab.txt \
  --output result/selected_vectors.json
```

## ライセンス
- `extract-vocab.py` および `extract-vec.py` を含むコードは，[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) のもとで公開されています．自由に利用・改変・再配布いただけます．
- `data/vocab.txt` は，[Wiktionary:日本語の基本語彙1000](https://ja.wiktionary.org/wiki/Wiktionary:%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%81%AE%E5%9F%BA%E6%9C%AC%E8%AA%9E%E5%BD%991000) の内容をもとに生成したものであり，Wiktionary のライセンス（[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)）に準拠する必要があります．
- `data/vec.json` は，以下の複数のライセンスの影響を受けます：
  - 語彙リストに基づくため，[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) に準拠する必要があります（出典：Wiktionary）．
  - ベクトル抽出に使用した Word2Vec モデルには，[chiVe: Sudachi による日本語単語ベクトル](https://github.com/WorksApplications/chiVe)の `v1.3 mc90` を使用しています．これは [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) の下で，[株式会社ワークスアプリケーションズ](https://www.worksap.co.jp/)によって提供されています．
