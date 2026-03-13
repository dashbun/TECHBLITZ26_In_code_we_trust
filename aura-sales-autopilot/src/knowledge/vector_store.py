import json
import re
from difflib import SequenceMatcher

class ProductSearch:
    def __init__(self, products):
        self.products = products
        self.index = self._build_index()
    
    def _build_index(self):
        """Build simple keyword index"""
        index = {}
        for product in self.products:
            # Index all searchable fields
            text = f"{product['brand']} {product['title']} {product['category']} {' '.join(product['tags'])}".lower()
            index[product['id']] = {
                'product': product,
                'text': text,
                'words': set(re.findall(r'\w+', text))
            }
        return index
    
    def search(self, query, limit=5):
        """Simple keyword matching with relevance scoring"""
        query_words = set(re.findall(r'\w+', query.lower()))
        scores = []
        
        for pid, data in self.index.items():
            # Calculate overlap
            common = query_words.intersection(data['words'])
            if common:
                score = len(common) / len(query_words) if query_words else 0
                
                # Boost for brand matches
                product = data['product']
                if product['brand'].lower() in query.lower():
                    score *= 1.5
                
                # Boost for category matches
                if product['category'].lower() in query.lower():
                    score *= 1.3
                
                scores.append((score, product))
        
        # Sort by score and return top results
        scores.sort(reverse=True, key=lambda x: x[0])
        return [p for s, p in scores[:limit] if s > 0.1]
    
    def get_recommendations(self, category=None, tags=None, limit=4):
        """Get recommendations based on category or tags"""
        if category:
            filtered = [p for p in self.products if p['category'] == category]
        elif tags:
            filtered = [p for p in self.products if any(tag in p['tags'] for tag in tags)]
        else:
            filtered = self.products
        
        # Sort by rating and return top
        filtered.sort(key=lambda x: x['rating'], reverse=True)
        return filtered[:limit]
