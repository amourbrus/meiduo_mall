from rest_framework.pagination import PageNumberPagination


class StandardResultSetPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 20    # 前端可以实现的最大值
    page_size_query_param = 'page_size'
