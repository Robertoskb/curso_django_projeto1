from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search',))
        self.assertIs(view.func.view_class, views.RecipeListViewSearch)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=search')

        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_seach_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))

        self.assertEqual(response.status_code, 404)
