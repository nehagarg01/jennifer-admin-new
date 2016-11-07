from django.views.generic import ListView


class SearchView(ListView):

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['form'] = self.search_form(self.request.GET or None, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        form = self.search_form(self.request.GET or None, queryset=queryset)
        if form.is_valid():
            queryset = form.search()
        return queryset
