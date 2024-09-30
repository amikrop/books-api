from django.urls import path

from comments.views import CommentViewSet

comment_list = CommentViewSet.as_view({"get": "list", "post": "create"})
comment_detail = CommentViewSet.as_view({"delete": "destroy"})

urlpatterns = [
    path("books/<int:book_pk>/comments/", comment_list, name="comment-list"),
    path("comments/<int:pk>/", comment_detail, name="comment-detail"),
]
