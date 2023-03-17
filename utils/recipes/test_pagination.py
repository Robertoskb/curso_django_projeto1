from unittest import TestCase

from utils.recipes.pagination import make_pagination_range


def get_pagination(current_page):
    return make_pagination_range(
        page_range=list(range(1, 21)),
        num_pages=4,
        current_page=current_page,
    )


class PaginationTest(TestCase):

    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            num_pages=4,
            current_page=1,
        )

        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
        self.assertEqual(get_pagination(1)['pagination'], [1, 2, 3, 4])
        self.assertEqual(get_pagination(2)['pagination'], [1, 2, 3, 4])

    def test_make_sure_middle_ranges_are_correct(self):
        self.assertEqual(get_pagination(12)['pagination'], [11, 12, 13, 14])
        self.assertEqual(get_pagination(13)['pagination'], [12, 13, 14, 15])
        self.assertEqual(get_pagination(14)['pagination'], [13, 14, 15, 16])

    def test_make_pagination_is_static_when_last_page_is_next(self):
        self.assertEqual(get_pagination(18)['pagination'], [17, 18, 19, 20])
        self.assertEqual(get_pagination(19)['pagination'], [17, 18, 19, 20])
