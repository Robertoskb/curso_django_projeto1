import math

from django.core.paginator import Paginator


def make_pagination_range(page_range, num_pages, current_page):
    middle = math.ceil(num_pages / 2)
    start = current_page - middle
    stop = current_page + middle
    total_pages = len(page_range)

    start_offset = abs(start) if start < 0 else 0

    if start < 0:
        start = 0
        stop += start_offset

    if stop >= total_pages:
        start = start - abs(total_pages - stop)

    pagination = page_range[start:stop]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'num_pages': num_pages,
        'total_pages': total_pages,
        'current_page': current_page,
        'start': start,
        'stop': stop,
        'first_page_out_of_range': current_page > middle,
        'last_page_out_of_range': stop < total_pages
    }


def make_pagination(request, queryset, per_page, qty_pages=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(queryset, per_page)
    pagination_range = make_pagination_range(
        paginator.page_range, qty_pages, current_page)

    pag_obj = paginator.get_page(current_page)

    return pag_obj, pagination_range
