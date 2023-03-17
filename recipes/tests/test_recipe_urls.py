from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):

    def test_recipes_home_url_is_correct(self):
        home_url = reverse('recipes:home')

        self.assertEqual(home_url, '/')

    def test_recipes_category_url_is_correct(self):
        category_url = reverse('recipes:category', kwargs={'category_id': 1})

        self.assertEqual(category_url, '/recipes/category/1/')

    def test_recipes_recipe_url_is_correct(self):
        recipe_url = reverse('recipes:recipe', kwargs={'pk': 1})

        self.assertEqual(recipe_url, '/recipes/1/')

    def test_recipes_search_url_is_correct(self):
        search_url = reverse('recipes:search')

        self.assertEqual(search_url, '/recipes/search/')
