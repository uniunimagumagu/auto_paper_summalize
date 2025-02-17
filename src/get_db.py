import sqlite3

def check_db_content(db_path="arxiv_summaries.db"):
    """
    arXiv論文要約データベースの内容を確認し表示する関数
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # テーブル構造の確認
    print("\n=== データベース内のテーブル構造 ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        print(f"\nテーブル名: {table[0]}")
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        print("カラム構成:")
        for col in columns:
            pk = "PRIMARY KEY" if col[5] == 1 else ""
            print(f"- {col[1]} ({col[2]}) {pk}")
    
    # データの確認
    print("\n=== 保存されているデータ ===")
    cursor.execute("SELECT arxiv_id, title, field FROM summaries")
    summaries = cursor.fetchall()
    
    if summaries:
        print(f"\n全{len(summaries)}件のデータが保存されています。\n")
        print("【概要一覧】")
        for summary in summaries:
            print("-" * 50)
            print(f"arXiv ID: {summary[0]}")
            print(f"タイトル: {summary[1]}")
            print(f"分野: {summary[2]}\n")
        
        # 詳細データの表示
        print("\n【詳細データ】")
        cursor.execute("SELECT * FROM summaries")
        all_data = cursor.fetchall()
        for data in all_data:
            print("=" * 60)
            print(f"arXiv ID: {data[0]}")
            print(f"タイトル: {data[1]}")
            print(f"分野: {data[2]}")
            print(f"課題: {data[3]}")
            print(f"手法: {data[4]}")
            print(f"結果: {data[5]}")
            print("\n要約:")
            print(data[6])
            print("=" * 60 + "\n")
    else:
        print("データベースにデータが保存されていません。")
    
    conn.close()

if __name__ == "__main__":
    check_db_content()