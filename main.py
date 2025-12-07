from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import os

app = FastAPI(title="ScreenView Debug Server")

UPLOAD_PATH = "latest.jpg"
event_list = []  # لیست ایونت‌ها

# -------------------------------
# صفحه اصلی
# -------------------------------
@app.get("/", response_class=HTMLResponse)
async def index():
    events_html = "<br>".join([str(e) for e in event_list]) if event_list else "هیچ ایونتی ثبت نشده."
    return f"""
    <html>
        <body>
            <h2>ارسال تصویر تست</h2>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit" value="Upload">
            </form>
            <h2>دریافت آخرین تصویر</h2>
            <a href="/latest" target="_blank">مشاهده آخرین تصویر</a>
            <h2>لیست ایونت‌ها</h2>
            {events_html}
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
# ثبت ایونت (POST)
# -------------------------------
@app.post("/event")
async def post_event(event: dict):
    event_list.append(event)
    print(f"✔ ایونت دریافت شد: {event}")
    return {"status": "ok"}

# -------------------------------
# دریافت ایونت‌ها (GET)
# -------------------------------
@app.get("/event")
async def get_events():
    return event_list

# -------------------------------
# اجرای سرور
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
