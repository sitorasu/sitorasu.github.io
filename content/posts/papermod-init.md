---
lastmod: 2025-06-08T22:07:57+09:00
date: '2025-06-08T05:45:50+09:00'
draft: false
title: 'PaperModの初期設定'
tags:
    - Hugo
    - Hugo-PaperMod
---

## PaperModのインストール

以下を参考にPaperModをインストールする。

- [Installation · adityatelange/hugo-PaperMod Wiki](https://github.com/adityatelange/hugo-PaperMod/wiki/Installation)
- [Use Hugo Modules](https://gohugo.io/hugo-modules/use-modules/)

Hugoのテーマのインストール方法にはいくつかあるが、今回はHugo Moduleを使う方法を採用する。`git submodule`を使う方法と比較して、リポジトリのクローン時に明示的な初期化が不要であり、アップデートのコマンドが単純であるという利点がある。ただしGoのインストールが必要。

空のサイトを作り、PaperModをインストールしてローカルで立ち上げるコマンドは以下の通り。

```
hugo new site sitorasu.github.io --format yaml
cd mysite
hugo mod init github.com/sitorasu/sitorasu.github.io
cat << EOS >> hugo.yaml
module:
  imports:
  - path: github.com/adityatelange/hugo-PaperMod
EOS
hugo server
```

`hugo server`で立ち上げたサイトを確認すると、PaperModのテーマが表示されているはず。

PaperMod Wikiの説明には`hugo.yaml`に`theme: ["PaperMod"]`を追加するよう指示があるが、Hugo Moduleを使う場合には**追加してはいけない**。追加すると`hugo server`実行時に*failed to load modules: module "PaperMod" not found*というエラーが出る。

テーマをアップデートするには以下のコマンドを実行する。

```
hugo mod get -u
```

Hugo Moduleの依存関係はプロジェクトのルートの`go.mod`というファイルに記録されており、上記コマンドで更新される。`go.mod`は`hugo mod init`実行時に作成される。

## 設定ファイルの記述

設定ファイルはプロジェクトのルートの`hugo.yaml`。[exampleSiteのconfig.yml](https://github.com/adityatelange/hugo-PaperMod/blob/exampleSite/config.yml)に主要な設定が載っている。意味が分からないものについては[PaperMod Wiki](https://github.com/adityatelange/hugo-PaperMod/wiki)または[Hugo Docs](https://gohugo.io/configuration/)を参照する。だいたいデフォルトで適切な設定になっているはずなので、デフォルトで気に入らない部分だけ明示的に設定する。

## アイコンの追加

ソーシャルアイコンに[VRChatっぽいアイコン](https://tabler.io/icons/icon/badge-vr)を追加する。[svg.html](https://github.com/adityatelange/hugo-PaperMod/blob/master/layouts/partials/svg.html)を`layouts/partials/`にコピーし、独自のSVGを追加すればよい。例えば[このコミット](https://github.com/adityatelange/hugo-PaperMod/commit/d3bc6af9b66cd160aff5b7ecc7ab19c9b8a34c03)が参考になる。


## CSSの上書き

[FAQs · adityatelange/hugo-PaperMod Wiki](https://github.com/adityatelange/hugo-PaperMod/wiki/FAQs#bundling-custom-css-with-themes-assets)によれば、`assets/css/extended`に配置したcssはすべて読み込まれるらしい。実際にやってみたらちゃんと読み込まれた。

コードブロックのフォントがmonospaceに設定されていたので調整した。

## リンクを新しいタブで開くようにする

[このコメント](https://github.com/adityatelange/hugo-PaperMod/discussions/760#discussioncomment-2021778)を参考に設定。`themes`の下にファイルを作るのではなくプロジェクトのルート直下の`layouts`の下に作るようにした。無事成功。

## 最終更新日をヘッダに表示する

[このプルリクエスト](https://github.com/adityatelange/hugo-PaperMod/pull/1337/commits/a5f4e804ffca2e692344571eb1098406d423cc86)の通りに設定する。作成日と同日中の更新は表示しない仕様のつもりなんだろうけど実装にミスがある。DateFormatの指定は`2006-01-02`の日付でないと機能しない。

ついでに日付の前に作成日・最終更新日の文字が表示されるようにした。

## 投稿日と最終更新日をコミット時に自動設定する

Git Hooksののpre-commitの仕組みで実現する。仕様は以下のようにする。

- ステージングされた`.md`ファイルのうち、`content/posts`ディレクトリの下にあるものを処理の対象とする
- 変更の種別がファイルの新規追加である`.md`ファイルについて
    - フロントマターに`date:`で始まる行がなければ`date: <現在の日時>`を追加する
    - フロントマターに`date:`で始まる行があれば何もしない
- 変更の種別が既存ファイルの変更である`.md`ファイルについて
    - フロントマターに`lastmod:`で始まる行があればその行を削除する
    - フロントマターに`lastmod: <現在の日時>`を追加する

なお、pre-commitのスクリプトは

- `.git/hooks/pre-commit`に記述するか、
- スクリプトを記述した`pre-commit`ファイルを任意の場所に配置し、`git config --local core.hooksPath <pre-commitの親ディレクトリのパス>`を実行する

ことでしか機能しない。いずれにしてもクローンしてすぐに機能させることはできないので初期設定のスクリプトが必要になる。

## Gistのサポート

そのままでは以下の警告が出るので言われたとおりに対策する。

> WARN  The "gist" shortcode was deprecated in v0.143.0 and will be removed in a future release. See https://gohugo.io/shortcodes/gist for instructions to create a replacement.

このコードを丸ごとコピペしてくださいというコードの中に警告のロジックが入っているのでそれは取り除かないと警告が消えないことに注意。

## GitHub Actionsの登録

[Host on GitHub Pages](https://gohugo.io/host-and-deploy/host-on-github-pages/)をそのまんまやる

## TODO: 目次をリッチにする

サイドバーで追従するやつにしたい。

