from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeRecipeViewTest(RecipeTestBase):
    def test_recipes_recipe_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': recipe.id}))

        self.assertEqual(response.status_code, 404)

    def test_recipes_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.RecipeDetailView)

    def test_recipes_recipe_template_loads_the_correct_correct_recipe(self):
        needed_title = 'Recipe Title'
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': 1}))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_return_status_code_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)
