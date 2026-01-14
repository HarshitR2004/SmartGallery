# Smart Gallery: AI-Powered Semantic Image Search

A self-hosted image gallery that lets you search your photos with natural language. Find images based on content, not just tags or filenames.

## Features

- **Semantic Search:** Find images using descriptive text queries.
- **Fast & Efficient:** Uses a high-performance vector database for instant results.
- **Custom CLIP Model:** Powered by a custom-trained CLIP model for accurate image-text understanding.
- **Self-Hosted:** Keep your images private and run the application locally.
- **Bulk Ingestion:** Add entire folders of images at once.
- **Multi-User Support:** Creates separate collections for different users.
- **RESTful API:** A FastAPI backend provides a simple interface.

---

## How It Works

Smart Gallery uses a custom CLIP (Contrastive Language-Image Pre-Training) model to understand images and text. An Image Encoder (ViT) and a Text Encoder (BERT) convert images and text queries into vectors. The model finds the closest image vectors to your text query vector.

### Technology Stack

- **Backend:** FastAPI (Python)
- **ML Framework:** PyTorch
- **Transformers:** Hugging Face Transformers
- **Vector Database:** ChromaDB
- **Web Server:** Uvicorn

---

## Project Structure

```
smart_gallery_backend/
├── models/              # ML Model definitions
├── database/            # Database management
├── services/            # Business logic
├── routes/              # API endpoints
├── main.py              # FastAPI entry point
└── clip_model_epoch_30.pt # Pre-trained model weights
```

---



## API Endpoints

- `POST /db/initialize`: Create a new user session.
- `POST /images/add`: Add a single image.
- `POST /images/add-folder`: Add all images from a folder.
- `POST /images/search`: Search for an image with a text query.

See `/docs` for detailed request/response models.

