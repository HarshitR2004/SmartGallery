import chromadb
import os
from ..models.clip_model import CLIPFeatureExtractor
from fastapi import HTTPException

class ImageDBManager:
    _instance = None
    _chroma_client = None
    _feature_extractor = None

    def __init__(self, user_id):
        self.user_id = user_id
        if ImageDBManager._chroma_client is None:
            ImageDBManager._chroma_client = chromadb.Client()
        if ImageDBManager._feature_extractor is None:
            ImageDBManager._feature_extractor = CLIPFeatureExtractor()
        
        self.collection = ImageDBManager._chroma_client.get_or_create_collection(name=self.user_id)
        print(f"DB Manager initialized for user {self.user_id}")

    @classmethod
    def get_instance(cls, user_id):
        if cls._instance is None:
            cls._instance = ImageDBManager(user_id)
        else:
            cls._instance.user_id = user_id
            cls._instance.collection = cls._chroma_client.get_or_create_collection(name=user_id)
        return cls._instance

    def add_image(self, image_path: str):
        if not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail=f"Image not found at {image_path}")
        
        try:
            features = self._feature_extractor.extract_image_features(image_path)
            
            self.collection.add(
                embeddings=features.tolist(),
                documents=[image_path],
                ids=[image_path]
            )
            
            print(f"Added image {image_path} for user {self.user_id}")
            return {"status": "success", "message": f"Added image: {image_path}"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process image {image_path}: {e}")

    def add_images_from_folder(self, folder_path: str):
        if not os.path.isdir(folder_path):
            raise HTTPException(status_code=404, detail=f"Folder not found at {folder_path}")

        added_images_count = 0
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(folder_path, filename)
                try:
                    self.add_image(image_path)
                    added_images_count += 1
                except HTTPException as e:
                    print(e.detail)
                except Exception as e:
                    print(f"Could not process {image_path}: {e}")
        
        return {"status": "success", "message": f"Added {added_images_count} images from: {folder_path}"}

