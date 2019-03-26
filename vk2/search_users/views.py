from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.shortcuts import render
from django.views import View
from account.models import Account


class Search(View):
    def get(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        search_vector = SearchVector('first_name', 'last_name')
        value = request.GET['value']
        search_query = SearchQuery(value)
        result = Account.objects.annotate(search=search_vector).filter(search=search_query)
        number_result = result.count()
        return render(request, 'search_users/search_page.html', context={'result': result,
                                                                         'number_result': number_result,
                                                                         'main_user': main_user,
                                                                         'value': value})
