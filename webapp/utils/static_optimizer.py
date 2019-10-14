from flask_compress import Compress
from flask_cachebuster import CacheBuster

asset_compressor = Compress()

cache_config = {
    'extensions': ['.js', '.css'],  # allowed extentions for caching
    'hash_size': 10                         # length of hash string
}

cache_buster = CacheBuster(config=cache_config)
