from django import template
from ..models import News


register = template.Library()

@register.simple_tag
def total_news():
    return News.published.count()


@register.inclusion_tag('news/latest_news.html')
def show_latest_news(count=3):
    latest_news = News.published.order_by('-publish')[:count]
    return {'latest_news': latest_news}