from unittest.mock import Mock, patch

from ebtools.general.online import is_online


def test_is_online_returns_true_when_connection_succeeds():
    connection = Mock()
    connection.__enter__ = Mock(return_value=connection)
    connection.__exit__ = Mock(return_value=None)

    with patch(
        "ebtools.general.online.socket.create_connection",
        return_value=connection,
    ) as create_connection:
        result = is_online(host="example.com", port=443, timeout=1.5)

    assert result is True
    create_connection.assert_called_once_with(("example.com", 443), timeout=1.5)


def test_is_online_returns_false_when_connection_fails():
    with patch(
        "ebtools.general.online.socket.create_connection",
        side_effect=OSError,
    ) as create_connection:
        result = is_online(host="example.com", port=443, timeout=1.5)

    assert result is False
    create_connection.assert_called_once_with(("example.com", 443), timeout=1.5)
