# teamMaking

## 追記

2022年9月7日に、テストデータとそのチーム分け結果を追加しました。<br>
スパゲッティコードで非常に申し訳ないので、何かあれば気軽に聞いてください。<br>
余裕があれば、適宜コード修正するかもしれないです。（あまり期待はしないでください…）

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
main_path = "../../参加者リスト.csv" # 参加者リストのcsvファイルを指定する
remove_path = "../../幹事リスト.csv" # 削除する幹事リストを指定する
zoom_num = 2 # 当日の会場数を指定する
group_information = [
    # n回目のグループ作成で使いたい情報を、[n-1]配列に指定する
    # [team_num : 『チーム数を指定、メンバー数指定なら0にする』, teamMember_num : 『メンバー数を指定、チーム数指定なら0にする』, make_method : 『順番に割り振るシステムなら"seq",最適化を用いるなら"opt"を指定する』]
    [25, 0, "seq"],
    [0, 5, "seq"],
    [0, 5, "opt"]
]
alphabet = [1,2] # n回目のグループ番号をアルファベットにしたい場合、nをリストに追加する
```
研究ではjupyterNotebookを用いることが多いので、分かりにくかったらすみません、、

## 参考にしたHP

[【競プロ×実務】pythonで簡単チーム分け【焼きなまし法】](https://recruit.gmo.jp/engineer/jisedai/blog/grouping_by_annealing/)
