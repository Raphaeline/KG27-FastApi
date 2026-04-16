from services.processing import process_dataframe
import io
import pandas as pd
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, UploadFile, File, HTTPException
from datetime import datetime
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = FastAPI(
    title="KG27 Hex Parser API",
    description="Upload CSV → Parse → Download XLSX",
    version="1.1.0"
)


@app.post("/parser", tags=["Processing"])
async def process_csv(file: UploadFile = File(...)):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    filename = f"result_{timestamp}.xlsx"

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
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
