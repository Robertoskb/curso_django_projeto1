from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

    def test_recipe_home_return_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found here',
                      response.content.decode('utf-8'),)

    def test_recipe_home_template_loads_recipes(self):
        needed_title = 'Recipe Title'

        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'No recipes found here',
            response.content.decode('utf-8')
        )

    @patch('recipes.views.PER_PAGE', new=9)
    def test_recipe_home_is_paginated(self):
        self.make_recipes_for_pagination(18)

        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.get_page(1)), 9)

    def test_recipe_home_returns_page_1_if_page_is_not_int(self):
        response = self.client.get(reverse('recipes:home')+'?page=str')

        context = response.context

        current_page = context['pagination_range']['current_page']

        self.assertEqual(current_page, 1)
