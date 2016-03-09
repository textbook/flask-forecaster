"""Useful values to keep around."""

status = type('HttpStatusCodes', (object,), dict(
    NOT_FOUND=404,
    REDIRECTED=302,
    OK=200,
))
