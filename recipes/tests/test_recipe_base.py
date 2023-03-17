from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(self,
                    first_name='user',
                    last_name='name',
                    username='username',
                    password='123456',
                    email='username@email.com'):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(self,
                    category=None,
                    author=None,
                    title='Recipe Title',
                    description='Recipe Description',
                    slug='recipe-slug',
                    preparation_time=10,
                    preparation_time_unit='Minutos',
                    servings=5,
                    servings_unit='Porções',
                    preparation_steps='Recipe Preparation Steps',
                    preparation_steps_is_html=False,
                    is_published=True):

        return Recipe.objects.create(  # noqa F841
            category=category or self.make_category(),
            author=author or self.make_author(),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )

    def make_recipes_for_pagination(self, qty_recipes):
        category = self.make_category()
        recipes = []
        for i in range(qty_recipes):
            kwargs = {
                'title': f'Recipe Title {i}',
                'slug': f'r{i}',
                'author': self.make_author(username=f'u{i}',),
                'category': category
            }
            recipes.append(self.make_recipe(**kwargs))

        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    ...
