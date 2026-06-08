import io
import pytest
from PIL import Image
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def make_image_bytes():
    img = Image.new("RGB", (100, 100), color=(128, 64, 32))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_list_filters(client):
    r = client.get("/filters")
    assert r.status_code == 200
    assert "blur" in r.get_json()["filters"]


def test_apply_blur(client):
    data = {"image": (make_image_bytes(), "test.jpg")}
    r = client.post("/apply?filter=blur", data=data, content_type="multipart/form-data")
    assert r.status_code == 200
    assert r.content_type == "image/jpeg"


def test_apply_unknown_filter(client):
    data = {"image": (make_image_bytes(), "test.jpg")}
    r = client.post("/apply?filter=nope", data=data, content_type="multipart/form-data")
    assert r.status_code == 400


def test_apply_no_image(client):
    r = client.post("/apply?filter=blur", data={}, content_type="multipart/form-data")
    assert r.status_code == 400
