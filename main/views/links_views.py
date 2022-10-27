from rest_framework.generics import ListAPIView

from main.serializers.links_serializers import LinkSerializer
from main.services.links.selectors import get_all_links


class LinkListAPIView(ListAPIView):
    serializer_class = LinkSerializer
    queryset = get_all_links()
