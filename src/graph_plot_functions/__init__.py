from flask_caching import Cache

cache = Cache(
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": "gp_cache",
        "CACHE_THRESHOLD": 10,
    }
)
