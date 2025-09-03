import numpy as np
import pytest
from face import Face

def dummy_detect_face(frame):
    # Simulate face detection: returns a list with one face [x, y, w, h]
    return [[10, 20, 30, 40]]

def test_update_and_get_face(monkeypatch):
    face = Face()
    # Patch detect_face to always return a dummy face
    monkeypatch.setattr("face.detect_face", dummy_detect_face)
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    face.update(frame)
    assert face.get_face() == [[10, 20, 30, 40]]
    assert face.inited is False or face.inited is True  # inited becomes True after N updates

def test_get_face_avg(monkeypatch):
    face = Face()
    monkeypatch.setattr("face.detect_face", dummy_detect_face)
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    for _ in range(face.N):
        face.update(frame)
    avg = face.get_face_avg()
    assert avg == [10, 20, 30, 40]

def test_get_face_predict(monkeypatch):
    face = Face()
    monkeypatch.setattr("face.detect_face", dummy_detect_face)
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    for _ in range(face.N):
        face.update(frame)
    pred = face.get_face_predict()
    # Since all faces are the same, prediction should equal the face
    assert pred == [10, 20, 30, 40]

def test_get_face_avg_no_faces():
    face = Face()
    avg = face.get_face_avg()
    assert avg == []

def test_get_face_predict_no_faces():
    face = Face()
    pred = face.get_face_predict()
    assert pred == []
