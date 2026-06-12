"""Client interface for the interactive driver boundary."""
from __future__ import annotations

from typing import Any, Protocol


class DriverClient(Protocol):
    """Client-side interface used by tool frontends.

    The client owns both command delivery and driver artifact access. Tool
    implementations should not know whether those operations use workdir files,
    sockets, or another driver-side protocol.
    """

    def send_command(
        self,
        command: dict,
        *,
        current_step: int | None = None,
        timeout_s: float = 600.0,
    ) -> dict:
        """Send one command to the driver and wait for the resulting step."""

    def load_states(self) -> list:
        """Return the parsed driver state trace."""

    def latest_step(self) -> int | None:
        """Return the latest recorded driver step, if any."""

    def load_step(self, step: int | None = None) -> dict:
        """Return one state trace entry, defaulting to the latest step."""

    def load_image(self, step: int, kind: str = "agent") -> bytes | None:
        """Return PNG bytes for one step.

        ``kind`` is ``"agent"`` for images/image_NN.png or ``"camera"`` for
        images_cam/image_cam_NN.png.
        """

    def load_camera_meta(self) -> dict[str, Any]:
        """Return camera calibration metadata."""

    def load_depth(self, step: int) -> Any:
        """Return the depth array for a step."""

    def close(self) -> None:
        """Release any client-side transport resources."""
