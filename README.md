# Webscraping
I've created this repository to share my a few webscraping codes from sites including Investing.com, Decrypt & Cointelegraph. These codes were made as of Apr2023 and I wanted to test the extent of ChatGPT & how much we can rely on ChatGPT to code. By way of introduction, I have fundamental knowledge on Python and learnt it fully-self taught via a couple of books and websites. My profession is in the Treasury space which deals mainly with excel, limited VBA and SQL. The following codes are just initial stages of my larger goal, which is trading via Sentiment analysis and different parameters.

In summary, ChatGPT (free version) is only useful to a certain extent as there are some code logics which it was not able to fulfill. Take for example to append new data into an existing excel sheet & I was usuing xlswriter, ChatGPT would give an appropriate fix using openpyxl, but at the same time conflict with some of my codes related to hyperlinking cells in the workbook. However, using ChatGPT definitely helped with de-bugging efficiently and time-saving. You could use ChatGPT to generate the initial code, but some knowledge on Python is still essential to understand and fix the the code ChatGPT generates for you.

Also, I use a Macbook and program the scripts to run automatically on a periodic basis via Crontab. However, one downside about Crontab is that it doesn't run the code when my laptop is closed. I am still trying to figure out how to overcome this restriction.

# Investing.com
This script would webscrape economic events in the US & Singapore, according to GMT+8 Timezone for events rating 3* (high importance). The events are separated by This week & Next week, and programmed to overwrite existing excel with its respective tabs. The code uses Selenium rather than BeautifuSoup as the website contains JavaScript which could not be parsed by bs. Selenium therefore helps to manually click and change tabs on the main economic calendar table, then retrieves the data from the table and store it into the excel.

# Decrypt
As a crypto enthusiast, I decided to parse news from Decrypt.co. I was able to use BeautifulSoup for this as the site does not involve the use of Js. The code would automatically parse the header, content, time of publication & category for each news article and append it into the existing excel sheet. Note that the excel sheet will have to be available in the source path prior to running the script. The code appends new news sources from the side into this existing workbook & again, I run it every hour using Crontab to fetch the latest news.

# Cointelegraph
This script would scrape news from Cointelegraph, which HTML was designed a little different from Decrypt as each "category" has a different website extension. Hence, the script would scrape news from 9 different URLs of different categories, parse it and append it into the existing workbook into tabs of their category. BeautifulSoup is used again over here as there is no need for interaction with Js.

# Summary
There are reporsitories, sites & sources out there which probably have codes to webscrape these sites. I did refer to some of these sources while creating my code, but realize that it was hard to find a one-size-fit-all reference, and some of these sources have already been outdated. Take for example when using Selenium.webdriver to find_element_by_XXX, the old version would allow you to use find_element_by_tag(), but after the update, this method does not work anymore, and you will have to find_element(By.Tag,'br') for example.
