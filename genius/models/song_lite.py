# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = genius_song_lite_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class PrimaryArtist:
    api_path: Optional[str] = None
    header_image_url: Optional[str] = None
    id: Optional[int] = None
    image_url: Optional[str] = None
    is_meme_verified: Optional[bool] = None
    is_verified: Optional[bool] = None
    name: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PrimaryArtist':
        assert isinstance(obj, dict)
        api_path = from_union([from_str, from_none], obj.get("api_path"))
        header_image_url = from_union([from_str, from_none], obj.get("header_image_url"))
        id = from_union([from_int, from_none], obj.get("id"))
        image_url = from_union([from_str, from_none], obj.get("image_url"))
        is_meme_verified = from_union([from_bool, from_none], obj.get("is_meme_verified"))
        is_verified = from_union([from_bool, from_none], obj.get("is_verified"))
        name = from_union([from_str, from_none], obj.get("name"))
        url = from_union([from_str, from_none], obj.get("url"))
        return PrimaryArtist(api_path, header_image_url, id, image_url, is_meme_verified, is_verified, name, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["api_path"] = from_union([from_str, from_none], self.api_path)
        result["header_image_url"] = from_union([from_str, from_none], self.header_image_url)
        result["id"] = from_union([from_int, from_none], self.id)
        result["image_url"] = from_union([from_str, from_none], self.image_url)
        result["is_meme_verified"] = from_union([from_bool, from_none], self.is_meme_verified)
        result["is_verified"] = from_union([from_bool, from_none], self.is_verified)
        result["name"] = from_union([from_str, from_none], self.name)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class Stats:
    unreviewed_annotations: Optional[int] = None
    hot: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Stats':
        assert isinstance(obj, dict)
        unreviewed_annotations = from_union([from_int, from_none], obj.get("unreviewed_annotations"))
        hot = from_union([from_bool, from_none], obj.get("hot"))
        return Stats(unreviewed_annotations, hot)

    def to_dict(self) -> dict:
        result: dict = {}
        result["unreviewed_annotations"] = from_union([from_int, from_none], self.unreviewed_annotations)
        result["hot"] = from_union([from_bool, from_none], self.hot)
        return result


@dataclass
class GeniusSongLite:
    annotation_count: Optional[int] = None
    api_path: Optional[str] = None
    full_title: Optional[str] = None
    header_image_thumbnail_url: Optional[str] = None
    header_image_url: Optional[str] = None
    id: Optional[int] = None
    lyrics_owner_id: Optional[int] = None
    lyrics_state: Optional[str] = None
    path: Optional[str] = None
    pyongs_count: Optional[int] = None
    song_art_image_thumbnail_url: Optional[str] = None
    song_art_image_url: Optional[str] = None
    stats: Optional[Stats] = None
    title: Optional[str] = None
    title_with_featured: Optional[str] = None
    url: Optional[str] = None
    primary_artist: Optional[PrimaryArtist] = None
    lyrics: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GeniusSongLite':
        assert isinstance(obj, dict)
        annotation_count = from_union([from_int, from_none], obj.get("annotation_count"))
        api_path = from_union([from_str, from_none], obj.get("api_path"))
        full_title = from_union([from_str, from_none], obj.get("full_title"))
        header_image_thumbnail_url = from_union([from_str, from_none], obj.get("header_image_thumbnail_url"))
        header_image_url = from_union([from_str, from_none], obj.get("header_image_url"))
        id = from_union([from_int, from_none], obj.get("id"))
        lyrics_owner_id = from_union([from_int, from_none], obj.get("lyrics_owner_id"))
        lyrics_state = from_union([from_str, from_none], obj.get("lyrics_state"))
        path = from_union([from_str, from_none], obj.get("path"))
        pyongs_count = from_union([from_int, from_none], obj.get("pyongs_count"))
        song_art_image_thumbnail_url = from_union([from_str, from_none], obj.get("song_art_image_thumbnail_url"))
        song_art_image_url = from_union([from_str, from_none], obj.get("song_art_image_url"))
        stats = from_union([Stats.from_dict, from_none], obj.get("stats"))
        title = from_union([from_str, from_none], obj.get("title"))
        title_with_featured = from_union([from_str, from_none], obj.get("title_with_featured"))
        url = from_union([from_str, from_none], obj.get("url"))
        primary_artist = from_union([PrimaryArtist.from_dict, from_none], obj.get("primary_artist"))
        lyrics = from_union([from_str, from_none], obj.get("lyrics"))
        return GeniusSongLite(annotation_count, api_path, full_title, header_image_thumbnail_url, header_image_url, id, lyrics_owner_id, lyrics_state, path, pyongs_count, song_art_image_thumbnail_url, song_art_image_url, stats, title, title_with_featured, url, primary_artist, lyrics)

    def to_dict(self) -> dict:
        result: dict = {}
        result["annotation_count"] = from_union([from_int, from_none], self.annotation_count)
        result["api_path"] = from_union([from_str, from_none], self.api_path)
        result["full_title"] = from_union([from_str, from_none], self.full_title)
        result["header_image_thumbnail_url"] = from_union([from_str, from_none], self.header_image_thumbnail_url)
        result["header_image_url"] = from_union([from_str, from_none], self.header_image_url)
        result["id"] = from_union([from_int, from_none], self.id)
        result["lyrics_owner_id"] = from_union([from_int, from_none], self.lyrics_owner_id)
        result["lyrics_state"] = from_union([from_str, from_none], self.lyrics_state)
        result["path"] = from_union([from_str, from_none], self.path)
        result["pyongs_count"] = from_union([from_int, from_none], self.pyongs_count)
        result["song_art_image_thumbnail_url"] = from_union([from_str, from_none], self.song_art_image_thumbnail_url)
        result["song_art_image_url"] = from_union([from_str, from_none], self.song_art_image_url)
        result["stats"] = from_union([lambda x: to_class(Stats, x), from_none], self.stats)
        result["title"] = from_union([from_str, from_none], self.title)
        result["title_with_featured"] = from_union([from_str, from_none], self.title_with_featured)
        result["url"] = from_union([from_str, from_none], self.url)
        result["primary_artist"] = from_union([lambda x: to_class(PrimaryArtist, x), from_none], self.primary_artist)
        result["lyrics"] = from_union([from_str, from_none], self.lyrics)
        return result


def genius_song_lite_from_dict(s: Any) -> GeniusSongLite:
    return GeniusSongLite.from_dict(s)


def genius_song_lite_to_dict(x: GeniusSongLite) -> Any:
    return to_class(GeniusSongLite, x)
