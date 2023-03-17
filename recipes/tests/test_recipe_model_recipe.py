from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase


class TestModelRecipe(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()

        return super().setUp()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65)
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length + 1))

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_string_representation(self):
        self.recipe.title = 'Title representation'
        self.recipe.full_clean()
        self.recipe.save()

        self.assertEqual(self.recipe.title, str(self.recipe))
