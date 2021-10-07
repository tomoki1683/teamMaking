# teamMaking

## レポジトリの概要

大きく分けて２つのプログラムが入っている。

1. jupyterNotebook（実際に使用したNotebookを記載）
2. python（Notebookだと分かりにくいため、後日まとめたコードを記載）

## 使い方

jupyterNotebook側は、Notebook上に説明を記載しているため割愛する。<br>
python側の実行方法は以下の通り。

```sh
cd teamMaking/python # ダウンロードしたディレクトリを指定する
python main.py
```

ただし、実行する前にmain.pyの設定を変更する必要がある。

```python
main_path = "../../testData.csv"
remove_path = "../../fix_zoom幹事リスト.csv"
zoom_num = 2

team_num = 25
teamMember_num = 0
```
等。研究ではjupyterNotebookを用いることが多いので、分かりにくかったらすみません、、

## 参考にしたHP

[【競プロ×実務】pythonで簡単チーム分け【焼きなまし法】](https://recruit.gmo.jp/engineer/jisedai/blog/grouping_by_annealing/)