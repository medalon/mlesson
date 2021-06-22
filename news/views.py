from django.shortcuts import render, get_object_or_404
from .models import News
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailNewsForm
from django.core.mail import send_mail


class NewsListView(ListView):
    queryset = News.published.all()
    context_object_name = 'news'
    paginate_by = 3
    template_name = 'news/list.html'


def news_list(request):
    object_list = News.published.all()
    paginator =Paginator(object_list, 3)
    page =request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        # если нет страниц, вернуть последнюю
        news = paginator.page(paginator.num_pages)

    return render(request,
                    'news/list.html',
                    {'page': page,
                    'news': news})


def news_detail(request, year, month, day, news):
    news = get_object_or_404(News, slug=news,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)



    new_comment = None


    return render(request,
                    'news/detail.html',
                    {'news': news,
                    'new_comment': new_comment,})


def news_share(request, news_id):
    news = get_object_or_404(News, id=news_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailNewsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # отправим почту
            news_url = request.build_absolute_uri(news.get_absolute_url())
            subject = f"{cd['name']} recommends you read {news.title}"
            message = f"Read {news.title} at {news_url}\n\n" \
                    f"{cd['name']}\'s comments: {cd['comments']}"
            
            send_mail(subject, message, 'hello@kah-kah.com', [cd['to']])
            sent = True
    else:
        form = EmailNewsForm()

    return render(request, 'news/share.html',
                    {'news': news,
                    'form': form,
                    'sent': sent})
