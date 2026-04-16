from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import io

from services.processing import process_dataframe

app = FastAPI()


@app.get("/")
def root():
    return {"status": "API running on Vercel"}


@app.post("/process-csv")
async def process_csv(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="File harus CSV")

    df = pd.read_csv(file.file)

    if 'custom.235.hex' not in df.columns:
        raise HTTPException(status_code=400, detail="Kolom tidak ada")

    df = process_dataframe(df)

    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=hasil.xlsx"
        }
    )
