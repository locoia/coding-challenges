def test_ping(app):
    res = app.get("/ping")
    assert "pong" == res.text


def test_search_pattern(app):
    res = app.post(
        "/api/v1/search", json={"username": "justdionysus", "pattern": "import"}
    )

    assert {
        "matches": [
            "https://gist.githubusercontent.com/justdionysus/c8693981025287ea858d2ca5a93ec103/raw/a1352c102b8d47e580cc773e56af9968f7fca03a/bflt.py",
            "https://gist.githubusercontent.com/justdionysus/65e6162d99c2e2ea8049b0584dd00912/raw/956c62609ab7ea695731bc836ccf85290809a59e/john_waters.py.nosecrets",
        ],
        "pagination": {"page": 1, "per_page": 10, "total": 4},
        "pattern": "import",
        "status": "success",
        "username": "justdionysus",
    } == res.json


def test_rate_control(app):
    res = app.get("/ping")
    res = app.get("/ping")
    res = app.get("/ping")
    assert {
        "code": 429,
        "description": "2 per 1 minute",
        "name": "Too Many Requests",
    } == res.json
