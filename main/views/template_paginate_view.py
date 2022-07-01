import math

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ViewPaginatorMixin(object):
    min_limit = 1
    max_limit = 100

    def paginate(self, object_list, page, limit, name_objects, **kwargs):
        try:
            page = int(page)
            if page < 1:
                page = 1
        except (TypeError, ValueError):
            page = 1

        try:
            limit = int(limit)
            if limit < self.min_limit:
                limit = self.min_limit
            if limit > self.max_limit:
                limit = self.max_limit
        except (ValueError, TypeError):
            limit = self.max_limit

        paginator = Paginator(object_list, limit)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        total_count = len(object_list)

        meta = {
            'totalCount': total_count,
            'pageCount': int(math.ceil(total_count / limit)),
            'currentPage': page,
            'perPage': len(objects),
        }

        data = {
            f'{name_objects}': list(objects),
            'meta': meta

        }
        return data
