from django.views.generic import ListView


class SearchView(ListView):

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['form'] = self.search_form(self.request.GET or None, queryset=self.get_queryset())
        if context['form'].is_valid():
            context['object_list'] = context['form'].search()
        return context
