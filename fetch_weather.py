import requests
import json
import csv

def fetch_weather_data():
    url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=CWA-2EA81324-31F0-4AA3-91F3-8F46E8ADE174&downloadType=WEB&format=JSON"
    
    print("Fetching weather data from CWA API...")
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("Data fetched successfully!")
        
        # 提取指定的地區: 台灣北部、中部、南部、東北部、東部及東南部地區
        target_locations = ["北部地區", "中部地區", "南部地區", "東北部地區", "東部地區", "東南部地區"]
        
        try:
            locations_data = data["cwaopendata"]["resources"]["resource"]["data"]["agrWeatherForecasts"]["weatherForecasts"]["location"]
            
            extracted_data = []
            for loc in locations_data:
                if loc["locationName"] in target_locations:
                    extracted_data.append(loc)
                    
            # 使用 json.dumps 觀察獲得的資料
            formatted_data = json.dumps(extracted_data, indent=4, ensure_ascii=False)
            
            # 印出觀察資料
            print(f"Extracted Data:\n{formatted_data[:1000]}...\n[Truncated for brevity]")
            
            # 將完整提取的資料存成 JSON 檔案以便詳細觀察
            with open("weather_target_regions.json", "w", encoding="utf-8") as f:
                f.write(formatted_data)
            print("\nSpecfic region data saved to weather_target_regions.json for observation.")
            
            # 轉換為 CSV 格式並儲存
            csv_filename = "weather_data.csv"
            with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csvfile:
                # 寫入 BOMI header encoding for excel compatibility => utf-8-sig does this automatically
                writer = csv.writer(csvfile)
                writer.writerow(["Location", "Date", "Weather", "Max Temperature (C)", "Min Temperature (C)"])
                
                for loc in extracted_data:
                    loc_name = loc["locationName"]
                    elements = loc["weatherElements"]
                    
                    # 取得每個天氣元素的 daily 陣列
                    wx_daily = elements.get("Wx", {}).get("daily", [])
                    maxt_daily = elements.get("MaxT", {}).get("daily", [])
                    mint_daily = elements.get("MinT", {}).get("daily", [])
                    
                    # 假設日期是順序且天數一致的
                    for i in range(len(wx_daily)):
                        date = wx_daily[i].get("dataDate", "")
                        weather = wx_daily[i].get("weather", "")
                        max_t = maxt_daily[i].get("temperature", "") if i < len(maxt_daily) else ""
                        min_t = mint_daily[i].get("temperature", "") if i < len(mint_daily) else ""
                        
                        writer.writerow([loc_name, date, weather, max_t, min_t])

            print(f"Data successfully exported to {csv_filename}")
            
        except KeyError as e:
            print(f"Unexpected JSON structure. Missing key: {e}")
            
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_weather_data()
