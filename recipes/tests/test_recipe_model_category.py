from recipes.tests.test_recipe_base import RecipeTestBase


class TestCategoryModel(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category()

        return super().setUp()

    def test_string_representation(self):
        self.category.name = 'Name representation'
        self.category.full_clean()
        self.category.save()

        self.assertEqual(self.category.name, str(self.category))
