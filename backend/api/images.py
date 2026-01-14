from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from ..models.schemas import ImageRequest, FolderRequest, ImageSearch
from ..services.database_service import ImageDBManager
from ..services.search_service import ImageSearcher

router = APIRouter(prefix="/images", tags=["images"])

@router.post("/add")
async def add_image(request: ImageRequest, user_id: str = Query(...)):
    try:
        db_manager = ImageDBManager(user_id)
        return db_manager.add_image(request.image_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-folder")
async def add_images_from_folder(request: FolderRequest, user_id: str = Query(...)):
    try:
        db_manager = ImageDBManager(user_id)
        return db_manager.add_images_from_folder(request.folder_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def search_image(request: ImageSearch, user_id: str = Query(...)):
    try:
        image_searcher = ImageSearcher(user_id)
        result = image_searcher.search_image(request.query)
        return JSONResponse(content={
            "image_path": result,
            "query": request.query
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))