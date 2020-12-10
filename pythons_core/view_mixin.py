from django.core.exceptions import PermissionDenied


class GroupRequiredMixin:
    groups = None

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            raise PermissionDenied
        group_set = set(self.groups or [])
        user_groups = set([group.name for group in request.user.groups.all()])
        if not user_groups.intersection(group_set) and not user.is_superuser:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
