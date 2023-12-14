from functools import wraps
from typing import Callable

from flask import request, redirect, render_template, url_for

from security import has_token


def redirect_to_index_if_authed(function: Callable) -> Callable:
    @wraps(function)
    def decorator(*args, **kwargs):
        if has_token(request):
            return redirect(url_for('index'))

        return function(*args, **kwargs)

    return decorator


def render_template_if_method(template_name: str, methods: list[str]) -> Callable:
    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def _decorator(*args, **kwargs):
            if request.method in methods:
                return render_template(template_name)

            return function(*args, **kwargs)

        return _decorator

    return decorator
