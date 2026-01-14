# Smart Gallery: AI-Powered Semantic Image Search

![Smart Gallery Banner](https://user-images.githubusercontent.com/12345/12345678-abcdef.png) <!-- Replace with an actual banner image if available -->

**Smart Gallery is an intelligent, self-hosted image gallery that allows you to search through your photo collection using natural language. Instead of relying on tags or filenames, you can find images based on their content, context, and meaning.**

---

## 📚 Table of Contents
- [✨ Features](#-features)
- [🧠 How It Works: The Technology](#-how-it-works-the-technology)
  - [The Machine Learning Model](#the-machine-learning-model)
  - [Technology Stack](#technology-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
- [💡 Usage](#-usage)
  - [1. Initialize the Database](#1-initialize-the-database)
  - [2. Add Images](#2-add-images)
  - [3. Search for Images](#3-search-for-images)
- [🔌 API Endpoints](#-api-endpoints)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## ✨ Features

- **🖼️ Semantic Search:** Find images using descriptive text queries (e.g., "a happy dog playing in a field").
- **⚡ Fast & Efficient:** Utilizes a high-performance vector database (`ChromaDB`) for near-instant search results.
- **🧠 Custom CLIP Model:** Powered by a custom-trained CLIP (Contrastive Language-Image Pre-Training) model for accurate image-text understanding.
- **📦 Self-Hosted:** Keep your images private. The entire application runs on your local machine or private server.
- **📁 Bulk Ingestion:** Easily add entire folders of images at once.
- **✅ Multi-User Support:** Creates separate, isolated collections for different users.
- **🐳 Dockerized:** (Optional) Includes a Dockerfile for easy containerization and deployment.
- **🔌 RESTful API:** A modern FastAPI backend provides a clean and simple interface for integration.

---

## 🧠 How It Works: The Technology

Smart Gallery combines a powerful machine learning model with a high-performance vector database to create a seamless search experience.

### The Machine Learning Model

The core of the application is a custom implementation of the **CLIP (Contrastive Language-Image Pre-Training)** model architecture. This model is designed to understand both images and text in a shared embedding space.

1.  **Image Encoder:** A **Vision Transformer (ViT)** processes images and converts them into a dense vector representation (an embedding). This vector captures the semantic essence of the image.
2.  **Text Encoder:** A **BERT (Bidirectional Encoder Representations from Transformers)** model processes your text query and converts it into a similar vector representation.
3.  **Shared Embedding Space:** The model is trained to place the vectors of similar images and text descriptions close to each other in this multi-dimensional space. When you search, we are essentially finding the image vectors that are "closest" to your text vector.

The pre-trained model weights (`clip_model_epoch_30.pt`) are included in this repository.

### Technology Stack

- **Backend:** **FastAPI** (Python)
- **ML Framework:** **PyTorch**
- **Transformers:** **Hugging Face Transformers** (for BERT and ViT)
- **Vector Database:** **ChromaDB** (local, persistent storage)
- **Web Server:** **Uvicorn**

---

## 📂 Project Structure

The backend is organized into a clean, layered architecture for better separation of concerns:

```
smart_gallery_backend/
├── models/              # ML Model definitions (CLIP, Encoders)
├── database/            # Database management layer (ChromaDB)
├── services/            # Business logic (Image Search)
├── routes/              # API endpoints (FastAPI routers)
├── main.py              # FastAPI application entry point
└── clip_model_epoch_30.pt # Pre-trained model weights
```
For more details, see the `STRUCTURE.md` file in the `smart_gallery_backend` directory.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- `pip` for package management

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/smart-gallery.git
    cd smart-gallery/smart_gallery_backend
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8080
    ```
    The API will now be live and accessible at `http://localhost:8080`. You can view the interactive documentation at `http://localhost:8080/docs`.

---

## 💡 Usage

Interact with the API using tools like `curl`, Postman, or by building a front-end client.

### 1. Initialize the Database
First, create a unique user session. This will create a dedicated image collection for that user.

```bash
curl -X POST "http://localhost:8080/db/initialize" \
-H "Content-Type: application/json" \
-d '{"user_name": "my_gallery"}'
```
**Response:**
```json
{
  "status": "success",
  "message": "Initialized DB for user my_gallery",
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}
```
**Save the `user_id` for all future requests.**

### 2. Add Images

Add a single image or an entire folder. Use the `user_id` from the previous step.

**Add a single image:**
```bash
curl -X POST "http://localhost:8080/images/add?user_id=YOUR_USER_ID" \
-H "Content-Type: application/json" \
-d '{"image_path": "/path/to/your/image.jpg"}'
```

**Add a folder of images:**
```bash
curl -X POST "http://localhost:8080/images/add-folder?user_id=YOUR_USER_ID" \
-H "Content-Type: application/json" \
-d '{"folder_path": "/path/to/your/pictures_folder"}'
```

### 3. Search for Images

Now, you can search for images using a natural language query.

```bash
curl -X POST "http://localhost:8080/images/search?user_id=YOUR_USER_ID" \
-H "Content-Type: application/json" \
-d '{"query": "a person walking on the beach at sunset"}'
```
**Response:**
```json
{
  "image_path": {
    "image_path": "/path/to/your/pictures_folder/sunset_beach.jpg"
  },
  "query": "a person walking on the beach at sunset"
}
```

---

## 🔌 API Endpoints

- `POST /db/initialize`: Creates a new user session and database collection.
- `POST /images/add`: Adds a single image to the user's collection.
- `POST /images/add-folder`: Adds all images from a specified folder.
- `POST /images/search`: Searches for an image based on a text query.

For detailed request/response models, please see the auto-generated docs at `/docs`.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for bugs, feature requests, or improvements.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
