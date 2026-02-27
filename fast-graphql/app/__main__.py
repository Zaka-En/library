import uvicorn
#uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
uvicorn.run("app.app:app", host="127.0.0.1", port=8000, workers=3)