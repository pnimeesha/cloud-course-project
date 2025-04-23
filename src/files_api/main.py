import os
from datetime import datetime
from typing import (
    List,
    Optional,
)

import pydantic
from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from responses import delete

from files_api.errors import (
    handle_broad_exceptions,
    handle_pydanic_validation_errors,
)
from files_api.routes import ROUTER
from files_api.s3.delete_objects import delete_s3_object
from files_api.s3.read_objects import (
    fetch_s3_object,
    fetch_s3_objects_metadata,
    fetch_s3_objects_using_page_token,
    object_exists_in_s3,
)
from files_api.s3.write_objects import upload_s3_object
from files_api.settings import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a FastAPI app with the given S3 bucket name."""
    # s3_bucket_name = s3_bucket_name or os.getenv("S3_BUCKET_NAME")
    
    settings = settings or Settings()
    
    app = FastAPI()    
    app.state.settings = settings
    
    app.include_router(ROUTER)
    app.add_exception_handler(
        exc_class_or_status_code=pydantic.ValidationError,
        handler=handle_pydanic_validation_errors,
    )
    app.middleware("http")(handle_broad_exceptions)
    
    return app

if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
