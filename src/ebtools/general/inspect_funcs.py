#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 21:28:31 2023

@author: eamonnbell
"""





import inspect
from collections.abc import Callable





def get_call_func_name() -> str:
    """
    Return the name of the calling function.

    Returns
    -------
    str
        Name of the function that called `get_call_func_name`.

    Examples
    --------
    >>> def outer():
    ...     return get_call_func_name()
    >>> outer()
    'outer'

    """
    current_frame = inspect.currentframe()
    
    if current_frame is None or current_frame.f_back is None:
        return ''
    
    return current_frame.f_back.f_code.co_name





def get_function_arguments(
        func: Callable[..., object],
        kwarg_values: bool = False
        ) -> tuple[str, ...]:
    """
    Return the parameter names or signature strings for a callable.
    
    Parameters
    ----------
    func : Callable
        Callable to inspect.
    kwarg_values : bool, default False
        If ``False``, return only parameter names. If ``True``, return
        signature strings including defaults where present.

    Returns
    -------
    tuple of str
        Parameter names or formatted parameter strings from `func`.

    Examples
    --------
    >>> def example(a, b=1):
    ...     return a + b
    >>> get_function_arguments(example)
    ('a', 'b')

    >>> get_function_arguments(example, kwarg_values=True)
    ('a', 'b=1')

    """
    signature = inspect.signature(func)
    
    if kwarg_values:
        return tuple(str(parameter) for parameter in signature.parameters.values())
    
    return tuple(signature.parameters)

