import socket


def is_online(
        host: str = "8.8.8.8",
        port: int = 53,
        timeout: float = 5.0
        ) -> bool:
    """
    Return whether a network connection can be opened.

    Parameters
    ----------
    host : str, default "8.8.8.8"
        Host to connect to when checking network access.
    port : int, default 53
        Port to connect to on `host`.
    timeout : float, default 5.0
        Maximum number of seconds to wait for the connection attempt.

    Returns
    -------
    bool
        ``True`` if a socket connection can be opened. ``False`` if the
        connection attempt fails with an `OSError`.

    Notes
    -----
    This checks whether the machine can reach a specific host and port. It
    does not guarantee that all internet services are reachable.

    Examples
    --------
    >>> is_online()
    True

    >>> is_online(host="1.1.1.1", port=53, timeout=2.0)
    True

    """
    try:
        # Attempt to connect to a reliable host and close the socket promptly.
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False
