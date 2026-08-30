from __future__ import annotations

from abc import ABC, abstractmethod


class VideoSource(ABC):
    @abstractmethod
    def get_frame(self) -> bytes:
        raise NotImplementedError


class MockVideoSource(VideoSource):
    def __init__(self, frame_provider):
        self._frame_provider = frame_provider

    def get_frame(self) -> bytes:
        return self._frame_provider()


class FileVideoSource(VideoSource):
    """Future-ready file adapter; OpenCV is loaded only when this adapter is used."""

    def __init__(self, path: str):
        try:
            import cv2
        except ImportError as exc:
            raise RuntimeError("OpenCV is required for FileVideoSource") from exc
        self._capture = cv2.VideoCapture(path)

    def get_frame(self) -> bytes:
        ok, frame = self._capture.read()
        if not ok:
            raise EOFError("video source ended")
        return frame

