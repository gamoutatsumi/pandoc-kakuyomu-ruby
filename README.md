# pandoc-kakuyomu-ruby

カクヨム風のルビと圏点（傍点）を使えるようにするPandocフィルタ。

## インストール

```sh
pip install regex pandocfilters
git clone https://github.com/Gamou-T/pandoc-kakuyomu-ruby.git
```

```sh
pandoc --filter=/path/to/ruby_kenten.py foo.md
```

## フォーマット

ルビ対象の文字列（親文字）の前に全角縦棒`｜`を置き、直後に二重山括弧`《` `》`で括ったルビを書きます。ルビ対象が漢字のみで構成される場合は縦棒を省略できます。

また、ルビ記法はエスケープが可能です。

また、LaTeX使用時のみ`pxrubrica`の機能の一部が使用可能です。(`pxrubrica`使用時のみ。というかこのフィルタ自体`pxrubrica`で動かす事を想定しています。一応他のパッケージでも動きますが保証はしません。)

HTML系に変換した場合は全て単一のグループルビになります。

本来`pxrubrica`の熟語・モノルビの区切り文字では半角縦棒`|`を使用しますが、ここでは全て全角縦棒`｜`に統一しています。というか半角だと動きません。

なお、ルビに対応しているのはunicode上での和文(`\p{Hiragana}` `\p{Katakana}` `\p{Han}`)+長音記号`ー`+約物(`\p{P}`に限られます。

e.g. :

```markdown
---
header-includes: # pxrubricaの読み込み、自動切替熟語ルビ(進入大)に設定
  - \usepackage{pxrubrica}
  - \rubysetup{<J>}
---

## 熟語ルビ

｜単語《たん｜ご》

ひらがな単語《たん｜ご》

東京特許｜許可局《きょ｜か｜きょく》

鶏《にわとり》

## グループルビ

あれは雲雀《ひばり》です。

## 圏点（傍点）

《《アレ》》

## ルビが付かない

ひらがな《よみがな》

単語｜《よみがな》

｜Linux《リナックス》
```

個々のルビへのモード指定には対応しておりません。

## 使用可能フォーマット

htmlベース(`html` `html5` `epub` `epub3`)、LaTeX(`latex`)に対応します。

その他細かい説明は[qiita](https://qiita.com/Gamou-T/items/efca3fe46ade9779f64b)を参照してください。
