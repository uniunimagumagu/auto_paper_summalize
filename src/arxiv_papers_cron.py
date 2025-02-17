import arxiv
import time
import fitz  # PyMuPDF
import sqlite3
import requests
import json
from datetime import datetime
import random
import logging
from pathlib import Path

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('arxiv_collector.log'),
        logging.StreamHandler()
    ]
)

class ArxivCollector:
    def __init__(self, db_path="arxiv_summaries.db", ollama_url="http://localhost:11434/api/generate", model_name="phi4"):
        self.db_path = db_path
        self.ollama_url = ollama_url
        self.model_name = model_name
        self.setup_database()
        
        # 検索クエリの設定
        self.search_queries = [
            'ti:"large language model"',  # タイトルにLLMを含む
            'ti:"artificial intelligence"',  # タイトルにAIを含む
            'cat:cs.AI',  # AI分野
            'cat:cs.CL',  # 計算言語学
            'cat:cs.LG'   # 機械学習
        ]

    def setup_database(self):
        """データベースの初期設定"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            arxiv_id TEXT PRIMARY KEY,
            title TEXT,
            field TEXT,
            problem TEXT,
            method TEXT,
            result TEXT,
            summary TEXT,
            processed_date TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    def get_processed_papers(self):
        """既に処理済みの論文IDを取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT arxiv_id FROM summaries")
        processed = set(row[0] for row in cursor.fetchall())
        conn.close()
        return processed

    def get_random_paper(self):
        """ランダムな検索クエリを使用して新しい論文を取得"""
        processed_papers = self.get_processed_papers()
        query = random.choice(self.search_queries)
        
        search = arxiv.Search(
            query=query,
            max_results=50,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        for paper in search.results():
            arxiv_id = paper.get_short_id()
            if arxiv_id not in processed_papers:
                return paper
        
        return None

    def download_pdf(self, paper):
        """論文PDFをダウンロード"""
        pdf_url = paper.pdf_url
        pdf_path = f"papers/{paper.get_short_id()}.pdf"
        Path("papers").mkdir(exist_ok=True)
        
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            return pdf_path
        return None

    def extract_text_from_pdf(self, pdf_path):
        """PDFからテキストを抽出"""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text

    def get_summary_from_llm(self, paper, text):
        """LLMを使用して論文を要約"""
        prompt = f"""
以下の論文を要点を明確にしながら要約してください。
人に伝えることを意識してわかりやすくかつ論文の主旨をしっかり押さえて答えてください。  

### **論文の概要**
- **タイトル**: {paper.title}
- **分野**: （この研究が属する学術的な分野を明示）

### **研究の背景**
- **何が問題か**: （この研究が解決しようとしている具体的な課題）  
- **なぜ解決が必要か**: （この問題の重要性）  

### **提案手法**
- **基本アイデア**: （従来手法と何が違うのか）  
- **技術的なポイント**: （手法の要点を3～4つ）  

### **実験と結果**
- **主な結果**: （提案手法の優位性）  

### **結論と今後の課題**

論文本文:
{text[:5000]}
"""
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=data)
            return response.json().get("response", "要約に失敗しました")
        except Exception as e:
            logging.error(f"LLM API error: {e}")
            return None

    def save_to_db(self, paper, summary):
        """要約をデータベースに保存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT INTO summaries 
            (arxiv_id, title, field, problem, method, result, summary, processed_date) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                paper.get_short_id(),
                paper.title,
                "AI/ML",  # 基本的な分野分類
                "Not extracted",  # 詳細な問題定義
                "Not extracted",  # 手法の説明
                "Not extracted",  # 結果の要約
                summary,
                datetime.now().isoformat()
            ))
            conn.commit()
            logging.info(f"Saved summary for paper {paper.get_short_id()}")
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            conn.close()

    def process_single_paper(self):
        """1つの論文を処理"""
        try:
            paper = self.get_random_paper()
            if not paper:
                logging.info("No new papers found")
                return False

            logging.info(f"Processing paper: {paper.get_short_id()}")
            
            pdf_path = self.download_pdf(paper)
            if not pdf_path:
                logging.error("Failed to download PDF")
                return False

            text = self.extract_text_from_pdf(pdf_path)
            summary = self.get_summary_from_llm(paper, text)
            
            if summary:
                self.save_to_db(paper, summary)
                #Path(pdf_path).unlink()  # PDFを削除
                return True
            
        except Exception as e:
            logging.error(f"Error processing paper: {e}")
        
        return False

def main():
    collector = ArxivCollector()
    
    while True:
        try:
            logging.info("Starting new paper processing cycle")
            collector.process_single_paper()
            
            # 5分待機
            logging.info("Waiting 5 minutes before next paper...")
            time.sleep(300)
            
        except KeyboardInterrupt:
            logging.info("Stopping the collector...")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(10)  # エラー時も5分待機

if __name__ == "__main__":
    main()