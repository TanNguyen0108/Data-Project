#Long Project for analysis the case study

Link drive for my database CSV files: https://drive.google.com/drive/folders/1t5ksthkCJLrmSy5kFjd6AkLbNGRzRBWh?usp=drive_link

Link drive for database SQLite: https://drive.google.com/file/d/1hiOj_HTp-p7HL3Dsa9u09yS-uApwwRfM/view?usp=drive_link
 
Crawl Restaurant's Infomation: 1.1 hcmc_foody.ipynb
Using Requests calling API of search page of Foody to get list of Restaurant. Because of the limited result, we split API by parameter district and category of the API. Extract restaurant ID from the list.
Using BeautifulSoup to get full detail of the restaurant from the Restaurant detail page.
Result: A table contains 101.401 rows and 33 columns(close to 130K restaurant in HCM at that time).
