---
date: '2025-06-08T05:45:50+09:00'
draft: false
title: 'PaperModの初期設定'
tags:
    - Hugo
    - Hugo/PaperMod
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

設定ファイルはプロジェクトのルートの`hugo.yaml`。[exampleSiteのconfig.yml](https://github.com/adityatelange/hugo-PaperMod/blob/exampleSite/config.yml)におそらく全部の設定が載っている。意味が分からないものについては[PaperMod Wiki](https://github.com/adityatelange/hugo-PaperMod/wiki)または[Hugo Docs](https://gohugo.io/configuration/)を参照する。だいたいデフォルトで適切な設定になっているはずなので、デフォルトで気に入らない部分だけ明示的に設定する。

## アイコンの追加

ソーシャルアイコンに[VRChatっぽいアイコン](https://tabler.io/icons/icon/badge-vr)を追加する。[svg.html](https://github.com/adityatelange/hugo-PaperMod/blob/master/layouts/partials/svg.html)を`layouts/partials/`にコピーし、独自のSVGを追加すればよい。追加方法については例えば[このコミット](https://github.com/adityatelange/hugo-PaperMod/commit/d3bc6af9b66cd160aff5b7ecc7ab19c9b8a34c03)が参考になる。