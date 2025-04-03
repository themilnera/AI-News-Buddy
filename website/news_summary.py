from fundus import PublisherCollection, Crawler
from fundus.scraping.filter import inverse, regex_filter
from . import ai_requests
from datetime import datetime
import asyncio

from . import db
from .models import News
from flask_login import current_user

crawler = Crawler(PublisherCollection.us)

async def _generate_article_summaries(article_amount, article_filter):
    summaries = [] 
    #filter for poltics should be something like 'politic'
    for article in crawler.crawl(max_articles=article_amount, url_filter=inverse(regex_filter(article_filter))):
        url = article.html.requested_url
        body = article.plaintext  # I'm choosing plaintext over .body for the AI
        summary = await ai_requests.gen_text(f"Summarize this article (in english) for later review, if the article is political, note any clear bias, logical errors, or misinformation: {body}", "You are a news article summarizer, use ### for headings * * around italicized text and ** ** around bold text, for new lines it should always be *heading* text or **bold**. Begin with writing a headline for an article, then go from there with your analysis", False)
        summaries.append(f"Article: {url}\n\n{summary}")
        print(f"Summaries compiled: {len(summaries)}")
        await asyncio.sleep(6) # Need to add more time between requests, I keep getting rate limited
    return summaries

async def _generate_summary_review(summaries):
    string_summaries = "\n\n".join(summaries)
    review = await ai_requests.gen_text(
        f"Review these news article summaries, and talk about today's news, focus on the more significant parts, and inform them on anything problematic in the articles. These are the summaries you wrote of today's news articles: {string_summaries}",
        "Your job is to report on today's current news, and tell the user about the news you found.", False)
    return review

async def news_review(count, filter):
    summaries = await _generate_article_summaries(count, filter)
    review = await _generate_summary_review(summaries)
    full_content = "\n\n".join(summaries) + "\n\n###Final Review:\n" + review

    new_entry = News(content=full_content, user_id=current_user.id)
    db.session.add(new_entry)
    db.session.commit()
    
    print(f"News for {datetime.now().strftime('%m-%d-%Y')} saved successfully!")
        
# asyncio.run(news_review(5, "politic"))