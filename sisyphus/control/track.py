from typing import Any, Dict


class Track:
    """Represents a track in the context of a Playlist or Table.

Every track known to a table is represented by a Track object whose parent
is the appropriate Table object.

Every track in a playlist is represented by a Track object whose parent is the
Playlist. If a given track appears multiple times in the playlist, each
occurrence is represented by its own Track object."""
    def __init__(self, parent, transport, data: Dict[str, Any]):
        self.parent = parent
        self._transport = transport
        self._data = data

    def __str__(self) -> str:
        return self.name

    @property
    def id(self):
        """UUID of the track design, not of the Track instance."""
        return self._data["id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def is_in_playlist(self) -> bool:
        return "_index" in self._data

    @property
    def index_in_playlist(self) -> int:
        """
This track's index in the owning playlist when the playlist is not shuffled"""
        return self._data["_index"]

    async def play(self):
        if not self.is_in_playlist:
            await self._transport.post("set_track", self._data)
            await self.parent.play()
        else:
            await self.parent.play(self)
