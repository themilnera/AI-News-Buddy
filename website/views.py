#routes for the website
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import News
from flask import jsonify
from . import db
import json
from datetime import datetime
from . import news_summary
import asyncio
from . import format
views = Blueprint('views', __name__)
#define views blueprint


#define home route
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user_news = News.query.filter_by(user_id=current_user.id).all()
    unique_dates = sorted(set(n.date_created.date() for n in user_news), reverse=True)
    return render_template("home.html", user=current_user, unique_dates=unique_dates)

@views.route("/generate-news", methods=["POST"])
def generate_news():
    try:
        data = request.json
        article_count = data.get("count", 5)
        article_filter = data.get("filter", "")
        asyncio.run(news_summary.news_review(article_count, article_filter))
        return jsonify({"message": "News generated successfully"}), 200
    except Exception as e:
        flash("Failed to get the news", "error")
        return jsonify({"error": str(e)})

@views.route('/news/<date>', methods=['GET'])
@login_required
def news_by_date(date):
    try:
        date_obj = datetime.strptime(date, "%m-%d-%Y").date()
    except ValueError:
        flash("Invalid date format.", category="error")
        return redirect(url_for("views.home"))
    news_entries = News.query.filter_by(user_id=current_user.id).filter(db.func.date(News.date_created) == date_obj).all()
    for news in news_entries:
        news.content = format.format_news_text(news.content)
    return render_template("news.html", user=current_user, news_entries=news_entries, date=date)


@views.route('/delete-news', methods=['POST'])
@login_required
def delete_news():
    data = json.loads(request.data)
    news_id = data.get('newsId')
    news = News.query.get(news_id)
    if news and news.user_id == current_user.id:
        db.session.delete(news)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success":False, "error":"Unauthorized"}), 403