import inspect
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from typing import List, Optional, Type, Callable, Any
from django.views import View

EXCLUDE_METHODS = {
        "__init__",
        "_allowed_methods",
        "_clean_data",
        "_get_ip_address",
        "_get_response_ms",
        "_get_user",
        "_get_view_method",
        "_get_view_name",
        "check_object_permissions",
        "check_permissions",
        "check_throttles",
        "determine_version",
        "dispatch",
        "filter_queryset",
        "finalize_response",
        "get_authenticate_header",
        "get_authenticators",
        "get_content_negotiator",
        "get_exception_handler",
        "get_exception_handler_context",
        "get_extra_action_url_map",
        "get_format_suffix",
        "get_object",
        "get_paginated_response",
        "get_parser_context",
        "get_parsers",
        "get_permissions",
        "get_queryset",
        "get_renderer_context",
        "get_renderers",
        "get_serializer",
        "get_serializer_class",
        "get_serializer_context",
        "get_success_headers",
        "get_throttles",
        "get_view_description",
        "get_view_name",
        "handle_exception",
        "handle_log",
        "http_method_not_allowed",
        "initial",
        "initialize_request",
        "options",
        "paginate_queryset",
        "perform_authentication",
        "perform_content_negotiation",
        "perform_create",
        "perform_destroy",
        "perform_update",
        "permission_denied",
        "raise_uncaught_exception",
        "reverse_action",
        "setup",
        "should_log",
        "throttled",
    }


def apply_swagger_auto_schema(
        tags: Optional[List[str]] = None,
        default_schema: Optional[Any] = None,
        excluded_methods: Optional[List[str]] = None,
) -> Callable[[Type[View]], Type[View]]:
    """
    Декоратор для применения swagger_auto_schema ко всем методам представления, кроме исключённых.

    :param tags: Список тегов для схемы Swagger.
    :param default_schema: Объект схемы Swagger по умолчанию.
    :param excluded_methods: Список имен методов, которые не следует декорировать.
    :return: Декорированный класс представления.
    """
    if tags is None:
        tags = []
    if excluded_methods is None:
        excluded_methods = []

    exclude = set(EXCLUDE_METHODS)
    exclude.update(excluded_methods)

    if default_schema is None:
        tags = tags if tags else ['default_tags']
        default_schema = swagger_auto_schema(tags=tags)

    def decorator_fn(view_cls: Type[View]) -> Type[View]:
        for name, method in inspect.getmembers(view_cls, predicate=inspect.isfunction):
            if name not in exclude:
                decorator = method_decorator(default_schema)(method)
                setattr(view_cls, name, decorator)

        return view_cls

    return decorator_fn