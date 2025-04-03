import re

def format_news_text(text):
    """Formats AI-generated text to HTML."""
    text = re.sub(r'### (.*?)\n', r'<h3>\1</h3>', text)  # Convert ### to <h3>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)  # Italics
    text = re.sub(r'\n- (.*?)\n', r'\n<ul><li>\1</li></ul>\n', text)  # Lists
    text = re.sub(r'</ul>\n<ul>', '', text)  # Fix nested <ul> tags
    text = re.sub(r'Article: (https?://\S+)', r'<a href="\1" target="_blank">\1</a>', text)
    return text

