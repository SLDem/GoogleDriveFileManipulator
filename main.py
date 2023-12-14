from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from fastapi import FastAPI, Form, Request
from fastapi.security import OAuth2PasswordBearer

import credential_handler
import drive

app = FastAPI()
templates = Jinja2Templates(directory="templates")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
credential_handler.get_creds()


folder_1_id = "1ha3wKJKEyZVWv1o6qhhWCzYdUj-5krUt"
folder_2_id = "1V4PRKhXkhpUvL4Hae2ES7wBvM0TgaRMM"
file_id = "1RWGTSrK0MQGdI8TydxJVngYd_BX0sma1"


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    """
    Displays a home page with available views.
    """
    return templates.TemplateResponse('home.html', {'request': request})


@app.get("/search-files")
async def search_files():
    """
    Displays all user files and folders.
    """
    return drive.search_files()


@app.get('/edit-file', response_class=HTMLResponse)
async def edit_file(request: Request):
    """
    Renders a form with one field - file id, user must enter a file id and a new content will be uploaded to this file.
    """
    return templates.TemplateResponse('edit_file.html', {'request': request})


@app.post('/edit-file')
async def edit_file(request: Request, object_id: str = Form(...)):
    """
    Edits the file and shows a success page.
    """
    drive.edit_file(object_id)
    return templates.TemplateResponse('success.html', {'request': request})


@app.get('/delete-object', response_class=HTMLResponse)
async def delete_object(request: Request):
    """
    Renders a form with one field - object id, user must enter an object id to delete.
    """
    return templates.TemplateResponse('delete_object.html', {'request': request})


@app.post('/delete-object')
async def delete_object(request: Request, object_id: str = Form(...)):
    """
    Trashes the file and shows a success page.
    """
    drive.delete_object(object_id)
    return templates.TemplateResponse('success.html', {'request': request})


@app.get('/move-file', response_class=HTMLResponse)
async def move_file(request: Request):
    """
    Renders a form with two fields: file_id and folder_id,
    user must enter an id of a file to move and an id of a folder to move it to.
    """
    return templates.TemplateResponse('move_file.html', {'request': request})


@app.post('/move-file')
async def move_file(request: Request, folder_id: str = Form(...), file_id: str = Form(...)):
    """
    Moves the file and shows a success page.
    """
    drive.move_file(file_id, folder_id)
    return templates.TemplateResponse('success.html', {'request': request})


@app.get('/upload-file', response_class=HTMLResponse)
async def upload_file_to_folder(request: Request):
    """
    Renders the form with one field: folder id, user must enter the form id and the file 'test_file.txt'
    will be uploaded to it.
    """
    return templates.TemplateResponse('upload_file.html', {'request': request})


@app.post('/upload-file')
async def upload_file_to_folder(request: Request, folder_id: str = Form(...), file_name: str = Form(...)):
    """
    Uploads the file and shows a success page.
    """
    drive.upload_file_to_folder(file_name, folder_id)
    return templates.TemplateResponse('success.html', {'request': request})


@app.get('/create-folder', response_class=HTMLResponse)
async def create_folder(request: Request):
    """
    Renders a form with 1 field: folder name, user must enter the folder name and it will be created in g-drive.
    """
    return templates.TemplateResponse('create_folder.html', {'request': request})


@app.post('/create-folder')
async def create_folder(request: Request, name: str = Form(...)):
    """
    Creates the folder and shows a success page.
    """
    drive.create_folder(name)
    return templates.TemplateResponse('success.html', {'request': request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
