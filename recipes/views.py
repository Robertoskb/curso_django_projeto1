import os

from django.db.models import Q
from django.http import Http404
from django.views.generic import DetailView, ListView

from utils.recipes.pagination import make_pagination

from .models import Recipe

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(is_published=True)
        queryset.select_related('author', 'category')
        queryset.prefetch_related('author__profile')

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        pag_obj, pagination_range = make_pagination(self.request,
                                                    context.get('recipes'),
                                                    PER_PAGE)

        context.update({
            'recipes': pag_obj,
            'pagination_range': pagination_range,
        })

        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.hmtl'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            is_published=True, category__id=self.kwargs.get('category_id'))

        if not queryset:
            raise Http404()

        return queryset


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404()

        queryset = queryset.filter(
            Q(Q(title__icontains=search_term) |
              Q(description__icontains=search_term)),
            is_published=True)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        search_term = self.kwargs.get('q', '').strip()

        context.update({
            'search_term': search_term,
            'page_title': f'Search for {search_term}',
            'additional_url_query': f'&q={search_term}',

        })

        return context


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(is_published=True)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'is_detail_page': True
        })

        return context
