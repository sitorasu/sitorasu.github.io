# 初期設定

```
git clone git@github.com:sitorasu/sitorasu.github.io.git
git config --local core.hooksPath .githooks
```

Git Hooksの設定はpre-commitフックでフロントマターの`date`/`lastmod`フィールドを自動更新するために必要。