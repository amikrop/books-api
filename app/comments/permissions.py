from rest_framework import permissions


class CommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            # "Create" permissions
            return view.book.comments_allowed and request.user.is_authenticated

        # "List" permissions
        return True

    def has_object_permission(self, request, view, obj):
        # "Destroy" permissions
        return obj.user == request.user or request.user.is_staff
