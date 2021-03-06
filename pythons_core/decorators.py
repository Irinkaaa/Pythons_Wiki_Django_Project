from django.http import HttpResponse


def group_required(groups=None):
    if groups is None:
        groups = []
    groups_set = set(groups)

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            user_groups = set([group.name for group in request.user.groups.all()])
            if user_groups.intersection(groups_set):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You're not authorized")

        return wrapper

    return decorator
