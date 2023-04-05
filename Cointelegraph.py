import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
import os.path

urls = ['https://cointelegraph.com/tags/bitcoin',
        'https://cointelegraph.com/tags/blockchain',
        'https://cointelegraph.com/tags/nft',
        'https://cointelegraph.com/tags/ethereum',
        'https://cointelegraph.com/tags/business',
        'https://cointelegraph.com/tags/defi',
        'https://cointelegraph.com/tags/altcoin',
        'https://cointelegraph.com/tags/regulation',
        'https://cointelegraph.com/tags/adoption',]

#step 1. Create Excel writer
if not os.path.exists('Cointelegraph.xlsx'):
    xlwriter = pd.ExcelWriter('Cointelegraph.xlsx', engine='openpyxl')
    xlwriter.book.save('Cointelegraph.xlsx')
else:
    xlwriter = pd.ExcelWriter('Cointelegraph.xlsx', engine='openpyxl',mode='a',if_sheet_exists='overlay')

#step 2. Open HTML
for url in urls:
    file_base_name = url.split('/')[-1]
    try:
        existing_data = pd.read_excel('Cointelegraph.xlsx', engine='openpyxl', sheet_name=file_base_name)
    except:
        existing_data = None
    workbook = xlwriter.book
    print(f'Scraping {url}')
    req = Request(url)
    resp = urlopen(req)
    
    #step 3. Define headers    
    Headers = ['Source','Header','Content','Date','Views']
   
    news_tables = []
    html = BeautifulSoup(resp,features="lxml")
    news_rows = html.find_all('article')
    #step 4. Retrieve news header
    for news_table in news_rows:
        news_source = "http://cointelegraph.com"+news_table.find('a',class_='post-card-inline__title-link').get('href')
        news_header = news_table.find('span',class_='post-card-inline__title').text
        news_content = news_table.find('p',class_='post-card-inline__text').text
        news_date = news_table.find('time',class_='post-card-inline__date').get('datetime')
        news_views = news_table.find('div',class_='post-card-inline__stats').text
        news_data = [news_source,news_header,news_content,news_date,news_views]
        news_tables.append(news_data)
        
    #step 5. Create Dataframe
    df = pd.DataFrame(news_tables,columns=Headers)
    if existing_data is None:
        df.to_excel(xlwriter, sheet_name=file_base_name, index=False)
    else:
        existing_urls = existing_data['Source'].tolist()
        new_data = df[~df['Source'].isin(existing_urls)]
        if len(new_data) > 0:
            sheet = workbook[file_base_name]
            next_row = sheet.max_row + 1
            for row in dataframe_to_rows(new_data, index=False, header=False):
                for col, value in enumerate(row, start=1):
                    sheet.cell(row=next_row, column=col, value=value)
                next_row += 1
           
            xlwriter.save()

xlwriter.close()

