# 自動でarxivをcronして論文の要約を作るよ
CPUとそこそこのメモリ（８はほしいかも）
## 使い方
* ollamaは自分で入れてね(ollama dockerするの面倒だったので)
### ollamaの入れ方
* Ubuntuならこれで入るよ(WSLでもね)
```
curl -fsSL https://ollama.com/install.sh | sh
```
*  ollama pull phi4でモデルをロードして、もし他のが良ければ（軽いやつとか使いたければ）自分でpullしてarxiv_cron.pyのモデルを修正すればいいと思う
### uv（仮想環境ツール）
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
これでinstallできる（interativeでsourceしてみたいなのが表示されるからやればよい）

### 実行コマンド
cloneしたディレクトリに入って、source .venv/bin/activateをして起動
src以下でpython arxiv_papers_cron.py（tmuxで仮想コンソールでやっておくとssh接続きれても続くからよさげ）
これで5分おきに一つの論文がDLされて要約結果がdbに出力される。
確認には

python get_db.pyすれば見れる
いまは表示結果をtxtにしてメモに貼ってるけど今後は自動でDiscordの通知に投げたい