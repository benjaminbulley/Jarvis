import pytest
from unittest import mock
from source.add_blob import add_blob


def test_add_blob():
    """ Test add_blob() with a mock cursor to ensure the execute method is called with
    the correct SQL expression.
    """
    cur = mock.MagicMock()
    title = "empty"
    data = b"\0\0\0"
    size = 0
    music = False
    loud = False
    # Call the function being tested, and check return value
    assert add_blob(cur, title, data, size, music, loud) == True
    # Was execute() called?
    cur.execute.assert_called()
    # Can also test if the correct arguments were given, like this -
    cur.execute.assert_called_with('INSERT INTO "clips" ("path", "content", "size", "music", "loud") VALUES (?, ?, ?, ?, ?)', mock.ANY)
