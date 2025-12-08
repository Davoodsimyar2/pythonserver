from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import os
import threading

app = FastAPI(title="ScreenView Optimized Server")

UPLOAD_PATH = "latest.jpg"
event_list = []
event_lock = threading.Lock()

# نسخه تصویر (هر بار آپلود جدید → +1)
image_version = 0
version_lock = threading.Lock()


# -------------------------------
# صفحه اصلی
# -------------------------------
@app.get("/", response_class=HTMLResponse)
async def index():
    with event_lock:
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
# API جدید: نسخه تصویر
# -------------------------------
@app.get("/latest_version")
async def get_version():
    global image_version
    return {"version": image_version}


# -------------------------------
# آپلود تصویر
# -------------------------------
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    global image_version

    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="فایل باید jpg یا png باشد")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="فایل خالی است")

    with open(UPLOAD_PATH, "wb") as f:
        f.write(content)

    # افزایش نسخه تصویر
    with version_lock:
        image_version += 1

    print(f"✔ تصویر جدید آپلود شد. نسخه تصویر: {image_version}")

    return {"status": "ok", "version": image_version, "size": len(content)}


# -------------------------------
# دریافت آخرین تصویر
# -------------------------------
@app.get("/latest")
async def get_latest():
    if not os.path.exists(UPLOAD_PATH):
        raise HTTPException(status_code=404, detail="No image uploaded yet.")
    return FileResponse(UPLOAD_PATH)


# -------------------------------
# ثبت ایونت
# -------------------------------
@app.post("/event")
async def post_event(event: dict):
    with event_lock:
        event_list.append(event)
    print(f"✔ ایونت دریافت شد: {event}")
    return {"status": "ok"}


# -------------------------------
# دریافت و پاک کردن ایونت‌ها
# -------------------------------
@app.get("/event")
async def get_events():
    with event_lock:
        current = event_list.copy()
        event_list.clear()
    return current


# -------------------------------
# اجرای سرور
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
