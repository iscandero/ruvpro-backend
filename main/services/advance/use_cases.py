from django.db.models import Sum

from main.services.advance.selectors import get_advances_by_worker


def get_sum_advance_by_worker(worker):
    advance_aggregate = get_advances_by_worker(employee=worker).aggregate(sum_amounts=Sum('advance'))
    return advance_aggregate['sum_amounts']
