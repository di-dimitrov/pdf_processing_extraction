from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
import json
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

# Load the JSON data
DATA_FILE = "data.json"
STATIC_DIR = "dataset"

# Ensure static directory exists
Path(STATIC_DIR).mkdir(exist_ok=True)

# Load JSON
#try:
#    with open(DATA_FILE, "r", encoding="utf-8") as f:
#        data = json.load(f)
#except FileNotFoundError:
#    data = []

templates = Jinja2Templates(directory="templates")
app.mount("/dataset", StaticFiles(directory=STATIC_DIR), name="dataset_images")

data = []
DATA_FILE = None

@app.post("/set_file")
async def set_data_file(data_file: str = Form(...)):
    global DATA_FILE, data
    DATA_FILE = data_file
    return RedirectResponse(url="/", status_code=303)

@app.get("/", response_class=HTMLResponse)
async def start_page(request: Request):
    img_url = None
    item = None
    global data
    if DATA_FILE:
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
           raise HTTPException(status_code=404, detail="File not found")
        if data:
            item = next((entry for entry in data if entry["answer_key"] == ""), None)
            if item:
                img_url = f"{item['img_path']}"
    return templates.TemplateResponse("index.html", {"request": request, "item": item, "img_url": img_url})


@app.post("/submit")
async def submit_answer(id: str = Form(...), answer: str = Form(...), chemical_structure: bool = Form(False), tablee: bool = Form(False),
                       figuree: bool = Form(False), graph: bool = Form(False)):
    for item in data:
        if item["id"] == id:
            item["chemical_structure"] = chemical_structure*1
            item["table"] = tablee*1
            item["figure"] = figuree*1
            item["graph"] = graph*1
            item["answer_key"] = answer
            #print(item)
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, separators=(',', ': '), ensure_ascii=False)
            return RedirectResponse(url="/", status_code=303)
    raise HTTPException(status_code=404, detail="Item not found")