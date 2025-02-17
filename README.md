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


### 動作例
```
 curl -LsSf https://astral.sh/uv/install.sh | sh
downloading uv 0.6.0 x86_64-unknown-linux-gnu
no checksums to verify
installing to /home/kobamasa/.local/bin
  uv
  uvx
everything's installed!

To add $HOME/.local/bin to your PATH, either restart your shell or run:

    source $HOME/.local/bin/env (sh, bash, zsh)
    source $HOME/.local/bin/env.fish (fish)
WARNING: The following commands are shadowed by other commands in your PATH: uv uvx
[master][~/mywork/auto_paper_summalize]$ source $HOME/.local/bin/env
[master][~/mywork/auto_paper_summalize]$ uv sync
Using CPython 3.13.2
Creating virtual environment at: .venv
Resolved 86 packages in 28ms
      Built sgmllib3k==1.0.0
      Built sentencepiece==0.2.0
Prepared 84 packages in 2m 36s
Installed 84 packages in 2.77s
 + ace-tools==0.0
 + acres==0.2.0
 + aiofiles==24.1.0
 + anyio==4.8.0
 + arxiv==2.1.3
 + certifi==2025.1.31
 + charset-normalizer==3.4.1
 + ci-info==0.3.0
 + click==8.1.8
 + configobj==5.0.9
 + configparser==7.1.0
 + etelemetry==0.3.1
 + feedparser==6.0.11
 + filelock==3.17.0
 + fitz==0.0.1.dev2
 + frontend==0.0.3
 + fsspec==2025.2.0
 + greenlet==3.1.1
 + h11==0.14.0
 + httplib2==0.22.0
 + huggingface-hub==0.28.1
 + idna==3.10
 + isodate==0.6.1
 + itsdangerous==2.2.0
 + jinja2==3.1.5
 + looseversion==1.3.0
 + lxml==5.3.1
 + markupsafe==3.0.2
 + mpmath==1.3.0
 + networkx==3.4.2
 + nibabel==5.3.2
 + nipype==1.9.2
 + numpy==2.2.2
 + nvidia-cublas-cu12==12.4.5.8
 + nvidia-cuda-cupti-cu12==12.4.127
 + nvidia-cuda-nvrtc-cu12==12.4.127
 + nvidia-cuda-runtime-cu12==12.4.127
 + nvidia-cudnn-cu12==9.1.0.70
 + nvidia-cufft-cu12==11.2.1.3
 + nvidia-curand-cu12==10.3.5.147
 + nvidia-cusolver-cu12==11.6.1.9
 + nvidia-cusparse-cu12==12.3.1.170
 + nvidia-cusparselt-cu12==0.6.2
 + nvidia-nccl-cu12==2.21.5
 + nvidia-nvjitlink-cu12==12.4.127
 + nvidia-nvtx-cu12==12.4.127
 + packaging==24.2
 + pandas==2.2.3
 + pathlib==1.0.1
 + protobuf==5.29.3
 + prov==2.0.1
 + puremagic==1.28
 + pydot==3.0.4
 + pymupdf==1.25.3
 + pyparsing==3.2.1
 + python-dateutil==2.9.0.post0
 + pytz==2025.1
 + pyxnat==1.6.3
 + pyyaml==6.0.2
 + rdflib==6.3.2
 + regex==2024.11.6
 + requests==2.32.3
 + safetensors==0.5.2
 + scipy==1.15.1
 + sentencepiece==0.2.0
 + setuptools==75.8.0
 + sgmllib3k==1.0.0
 + simplejson==3.19.3
 + six==1.17.0
 + sniffio==1.3.1
 + sqlalchemy==2.0.38
 + starlette==0.45.3
 + sympy==1.13.1
 + tiktoken==0.8.0
 + tokenizers==0.21.0
 + torch==2.6.0
 + tqdm==4.67.1
 + traits==7.0.2
 + transformers==4.48.3
 + triton==3.2.0
 + typing-extensions==4.12.2
 + tzdata==2025.1
 + urllib3==2.3.0
 + uvicorn==0.34.0
[master][~/mywork/auto_paper_summalize]$ ls
README.md  pyproject.toml  src  uv.lock
[master][~/mywork/auto_paper_summalize]$ source .venv/bin/activate
(auto-paper-summalize) [master][~/mywork/auto_paper_summalize]$ python -V
Python 3.13.2
(auto-paper-summalize) [master][~/mywork/auto_paper_summalize]$ python src/arxiv_papers_cron.py
2025-02-17 12:48:26,051 - INFO - Starting new paper processing cycle
/home/kobamasa/mywork/auto_paper_summalize/src/arxiv_papers_cron.py:77: DeprecationWarning: The 'Search.results' method is deprecated, use 'Client.results' instead
  for paper in search.results():
2025-02-17 12:48:26,052 - INFO - Requesting page (first: True, try: 0): https://export.arxiv.org/api/query?search_query=ti%3A%22large+language+model%22&id_list=&sortBy=submittedDate&sortOrder=descending&start=0&max_results=100
2025-02-17 12:48:31,034 - INFO - Got first page: 100 of 10048 total results
2025-02-17 12:48:31,035 - INFO - Processing paper: 2502.09604v1
2025-02-17 12:48:32,051 - INFO - Saved summary for paper 2502.09604v1
2025-02-17 12:48:32,051 - INFO - Waiting 5 minutes before next paper...
```