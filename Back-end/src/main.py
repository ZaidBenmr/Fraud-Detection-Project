import os
from fastapi import FastAPI
from fastapi.responses import FileResponse,StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from model.model import predict_one, predict_all
from bdd import *

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/predict")
def makepred(index : str):
    df = import_data_one(index)
    prediction = predict_one(df)
    return {"fraud": int(prediction)}

@app.get("/predict_all")
def makepred2():
    prediction = predict_all()
    return {"Etat": prediction}

@app.get("/cards")
def cards_data():
    result = cards()
    return result

@app.get("/frauddetectdconfrmed")
def fraud_detectd_confrmed_data():
    result = fraud_detectd_confrmed()
    return result

@app.get("/fraudparregion")
def fraud_par_region_data():
    result = fraud_par_region()
    return result

@app.get("/frauddetectdconfrmedencour")
def fraud_conf_det_encour_data():
    result = fraud_conf_det_encour()
    return result

@app.get("/fraudbillingcat")
def fraud_billing_cat_data():
    result = fraud_billing_cat()
    return result

@app.get("/fraudsubstatus")
def fraud_sub_status_data():
    result = fraud_sub_status()
    return result

@app.get("/fraudlastdateparregion")
def fraud_detectd_lastdate_par_region_data():
    result = fraud_detectd_lastdate_par_region()
    return result

## Sending Data as Excel Files
@app.get("/fraudanalysedates")
def fraud_analyse_dates_data():
    result = fraud_analyse_dates()
    return result

@app.get("/downloadcsv")
def download(date : str) :
    # Path to the CSV file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #xlsx_file_path = os.path.join(BASE_DIR, 'src\\NEW_FRAUD_LIST_01-05-2023.xlsx')
    xlsx_file  = fraud_data_by_date(date)
    headers = {
        'Content-Disposition': 'attachment; filename="data.xlsx"'
    }

    # Return the CSV file as a streaming response
    #return FileResponse(xlsx_file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
    return StreamingResponse(
        iter([xlsx_file.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )