from services.processing import process_dataframe
import io
import pandas as pd
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, UploadFile, File, HTTPException
import sys
import os

# penting untuk Vercel (fix import path)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


app = FastAPI(
    title="KG27 Hex Parser API",
    description="Upload CSV → Parse → Download XLSX",
    version="1.1.0"
)


# @app.get("/")
# def root():
#     return {"status": "API running on Vercel"}


@app.post("/parser", tags=["Processing"])
async def process_csv(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="File harus CSV")
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Gagal membaca CSV")
    if 'custom.235.hex' not in df.columns:
        raise HTTPException(
            status_code=400, detail="Kolom custom.235.hex tidak ditemukan")

    try:
        df = process_dataframe(df)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Processing error: {str(e)}")
    try:
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
    except Exception:
        raise HTTPException(status_code=500, detail="Gagal convert ke Excel")

    # 6. Return file
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=hasil_parsing.xlsx"
        }
    )
