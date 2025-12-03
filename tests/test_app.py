import os
import io
import tempfile
import pytest
from app.main import app as flask_app

@pytest.fixture
def client():
    flask_app.testing = True
    with flask_app.test_client() as client:
        yield client

def test_get_index(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Текстовый редактор".encode() in rv.data

def test_save_txt(client):
    data = {"editor": "Привет, мир!", "format": "txt"}
    rv = client.post("/", data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert rv.mimetype == "application/octet-stream"
    assert rv.headers["Content-Disposition"].startswith('attachment;')
    assert rv.headers["Content-Disposition"].endswith('output.txt')

def test_save_docx(client):
    data = {"editor": "Документ", "format": "docx"}
    rv = client.post("/", data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert rv.headers["Content-Disposition"].endswith('output.docx')

def test_save_doc(client, monkeypatch):
    # Подменяем вызов libreoffice, чтобы не запускать реальную конвертацию
    def fake_run(cmd, check, stdout, stderr):
        # просто создаём пустой .doc файл
        doc_path = cmd[-1].replace(".docx", ".doc")
        Path(doc_path).write_bytes(b"")
        return None

    monkeypatch.setattr("subprocess.run", fake_run)

    data = {"editor": "Старый документ", "format": "doc"}
    rv = client.post("/", data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert rv.headers["Content-Disposition"].endswith('output.doc')