from datetime import date, datetime
from django.views.generic.list import ListView
from webScraping.models import *
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Internship


@login_required
def favourite_list(request):
    current_user = request.user
    new = Internship.objects.filter(user=current_user.id)
    return render(request, 'webScraping/fav.html', {'new': new})


@login_required
def favourite_add(request, id):
    post = get_object_or_404(Internship, id=id)
    if post.user.filter(id=request.user.id).exists():
        post.user.remove(request.user)
    else:
        post.user.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ScrapeData:

    @classmethod
    def get_linkedin_data(cls):

        keywords = Keyword.objects.all()
        keyword_dict = cls.replace_space(keywords)
        job_data = list()

        for key, keyword in keyword_dict.items():
            url = f"https://www.linkedin.com/jobs/search/?currentJobId=3290944523&geoId=103030111&keywords={keyword}%20internship&location=Armenia&refresh=true&pageNum=0"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            get_list = soup.select('ul.jobs-search__results-list li')
            cat_id = Category.objects.get(id=key)

            for item in get_list:
                published_date = item.find("time", {"class": "job-search-card__listdate"})
                link = item.find("a", {"class": "base-card__full-link"})
                company = item.find("a", {"class": "hidden-nested-link"})

                if link is None or company is None or published_date is None:
                    continue
                # if published_date is date.today():
                data = {
                    "title": item.find("h3", class_="base-search-card__title").text,
                    "link": link.get('href'),
                    "company": company.text,
                    "category": cat_id
                }
                job_data.append(data)

        cls.store_data(job_data)
        return job_data

    @classmethod
    def get_staff_data(cls):

        url = "https://staff.am/en/jobs?JobsFilter%5Bcompany%5D=&JobsFilter%5Bkey_word%5D=&JobsFilter" \
              "%5Bjob_candidate_level%5D=&JobsFilter%5Bcategory%5D=&JobsFilter%5Bjob_type%5D=&JobsFilter%5Bjob_type" \
              "%5D%5B%5D=3&JobsFilter%5Bsalary%5D=&JobsFilter%5Bjob_term%5D=&JobsFilter%5Bjob_city%5D=&JobsFilter" \
              "%5Bsort_by%5D=&&JobsFilter%5Bsort_by%5D=0"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        get_list = soup.select('div.list-view div.featured-job')
        job_data = list()
        cat_id = Category.objects.get(title='Uncategorized')

        for item in get_list:
            link = item.find("a")
            title = item.find("p", {"class": "font_bold"})
            company = item.find("p", {"class": "job_list_company_title"})
            published_date = item.find("span", {"class": "formatted_date"}).text
            website_url = "https://staff.am"
            format_date = datetime.strptime(published_date, '%d %B %Y').strftime('%Y-%m-%d')

            # if format_date == date.today():
            data = {
                "title": title.text,
                "link": website_url + link.get("href"),
                "company": company.text,
                "category": cat_id
            }
            job_data.append(data)

        cls.store_data(job_data)
        return job_data

    @classmethod
    def replace_space(cls, keyword_list):
        keyword_dict = dict()

        for item in keyword_list:
            key = item.category_id
            keyword = str(item.keyword).replace(" ", "%20")
            keyword_dict[key] = keyword

        return keyword_dict

    @classmethod
    def store_data(cls, data_list):

        if bool(data_list):
            print(data_list)
            for data in data_list:
                Internship.objects.create(**data)
            return True
        return False


class InternshipView(ListView):
    model = Internship
    context_object_name = 'internships'
    template_name = "webScraping/internship_list.html"

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context.update({'categories': categories})
        current_time = datetime.now().strftime('%H:%M:%S')

        if current_time == "01:00:00":
            ScrapeData.get_linkedin_data()
            ScrapeData.get_staff_data()

        return context


class InternshipCategoryView(ListView):
    model = Internship
    template_name = "webScraping/index.html"
    context_object_name = 'internships'
    allow_empty = False

    def get_queryset(self):
        return Internship.objects.filter(category__slug=self.kwargs['cat_slug']).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['cat_selected'] = context['internships'][0].category_id
        context['categories'] = categories
        return context
