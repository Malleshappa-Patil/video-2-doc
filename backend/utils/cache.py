import json
import hashlib
import os

CACHE_FILE = "cache.json"

def _load_cache() -> dict:
    """Loads the cache file, creating it if it doesn't exist."""
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def _save_cache(cache_data: dict):
    """Persists the cache dictionary to disk."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f, indent=4)

def generate_hash(input_data: str, is_file: bool = False) -> str:
    """Generates a unique SHA-256 hash for a URL or local file content."""
    hasher = hashlib.sha256()
    if is_file:
        # Read the file in chunks so we don't blow up memory on large video files
        with open(input_data, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
    else:
        # Just hash the URL string
        hasher.update(input_data.encode('utf-8'))
    return hasher.hexdigest()

def check_cache(input_hash: str) -> dict | None:
    """Returns the cached metadata (like ChromaDB collection IDs) if processed."""
    cache = _load_cache()
    return cache.get(input_hash)

def save_to_cache(input_hash: str, data: dict):
    """Saves the processing results/metadata into the cache."""
    cache = _load_cache()
    cache[input_hash] = data
    _save_cache(cache)