from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os

app = FastAPI()

UPLOAD_PATH = "latest.jpg"

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()

    # ذخیره تصویر
    with open(UPLOAD_PATH, "wb") as f:
        f.write(content)

    print("✔ تصویر دریافت شد و ذخیره شد.")
    return {"status": "ok"}

@app.get("/latest")
async def get_latest():
    if not os.path.exists(UPLOAD_PATH):
        return {"error": "No image uploaded yet."}
    return FileResponse(UPLOAD_PATH)


# ----------------------------
# Render uses PORT environment variable
# ----------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
