# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = release_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, Callable, cast
from uuid import UUID
from datetime import datetime
import dateutil.parser

T = TypeVar("T")


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_stringified_bool(x: str) -> bool:
    if x == "true":
        return True
    if x == "false":
        return False
    assert False


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except Exception as e:
            # print(e)
            pass
    assert False


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class CoverArtArchive:
    artwork: Optional[bool] = None
    count: Optional[int] = None
    front: Optional[bool] = None
    back: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CoverArtArchive':
        assert isinstance(obj, dict)
        artwork = from_union([from_none, lambda x: from_stringified_bool(from_str(x))], obj.get("artwork"))
        count = from_union([from_none, lambda x: int(from_str(x))], obj.get("count"))
        front = from_union([from_none, lambda x: from_stringified_bool(from_str(x))], obj.get("front"))
        back = from_union([from_none, lambda x: from_stringified_bool(from_str(x))], obj.get("back"))
        return CoverArtArchive(artwork, count, front, back)

    def to_dict(self) -> dict:
        result: dict = {}
        result["artwork"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str(
            (lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))], self.artwork)
        result["count"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                      lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                     self.count)
        result["front"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                      lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))],
                                     self.front)
        result["back"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                     lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))],
                                    self.back)
        return result


@dataclass
class Label:
    label_code: Optional[int] = None
    id: Optional[UUID] = None
    type: Optional[str] = None
    name: Optional[str] = None
    sort_name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Label':
        assert isinstance(obj, dict)
        label_code = from_union([from_none, lambda x: int(from_str(x))], obj.get("label-code"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        type = from_union([from_str, from_none], obj.get("type"))
        name = from_union([from_str, from_none], obj.get("name"))
        sort_name = from_union([from_str, from_none], obj.get("sort-name"))
        return Label(label_code, id, type, name, sort_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["label-code"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                           lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                          self.label_code)
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        result["type"] = from_union([from_str, from_none], self.type)
        result["name"] = from_union([from_str, from_none], self.name)
        result["sort-name"] = from_union([from_str, from_none], self.sort_name)
        return result


@dataclass
class LabelInfoList:
    catalog_number: Optional[Any] = None
    label: Optional[Label] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LabelInfoList':
        assert isinstance(obj, dict)
        catalog_number = obj.get("catalog-number")
        label = from_union([Label.from_dict, from_none], obj.get("label"))
        return LabelInfoList(catalog_number, label)

    def to_dict(self) -> dict:
        result: dict = {}
        result["catalog-number"] = self.catalog_number
        result["label"] = from_union([lambda x: to_class(Label, x), from_none], self.label)
        return result


@dataclass
class DiscList:
    sectors: Optional[int] = None
    id: Optional[str] = None
    offset_list: Optional[List[int]] = None
    offset_count: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DiscList':
        assert isinstance(obj, dict)
        sectors = from_union([from_none, lambda x: int(from_str(x))], obj.get("sectors"))
        id = from_union([from_str, from_none], obj.get("id"))
        offset_list = from_union([lambda x: from_list(from_int, x), from_none], obj.get("offset-list"))
        offset_count = from_union([from_int, from_none], obj.get("offset-count"))
        return DiscList(sectors, id, offset_list, offset_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["sectors"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                        lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                       self.sectors)
        result["id"] = from_union([from_str, from_none], self.id)
        result["offset-list"] = from_union([lambda x: from_list(from_int, x), from_none], self.offset_list)
        result["offset-count"] = from_union([from_int, from_none], self.offset_count)
        return result


@dataclass
class Recording:
    length: Optional[int] = None
    id: Optional[UUID] = None
    title: Optional[str] = None
    disambiguation: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Recording':
        assert isinstance(obj, dict)
        length = from_union([from_none, lambda x: int(from_str(x))], obj.get("length"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        title = from_union([from_str, from_none], obj.get("title"))
        disambiguation = from_union([from_str, from_none], obj.get("disambiguation"))
        return Recording(length, id, title, disambiguation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["length"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                       lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                      self.length)
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        result["title"] = from_union([from_str, from_none], self.title)
        result["disambiguation"] = from_union([from_str, from_none], self.disambiguation)
        return result


@dataclass
class TrackList:
    position: Optional[int] = None
    number: Optional[int] = None
    length: Optional[int] = None
    track_or_recording_length: Optional[int] = None
    id: Optional[UUID] = None
    recording: Optional[Recording] = None
    title: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TrackList':
        assert isinstance(obj, dict)
        position = from_union([from_none, lambda x: int(from_str(x))], obj.get("position"))
        number = from_union([from_none, lambda x: int(from_str(x))], obj.get("number"))
        length = from_union([from_none, lambda x: int(from_str(x))], obj.get("length"))
        track_or_recording_length = from_union([from_none, lambda x: int(from_str(x))],
                                               obj.get("track_or_recording_length"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        recording = from_union([Recording.from_dict, from_none], obj.get("recording"))
        title = from_union([from_str, from_none], obj.get("title"))
        return TrackList(position, number, length, track_or_recording_length, id, recording, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["position"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                         lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                        self.position)
        result["number"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                       lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                      self.number)
        result["length"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                       lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                      self.length)
        result["track_or_recording_length"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                                          lambda x: from_str(
                                                              (lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                                         self.track_or_recording_length)
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        result["recording"] = from_union([lambda x: to_class(Recording, x), from_none], self.recording)
        result["title"] = from_union([from_str, from_none], self.title)
        return result


@dataclass
class MediumList:
    position: Optional[int] = None
    format: Optional[str] = None
    disc_list: Optional[List[DiscList]] = None
    disc_count: Optional[int] = None
    track_list: Optional[List[TrackList]] = None
    track_count: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MediumList':
        assert isinstance(obj, dict)
        position = from_union([from_none, lambda x: int(from_str(x))], obj.get("position"))
        format = from_union([from_str, from_none], obj.get("format"))
        disc_list = from_union([lambda x: from_list(DiscList.from_dict, x), from_none], obj.get("disc-list"))
        disc_count = from_union([from_int, from_none], obj.get("disc-count"))
        track_list = from_union([lambda x: from_list(TrackList.from_dict, x), from_none], obj.get("track-list"))
        track_count = from_union([from_int, from_none], obj.get("track-count"))
        return MediumList(position, format, disc_list, disc_count, track_list, track_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["position"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                         lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                        self.position)
        result["format"] = from_union([from_str, from_none], self.format)
        result["disc-list"] = from_union([lambda x: from_list(lambda x: to_class(DiscList, x), x), from_none],
                                         self.disc_list)
        result["disc-count"] = from_union([from_int, from_none], self.disc_count)
        result["track-list"] = from_union([lambda x: from_list(lambda x: to_class(TrackList, x), x), from_none],
                                          self.track_list)
        result["track-count"] = from_union([from_int, from_none], self.track_count)
        return result


@dataclass
class Area:
    id: Optional[UUID] = None
    name: Optional[str] = None
    sort_name: Optional[str] = None
    iso_31661_code_list: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Area':
        assert isinstance(obj, dict)
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        sort_name = from_union([from_str, from_none], obj.get("sort-name"))
        iso_31661_code_list = from_union([lambda x: from_list(from_str, x), from_none], obj.get("iso-3166-1-code-list"))
        return Area(id, name, sort_name, iso_31661_code_list)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        result["name"] = from_union([from_str, from_none], self.name)
        result["sort-name"] = from_union([from_str, from_none], self.sort_name)
        result["iso-3166-1-code-list"] = from_union([lambda x: from_list(from_str, x), from_none],
                                                    self.iso_31661_code_list)
        return result


@dataclass
class ReleaseEventList:
    date: Optional[datetime] = None
    area: Optional[Area] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ReleaseEventList':
        assert isinstance(obj, dict)
        date = from_union([from_datetime, from_none], obj.get("date"))
        area = from_union([Area.from_dict, from_none], obj.get("area"))
        return ReleaseEventList(date, area)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = from_union([lambda x: x.isoformat(), from_none], self.date)
        result["area"] = from_union([lambda x: to_class(Area, x), from_none], self.area)
        return result


@dataclass
class ReleaseGroup:
    id: Optional[UUID] = None
    type: Optional[str] = None
    title: Optional[str] = None
    first_release_date: Optional[datetime] = None
    primary_type: Optional[str] = None
    secondary_type_list: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ReleaseGroup':
        assert isinstance(obj, dict)
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        type = from_union([from_str, from_none], obj.get("type"))
        title = from_union([from_str, from_none], obj.get("title"))
        first_release_date = from_union([from_datetime, from_none], obj.get("first-release-date"))
        primary_type = from_union([from_str, from_none], obj.get("primary-type"))
        secondary_type_list = from_union([lambda x: from_list(from_str, x), from_none], obj.get("secondary-type-list"))
        return ReleaseGroup(id, type, title, first_release_date, primary_type, secondary_type_list)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        result["type"] = from_union([from_str, from_none], self.type)
        result["title"] = from_union([from_str, from_none], self.title)
        result["first-release-date"] = from_union([lambda x: x.isoformat(), from_none], self.first_release_date)
        result["primary-type"] = from_union([from_str, from_none], self.primary_type)
        result["secondary-type-list"] = from_union([lambda x: from_list(from_str, x), from_none],
                                                   self.secondary_type_list)
        return result


@dataclass
class TextRepresentation:
    language: Optional[str] = None
    script: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TextRepresentation':
        assert isinstance(obj, dict)
        language = from_union([from_str, from_none], obj.get("language"))
        script = from_union([from_str, from_none], obj.get("script"))
        return TextRepresentation(language, script)

    def to_dict(self) -> dict:
        result: dict = {}
        result["language"] = from_union([from_str, from_none], self.language)
        result["script"] = from_union([from_str, from_none], self.script)
        return result


@dataclass
class Release:
    id: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    quality: Optional[str] = None
    packaging: Optional[str] = None
    text_representation: Optional[TextRepresentation] = None
    release_group: Optional[ReleaseGroup] = None
    date: Optional[datetime] = None
    country: Optional[str] = None
    release_event_list: Optional[List[ReleaseEventList]] = None
    release_event_count: Optional[int] = None
    barcode: Optional[str] = None
    asin: Optional[str] = None
    cover_art_archive: Optional[CoverArtArchive] = None
    label_info_list: Optional[List[LabelInfoList]] = None
    label_info_count: Optional[int] = None
    medium_list: Optional[List[MediumList]] = None
    medium_count: Optional[int] = None
    sub_cover_art: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Release':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        title = from_union([from_str, from_none], obj.get("title"))
        status = from_union([from_str, from_none], obj.get("status"))
        quality = from_union([from_str, from_none], obj.get("quality"))
        packaging = from_union([from_str, from_none], obj.get("packaging"))
        text_representation = from_union([TextRepresentation.from_dict, from_none], obj.get("text-representation"))
        release_group = from_union([ReleaseGroup.from_dict, from_none], obj.get("release-group"))
        date = from_union([from_datetime, from_none], obj.get("date"))
        country = from_union([from_str, from_none], obj.get("country"))
        release_event_list = from_union([lambda x: from_list(ReleaseEventList.from_dict, x), from_none],
                                        obj.get("release-event-list"))
        release_event_count = from_union([from_int, from_none], obj.get("release-event-count"))
        barcode = from_union([from_str, from_none], obj.get("barcode"))
        asin = from_union([from_str, from_none], obj.get("asin"))
        cover_art_archive = from_union([CoverArtArchive.from_dict, from_none], obj.get("cover-art-archive"))
        label_info_list = from_union([lambda x: from_list(LabelInfoList.from_dict, x), from_none],
                                     obj.get("label-info-list"))
        label_info_count = from_union([from_int, from_none], obj.get("label-info-count"))
        medium_list = from_union([lambda x: from_list(MediumList.from_dict, x), from_none], obj.get("medium-list"))
        medium_count = from_union([from_int, from_none], obj.get("medium-count"))
        return Release(id, title, status, quality, packaging, text_representation, release_group, date, country,
                       release_event_list, release_event_count, barcode, asin, cover_art_archive, label_info_list,
                       label_info_count, medium_list,
                       medium_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_str, from_none], self.id)
        result["title"] = from_union([from_str, from_none], self.title)
        result["status"] = from_union([from_str, from_none], self.status)
        result["quality"] = from_union([from_str, from_none], self.quality)
        result["packaging"] = from_union([from_str, from_none], self.packaging)
        result["text-representation"] = from_union([lambda x: to_class(TextRepresentation, x), from_none],
                                                   self.text_representation)
        result["release-group"] = from_union([lambda x: to_class(ReleaseGroup, x), from_none], self.release_group)
        result["date"] = from_union([lambda x: x.isoformat(), from_none], self.date)
        result["country"] = from_union([from_str, from_none], self.country)
        result["release-event-list"] = from_union(
            [lambda x: from_list(lambda x: to_class(ReleaseEventList, x), x), from_none], self.release_event_list)
        result["release-event-count"] = from_union([from_int, from_none], self.release_event_count)
        result["barcode"] = from_union([from_str, from_none], self.barcode)
        result["asin"] = from_union([from_str, from_none], self.asin)
        result["cover-art-archive"] = from_union([lambda x: to_class(CoverArtArchive, x), from_none],
                                                 self.cover_art_archive)
        result["label-info-list"] = from_union(
            [lambda x: from_list(lambda x: to_class(LabelInfoList, x), x), from_none], self.label_info_list)
        result["label-info-count"] = from_union([from_int, from_none], self.label_info_count)
        result["medium-list"] = from_union([lambda x: from_list(lambda x: to_class(MediumList, x), x), from_none],
                                           self.medium_list)
        result["medium-count"] = from_union([from_int, from_none], self.medium_count)
        return result


def release_from_dict(s: Any) -> Release:
    try:
        return Release.from_dict(s)
    except Exception as e:
        # print(e.with_traceback(e.__traceback__))
        raise e


def release_to_dict(x: Release) -> Any:
    return to_class(Release, x)
