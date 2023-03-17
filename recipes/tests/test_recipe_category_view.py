from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    @patch('recipes.views.PER_PAGE', new=9)
    def test_recipe_category_is_paginated(self):
        self.make_recipes_for_pagination(18)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        recipes = response.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.get_page(1)), 9)

    def test_recipe_category_template_is_correct(self):
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))

        self.assertTemplateUsed(response, 'recipes/pages/category.hmtl')

    def test_recipe_category_view_raises_404_if_category_not_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))

        self.assertEqual(404, response.status_code)
