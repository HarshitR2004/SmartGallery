import chromadb
from ..models.clip_model import CLIPFeatureExtractor
from fastapi import HTTPException

class ImageSearcher:
    _chroma_client = None
    _feature_extractor = None

    def __init__(self, user_id):
        self.user_id = user_id
        if ImageSearcher._chroma_client is None:
            ImageSearcher._chroma_client = chromadb.Client()
        if ImageSearcher._feature_extractor is None:
            ImageSearcher._feature_extractor = CLIPFeatureExtractor()

        try:
            self.collection = ImageSearcher._chroma_client.get_collection(name=self.user_id)
        except ValueError:
            raise HTTPException(status_code=404, detail=f"User collection for {self.user_id} not found. Please initialize.")
        
        print(f"Image searcher initialized for user {self.user_id}")

    def search_image(self, query: str):
        try:
            text_features = self._feature_extractor.extract_text_features(query)
            
            results = self.collection.query(
                query_embeddings=text_features.tolist(),
                n_results=1
            )

            if not results['documents'] or not results['documents'][0]:
                return {"image_path": "No image found"}

            image_path = results['documents'][0][0]
            
            return {"image_path": image_path}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to search for image: {e}")

