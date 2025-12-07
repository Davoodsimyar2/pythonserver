from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import os

app = FastAPI(title="ScreenView Debug Server")

UPLOAD_PATH = "latest.jpg"

# -------------------------------
# صفحه اصلی برای تست از مرورگر
# -------------------------------
@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <body>
            <h2>ارسال تصویر تست</h2>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit" value="Upload">
            </form>
            <h2>دریافت آخرین تصویر</h2>
            <a href="/latest" target="_blank">مشاهده آخرین تصویر</a>
        </body>
    </html>
    """

# -------------------------------
# آپلود تصویر
# -------------------------------
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="فایل باید jpg یا png باشد")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="فایل خالی است")

    with open(UPLOAD_PATH, "wb") as f:
        f.write(content)

    print(f"✔ تصویر دریافت شد: {file.filename}, سایز: {len(content)} بایت")
    return {"status": "ok", "filename": file.filename, "size": len(content)}

# -------------------------------
# دریافت آخرین تصویر
# -------------------------------
@app.get("/latest")
async def get_latest():
    if not os.path.exists(UPLOAD_PATH):
        raise HTTPException(status_code=404, detail="No image uploaded yet.")
    return FileResponse(UPLOAD_PATH)

# -------------------------------
# اجرای سرور (Render-ready)
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
