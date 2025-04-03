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
        summary = await ai_requests.gen_text(f"Summarize this article: {body}", "You a news article summarizer/reporter, write a simple headline for the article that begins with '###' and then a simple two to three paragraph summary of a given article in plain text, without bulletpoints or any formatting syntax, just two to three plain text paragraphs. Maintain a skeptical perspective and call things into question if they seem skewed.", False)
        summaries.append(f"Article: {url}\n\n{summary}")
        print(f"Summaries compiled: {len(summaries)}")
        await asyncio.sleep(6) # Need to add more time between requests, I keep getting rate limited
    return summaries

async def _generate_summary_review(summaries):
    string_summaries = "\n\n".join(summaries)
    review = await ai_requests.gen_text(
        f"Review these news article summaries, and write a conclusion for them in a few paragraphs, using plaintext (no formatting) and a conversational tone. These are the summaries of today's news articles: {string_summaries}",
        "Your job is to read previously generated article summaries, then give a final thoughts/conclusion. Begin with a headline that looks exactly like this: ###Final Thoughts:", False)
    return review

async def news_review(count, filter):
    summaries = await _generate_article_summaries(count, filter)
    review = await _generate_summary_review(summaries)
    full_content = "\n\n".join(summaries) + "\n\n\n" + review

    new_entry = News(content=full_content, user_id=current_user.id)
    db.session.add(new_entry)
    db.session.commit()
    
    print(f"News for {datetime.now().strftime('%m-%d-%Y')} saved successfully!")
        