# movie
威秀影城官網暨訂票系統

此影城網站結合訂票系統，提供迅速的網路會員註冊、登入、資料查詢，以及忘記密碼功能。
影迷可輕鬆查閱影城介紹和電影資訊，並透過會員訂票系統預約座位。
最後，訂單紀錄系統可以方便會員查詢及修改訂票歷史。

說明
---
本資料加包含七個模組
- PyPtt_generate_stock_posts_dataset.py
  - 透過PyPtt，取得ptt Stock版的盤中閒聊post內容，產生資料集
- generate_stock_sentiment_dataset.py
  - 讀取post內容資料集，透過OpenAI API使用GPT模型分析post中的pushes(推文)的情緒與標的，並生成包含分析結果的資料集
- generate_content_stock_sentiment_dataset.py
  - 讀取post內容資料集，透過OpenAI API使用GPT模型分析post中的posts(發文)的情緒與標的，並生成包含分析結果的資料集
- get_the_direction.py
  - 讀取經人工審核過的盤中推文，將推文和鎖定的66張特定股票之漲跌以及大盤漲跌進行比較，找出有用的資料進行模型訓練
- read_dataset.py
  - csv資料集儲存時在Pushes欄位有經過格式的轉換，透過read_dataset.py中的read_dataset function可以讀取資料集，並將格式轉換回來
- get_market_data.py
  - 在找出有用資料時，可以透過push的時間自動抓取相同日期的大盤資料，並計算出30分鐘後的漲跌，協助找出有用資料 
- get_individual_stocks.py
  - 抓取各股票的金額，並計算出5min、15min、30min後的漲跌，協助找出有用的資料
- Nickname.csv
  - 將選擇的66張股票，整理出個別的暱稱，可用來將資料集中的標的，連接到其對應的股票漲跌
    
安裝
---
- step01   
```
git clone https://github.com/lzrong0203/PTT_Stock_sentiment.git
cd PTT_Stock_sentiment/sentiment_analysis
pip install -r requirements.txt
git clone https://github.com/lzrong0203/PyPtt.git -b stock market time
ren PyPtt NewPyPtt
```
- step02  
建立.env  
編輯.env內容為  
```
OPENAI_API_KEY = sk-...  
OPENAI_ORGANIZATION = org-...   
PTT_ID = ...  
PTT_PW = ...  
```
PyPtt_generate_stock_posts_dataset.py
---
### 模組使用方式
``` python
import PyPtt_generate_stock_posts_dataset
from PyPtt_generate_stock_posts_dataset import PyPttObj

# 將id與pw存在.env中，透過此指令將環境變數引入
load_dotenv()
# 建立物件
pyptt_obj = PyPttObj()
# 登入
pyptt_obj.login(os.getenv('PTT_ID'), os.getenv('PTT_PW'))
# 建立資料集
pyptt_obj.generate_newest_posts_dataset(
    post_num=2, save_path='ptt_stock_posts.csv')
# 登出
pyptt_obj.logout()
```

### 直接執行步驟  
- step01  
確認模組if __name__ == '__main__':中的程式碼，參數等相關設定正確  
- step02
```
cd PTT_Stock_sentiment/sentiment_analysis
python PyPtt_generate_stock_posts_dataset.py
```
### 結果資料
- 資料格式  
![image](https://github.com/lzrong0203/PTT_Stock_sentiment/assets/71923853/203cf952-fd14-41fe-aeb9-2f7fba830f9a)  
- Pushes欄位中的資料  
![image](https://github.com/lzrong0203/PTT_Stock_sentiment/assets/71923853/47085605-f520-47ab-b179-9e4ad28fae3f)  
- 資料集可見 sentiment_analysis/dataset/ptt_stock_posts.csv  

generate_stock_sentiment_dataset.py
---
### 模組使用方式
``` python
import generate_stock_sentiment_dataset
from generate_stock_sentiment_dataset import GPTStockChatAnalyzer
analyzer = GPTStockChatAnalyzer('ptt_stock_posts.csv')
analyzer.generate_analysis_result(
    save_path='ptt_stock_analysis_result.csv')
print('tokens:', analyzer.token_sum)
```
### 結果資料
- 資料格式  
![image](https://github.com/lzrong0203/PTT_Stock_sentiment/assets/71923853/6f679e86-612f-4cdd-953c-c4f0f98762ce)  
- Pushes欄位中的資料  
![image](https://github.com/lzrong0203/PTT_Stock_sentiment/assets/71923853/2eac07bb-ce69-47c6-a940-31cf0c5e88f2)  
- 資料集可見 sentiment_analysis/dataset/new_ptt_stock_analysis_5posts.csv    

### 直接執行步驟  
- step01  
確認模組if __name__ == '__main__':中的程式碼，參數等相關設定正確  
- step02
```
cd PTT_Stock_sentiment/sentiment_analysis
python generate_stock_sentiment_dataset.py
```
generate_content_stock_sentiment_dataset.py
---
### 模組使用方式

``` python
# 讀取包含許多文章的 CSV 檔案
csv_file = '/Users/luyuxuan/Desktop/0307_0331.csv'
df = read_csv_data(csv_file)

# 進行文章的情緒分析
sentiment_results = analyze_articles(df)

# 將情緒分析結果加入 DataFrame
df['Sentiment_Result'] = sentiment_results

# 儲存包含情緒分析結果的 DataFrame 到新的 CSV 檔案
df.to_csv('//Users/luyuxuan/Desktop/0307_0331_要分析文章的_結果.csv', index=False, encoding='utf_8_sig')
    
print('done')


```
### 函式說明
``` python
def analyze_articles(df):
    # 建立 GPTStockChatAnalyzer 物件
    analyzer = GPTStockChatAnalyzer()
    sentiment_results = []

    for index, row in df.iterrows():
        # 取得每篇文章的內容
        article_content = row['Content']
        
        # 進行情緒分析
        sentiment_analysis_result = analyzer.analyze_sentiment(article_content)
        
        if sentiment_analysis_result is not None:
            sentiment_results.append(sentiment_analysis_result)
        else:
            sentiment_results.append("情緒分析失敗，請檢查程式設定及環境。")
        
        # 限制每分析一篇文章後等待 1 秒，以避免 OpenAI API 頻率限制
        time.sleep(1)
    
    return sentiment_results



```

### 結果資料
- Content欄位中的資料  
![image](https://github.com/luyuxuan0414/deep-leaning-with-jupyternotebook/blob/main/%E6%88%AA%E5%9C%96%202023-08-17%20%E4%B8%8B%E5%8D%8810.54.06.png)
- 資料集可見 sentiment_analysis/Non_Trading_Chat_dataset/April_5posts.csv

get_the_direction.py
---
### 模組使用方式
``` python
merge = MergeStockData('ptt_stock_analysis_result721_checked.csv')
merge.merge_data('ptt_stock_analysis_result721_Final.csv')
```

### 直接執行步驟
- 將人工審核過的檔案(需只剩push內資料)名稱，寫入MergeStockData('filename.csv')中，並將存檔名稱寫入merge.merge_data('savename.csv')，直接執行即可。
  - 如出現錯誤，請注意檔案位置以及名稱是否錯誤
  - 若是讀檔失敗，可以檢查是否使用utf-8進行存檔
### 輸入資料
- 只需保留push(這是因為在人工審核時，用這種存法比較有效率)
![image](https://github.com/Dadanielwu/image/blob/main/input.gif)
- 資料集可見 sentiment_analysis/pyptt_dataset/ptt_stock_analysis_result714_checked.csv

### 結果資料
- 只保留正相關的部分(因為jupter無法完整顯示，所以用excel)
![image](https://github.com/Dadanielwu/image/blob/main/get_the_direction.gif)
- 資料集可見 sentiment_analysis/pyptt_dataset/ptt_stock_analysis_result721_Final.csv 

get_individual_stocks.py
---
### 模組使用方式
``` python
stock='2316'
#以每7天為一單位，填寫想抓取資料的時間，interval可以調整爬取的時間間格
df = yf.download(f'{stock}.TW', start="2023-07-14", end="2023-07-20", interval="1m")
``` 
- step1:更改stock='股票編號'
- step2:更改start="起始日期", end="結束日期", interval="間隔"

### 結果資料
- 各股票資料顯示
![image](https://github.com/Dadanielwu/image/blob/main/the_individual_stocks.gif)
- 資料集可見 sentiment_analysis/pyptt_dataset/individual_stock_dataset/878_2023_7_11_31.csv
  
read_dataset.py
---
### 模組使用方式
``` python
from read_dataset import read_dataset
df = read_dataset("test.csv")
```

get_market_data.py
---
### 模組使用方式
``` python
from get_market_data import get_market_data
get_market_data(year,month,day)
```

### 結果資料
- 大盤資料顯示(因為會依照push時間自動爬取，所以沒另外上傳資料)  
![image](https://github.com/Dadanielwu/image/blob/main/merkert_stock.gif)

Nickname.csv
---
### 檔案使用方式
- 用於協助將同一支股票的不同暱稱，都對應到相同漲跌資料
  
### 結果資料
- 各股票暱稱資料顯示
![image](https://github.com/Dadanielwu/image/blob/main/Nickname.gif)
- 資料集可見 sentiment_analysis/Nickname.csv
