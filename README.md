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

Smart Gallery uses a custom CLIP (Contrastive Language-Image Pre-Training) model to map images and text to a shared embedding space. This is achieved through two main components: an image encoder and a text encoder.

### Image Encoder: ResNet50

A pre-trained ResNet50 model, with its final classification layer removed, is used to extract high-level features from images. The weights of the initial layers are frozen, while the final few layers are fine-tuned to adapt the features for the retrieval task. The output is a dense vector (embedding) that represents the semantic content of the image.

### Text Encoder: BERT

The text encoder is based on the `bert-base-uncased` model. Similar to the image encoder, the majority of the layers are frozen, with only the last two layers being fine-tuned. This allows the model to adapt to the specific language style of the image descriptions. The model processes a text query and generates a corresponding embedding.

### The CLIP Model

The image and text embeddings are projected into a shared space of the same dimension. The model is trained using a contrastive loss function, which aims to maximize the cosine similarity between corresponding image-text pairs while minimizing the similarity between non-matching pairs. This process aligns the vector representations of images and their textual descriptions in the embedding space, enabling effective semantic search.

### Technology Stack

- **Backend:** FastAPI (Python)
- **ML Framework:** PyTorch
- **Transformers:** Hugging Face Transformers
- **Vector Database:** ChromaDB
- **Web Server:** Uvicorn

---

## Model Performance

This project uses a custom CLIP-style model with a ResNet50 and BERT architecture, trained on a domain-specific dataset. Unlike large-scale models, it is optimized for retrieval quality under limited compute.

### Quantitative Comparison

| Model                     | Training Scale         | MRR     | MAP     |
| ------------------------- | ---------------------- | ------- | ------- |
| OpenAI CLIP (ViT-B/32)    | Web-scale (400M+ pairs)| ~0.6–0.7| ~0.7–0.8|
| OpenCLIP (LAION)          | Web-scale              | ~0.7+   | ~0.8+   |
| **Custom ResNet50 + BERT**| **Domain-specific**    | **0.3** | **0.9** |

### Interpretation

-   **High MAP (0.9):** Indicates strong semantic alignment. The model consistently ranks relevant images highly.
-   **Lower MRR (0.3):** The top-1 result may not always be the most relevant, a common trade-off with smaller, domain-specific datasets and limited compute.

This performance profile is ideal for retrieval systems where returning a set of relevant items is prioritized over achieving perfect top-1 accuracy.


---

## Getting Started

### 1. Model Download

The pre-trained CLIP model is too large for this repository. Download it from the link below and place it in the `backend/models/` directory.

[**Download Model**](https://drive.google.com/file/d/1neTz_juoWwdKnVqiyJOtQxdsn0mlPpgR/view?usp=sharing)

### 2. Prerequisites
- Python 3.8+
- `pip`

### 3. Installation & Setup

1.  **Clone the repository and navigate to the backend:**
    ```bash
    git clone <repository_url>
    cd SmartGallery/backend
    ```

2.  **Install dependencies (a virtual environment is recommended):**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
    The API will be live at `http://localhost:8000/docs`.

---
## Usage

Interact with the API using tools like `curl` or Postman.

### 1. Initialize the Database
Create a unique user session to get a `user_id`.

```bash
curl -X POST "http://localhost:8000/db/initialize" -H "Content-Type: application/json" -d '{"user_name": "my_gallery"}'
```
**Save the `user_id` for all future requests.**

### 2. Add Images
Add a single image or an entire folder.

**Add a single image:**
```bash
curl -X POST "http://localhost:8000/images/add?user_id=YOUR_USER_ID" -H "Content-Type: application/json" -d '{"image_path": "/path/to/your/image.jpg"}'
```

**Add a folder of images:**
```bash
curl -X POST "http://localhost:8000/images/add-folder?user_id=YOUR_USER_ID" -H "Content-Type: application/json" -d '{"folder_path": "/path/to/your/pictures_folder"}'
```

### 3. Search for Images
Search for images using a natural language query.

```bash
curl -X POST "http://localhost:8000/images/search?user_id=YOUR_USER_ID" -H "Content-Type: application/json" -d '{"query": "a person walking on the beach at sunset"}'
```
---

## API Endpoints

- `POST /db/initialize`: Create a new user session.
- `POST /images/add`: Add a single image.
- `POST /images/add-folder`: Add all images from a folder.
- `POST /images/search`: Search for an image with a text query.

See `/docs` for detailed request/response models.

