闇レン APIキー確認用アプリケーション
---

# 概要

これは闇レンで使用するAPI疎通確認用のアプリケーションです。

`OPENAI_API_KEY`が発行されていないと何もできません。

# 詳細

環境変数 `OPENAI_API_KEY` にAPI keyが設定されていること。

Windows
環境変数の登録 で追加

その他
`.bashrc_profile`や`.bashrc`、`.zprofile`等（環境により異なる）で

```
export OPENAI_API_KEY=*****************************...
```

その他、省略（インストールを参照のこと）



# インストール

多少の誤りはご容赦を

Clone
```shell
git clone https://github.com/IPLMasayukiFujikawa/study-yami-chapter02.git
```

Pythonの設定

仮想環境の作成

```shell
cd <pathto>/study-yami-chapter02
python -m venv .venv
# Windows
.¥.venv¥Script¥Activate
# others
. ./.venv/bin/activate
```

仮想環境（コマンドプロンプトの先頭に'(.venv)'がつく）

```shell
pip install pip-tools
# パッケージのインストール
pip-compile requirements.in
# requirements.txtが作成されたことを確認して実行
pip install -r requirements.txt
```

パッケージインストールの確認

```shell
$ pip freeze
annotated-types==0.7.0
:
openai==1.40.6
:
typing_extensions==4.12.2
```

# 実行

```shell
python main.py
```

成功すると

```
東京の天気はどうですか？
```

に対し

```
申し訳ありませんが、リアルタイムの天気情報を提供することはできません。東京の現在の天気を知りたい場合は、天気予報のウェブサイトやアプリをご利用ください。
```

のような返事が返ってくる。
