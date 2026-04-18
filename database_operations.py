import sqlite3
import csv

def setup_database():
    # 建立 SQLite3 資料庫，取名為 "data.db"
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # 創建資料庫 Table，取名為 "TemperatureForecasts"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TemperatureForecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            regionName TEXT NOT NULL,
            dataDate TEXT NOT NULL,
            mint INTEGER NOT NULL,
            maxt INTEGER NOT NULL
        )
    ''')
    
    # 為了避免重複執行程式時出現重複資料，先清空資料表
    cursor.execute('DELETE FROM TemperatureForecasts')

    # 從剛剛產生的 weather_data.csv 讀取資料
    try:
        with open('weather_data.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                regionName = row['Location']
                dataDate = row['Date']
                mint = int(row['Min Temperature (C)']) if row['Min Temperature (C)'] else 0
                maxt = int(row['Max Temperature (C)']) if row['Max Temperature (C)'] else 0
                
                # 將氣溫資料存到資料庫
                cursor.execute('''
                    INSERT INTO TemperatureForecasts (regionName, dataDate, mint, maxt)
                    VALUES (?, ?, ?, ?)
                ''', (regionName, dataDate, mint, maxt))
        
        # 提交變更
        conn.commit()
        print("Data successfully saved to data.db -> TemperatureForecasts table.\n")
    except FileNotFoundError:
        print("Error: weather_data.csv not found. Please ensure it is generated first.")
        return None

    return conn

def check_database(conn):
    if not conn:
        return
        
    cursor = conn.cursor()
    
    # 1. 列出所有地區名稱
    print("=== 檢查 1: 列出所有地區名稱 ===")
    cursor.execute('SELECT DISTINCT regionName FROM TemperatureForecasts')
    regions = cursor.fetchall()
    for row in regions:
        print(f"- {row[0]}")
        
    # 2. 列出中部地區的氣溫資料
    print("\n=== 檢查 2: 列出中部地區的氣溫資料 ===")
    cursor.execute('SELECT regionName, dataDate, mint, maxt FROM TemperatureForecasts WHERE regionName = "中部地區"')
    central_data = cursor.fetchall()
    
    # 標頭對齊
    print(f"{'地區':<8} | {'時間 (dataDate)':<12} | {'最低氣溫':<6} | {'最高氣溫':<6}")
    print("-" * 55)
    for row in central_data:
        # 使用格式化字串補齊顯示長度
        print(f"{row[0]:<10} | {row[1]:<16} | {row[2]:<10} | {row[3]:<10}")

    conn.close()

if __name__ == '__main__':
    db_conn = setup_database()
    check_database(db_conn)
