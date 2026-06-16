from ebtools.general.inspect_funcs import (
    get_call_func_name,
    get_function_arguments,
)


def test_get_call_func_name_returns_immediate_caller_name():
    def immediate_caller():
        return get_call_func_name()

    assert immediate_caller() == "immediate_caller"


def test_get_call_func_name_reports_direct_caller_only():
    def direct_caller():
        return get_call_func_name()

    def indirect_caller():
        return direct_caller()

    assert indirect_caller() == "direct_caller"


def test_get_function_arguments_returns_parameter_names():
    def example(required, optional=1):
        return required + optional

    assert get_function_arguments(example) == ("required", "optional")


def test_get_function_arguments_returns_signature_strings_with_defaults():
    def example(required, optional=1):
        return required + optional

    assert get_function_arguments(example, kwarg_values=True) == (
        "required",
        "optional=1",
    )


def test_get_function_arguments_handles_signature_parameter_kinds():
    def example(pos_only, /, regular, *args, keyword_only=3, **kwargs):
        return pos_only, regular, args, keyword_only, kwargs

    assert get_function_arguments(example) == (
        "pos_only",
        "regular",
        "args",
        "keyword_only",
        "kwargs",
    )
    assert get_function_arguments(example, kwarg_values=True) == (
        "pos_only",
        "regular",
        "*args",
        "keyword_only=3",
        "**kwargs",
    )


def test_get_function_arguments_accepts_callable_object():
    class ExampleCallable:
        def __call__(self, value, scale=1):
            return value * scale

    assert get_function_arguments(ExampleCallable()) == ("value", "scale")
    assert get_function_arguments(ExampleCallable(), kwarg_values=True) == (
        "value",
        "scale=1",
    )
