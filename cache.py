# cache.py
import pickle
import os
import hashlib
from functools import wraps
import time

class TranslationCache:
    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_key(self, text, language):
        """Generate cache key for text and language combination"""
        content = f"{text}_{language}".encode('utf-8')
        return hashlib.md5(content).hexdigest()
    
    def get(self, text, language):
        """Get cached translation if available"""
        cache_key = self.get_cache_key(text, language)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                    # Check if cache is still valid (24 hours)
                    if time.time() - cached_data['timestamp'] < 86400:
                        return cached_data['result']
            except Exception:
                pass
        return None
    
    def set(self, text, language, result):
        """Cache translation result"""
        cache_key = self.get_cache_key(text, language)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        cache_data = {
            'result': result,
            'timestamp': time.time()
        }
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
        except Exception:
            pass

def cached_translation(cache_instance):
    """Decorator for caching translations"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, text, language='isl'):
            # Check cache first
            cached_result = cache_instance.get(text, language)
            if cached_result:
                return cached_result
            
            # Perform translation
            result = func(self, text, language)
            
            # Cache successful results
            if result.get('success'):
                cache_instance.set(text, language, result)
            
            return result
        return wrapper
    return decorator
