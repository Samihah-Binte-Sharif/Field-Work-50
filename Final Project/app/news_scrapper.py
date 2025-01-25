import cloudscraper
from bs4 import BeautifulSoup
from lxml import html
from .database import SessionLocal
from .crud import create_news
from .schemas import NewsCreate

def single_news_scraper(url: str):
    scraper = cloudscraper.create_scraper()
    try:
        response = scraper.get(url)
        if response.status_code == 200:
            print('Response Successful!!')
        else:
            print(f"Failed to fetch the webpage. Status code: {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        tree = html.fromstring(response.text)

        # Extract publisher information
        publisher_website = url.split('/')[2]
        publisher = publisher_website.split('.')[-2]
        
        # print(f"Scraped news from {publisher_website}")
        
        # Extract the title
        title = soup.select_one('h1.text-3xl').text.strip() if soup.select_one('h1.text-3xl') else "No Title"
        
        # print(f"Title: {title}")
        
        # Extract the reporter name
        reporter = soup.select_one('.contributor-name').text.strip() if soup.select_one('.contributor-name') else "No Reporter"
        
        # print(f"Reporter: {reporter}")
        
        datetime = soup.select('body > section > div > div:nth-child(2) > div.grid.lg\:grid-cols-\[200px_auto_300px\].gap-6.mb-6 > div:nth-child(2) > div.mb-3 > div.mb-4.flex.flex-col.lg\:flex-row.lg\:items-center.gap-x-6.gap-y-1 > div')
        
        news_datetime = datetime[0].text.strip() if datetime else "No Date"
        
        # print(f"Date: {news_datetime}")
         
        # Extract the news category using XPath
        category_element = soup.select('body > section > div > div:nth-child(2) > div.grid.lg\:grid-cols-\[200px_auto_300px\].gap-6.mb-6 > div:nth-child(2) > div.mb-3 > div.mb-3 > div > a > div > span:nth-child(2)')
        news_category = category_element[0].text.strip() if category_element else "No Category"
        
        # print(f"Category: {news_category}")
        
        # Extract the news content
        content = '\n'.join([p.text.strip() for p in soup.find_all('p')])
        
        # Extract image URLs
        img_tags = soup.find_all('img')
        images = [img['src'] for img in img_tags if img.has_attr('src')]
        
        # print(f"Images: {images}")
        
        # Return the data as a NewsCreate object
        return NewsCreate(
            publisher_website=publisher_website,
            news_publisher=publisher,
            title=title,
            news_reporter=reporter,
            datetime=news_datetime,
            link=url,
            news_category=news_category,
            body=content,
            images=images,
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def scrape_and_store_news(url: str, db: SessionLocal):
    news_data = single_news_scraper(url)
    #print(news_data)
    inserted_news = ""
    if news_data:
        inserted_news = create_news(db=db, news=news_data)
    db.close()

    return inserted_news

# # Create a new database session
# db_session = SessionLocal()

# # Define the URL of the news article to scrape
# news_url = "https://dailyamardesh.com/world/amdppidimm1ne"

# # Call the scrape_and_store_news function
# result = scrape_and_store_news(url=news_url, db=db_session)

# if result:
#     print("News scraped and stored successfully!")
# else:
#     print("Failed to scrape or store the news.")
