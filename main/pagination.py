import math
from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination, _positive_int, PageNumberPagination
from rest_framework.response import Response


class ProjectPagination(PageNumberPagination):
    page_header = 'X-Pagination-Current-Page'
    page_size_header = 'X-Pagination-Per-Page'
    page_size = 1
    max_page_size = 100

    def get_page_number(self, request, paginator):
        page_number = request.headers.get(self.page_header, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        return page_number

    def get_page_size(self, request):
        if self.page_size_header:
            try:
                return _positive_int(
                    request.headers[self.page_size_header],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(data, page_size)
        page_number = int(self.get_page_number(self.request, paginator))

        meta = OrderedDict([
            ('totalCount', self.page.paginator.count),
            ('pageCount', int(math.ceil(self.page.paginator.count / page_size))),
            ('currentPage', page_number),
            ('perPage', len(data)),
        ])
        return Response(OrderedDict([
            ('projects', data),
            ('meta', meta),
        ]))


class HistoryPagination(PageNumberPagination):
    page_header = 'X-Pagination-Current-Page'
    page_size_header = 'X-Pagination-Per-Page'
    page_size = 1
    max_page_size = 100

    def get_page_number(self, request, paginator):
        page_number = request.headers.get(self.page_header, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        return page_number

    def get_page_size(self, request):
        if self.page_size_header:
            try:
                return _positive_int(
                    request.headers[self.page_size_header],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(data, page_size)
        page_number = int(self.get_page_number(self.request, paginator))

        meta = OrderedDict([
            ('totalCount', self.page.paginator.count),
            ('pageCount', int(math.ceil(self.page.paginator.count / page_size))),
            ('currentPage', page_number),
            ('perPage', len(data)),
        ])
        return Response(OrderedDict([
            ('data', data),
            ('meta', meta),
        ]))
