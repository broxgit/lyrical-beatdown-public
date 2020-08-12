# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = artist_results_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable


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
        except:
            pass
    assert False


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


@dataclass
class AreaLifeSpan:
    ended: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AreaLifeSpan':
        assert isinstance(obj, dict)
        ended = from_union([from_none, lambda x: from_stringified_bool(from_str(x))], obj.get("ended"))
        return AreaLifeSpan(ended)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ended"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))], self.ended)
        return result


@dataclass
class Area:
    id: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
    sort_name: Optional[str] = None
    life_span: Optional[AreaLifeSpan] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Area':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        type = from_union([from_str, from_none], obj.get("type"))
        name = from_union([from_str, from_none], obj.get("name"))
        sort_name = from_union([from_str, from_none], obj.get("sort-name"))
        life_span = from_union([AreaLifeSpan.from_dict, from_none], obj.get("life-span"))
        return Area(id, type, name, sort_name, life_span)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_str, from_none], self.id)
        result["type"] = from_union([from_str, from_none], self.type)
        result["name"] = from_union([from_str, from_none], self.name)
        result["sort-name"] = from_union([from_str, from_none], self.sort_name)
        result["life-span"] = from_union([lambda x: to_class(AreaLifeSpan, x), from_none], self.life_span)
        return result


@dataclass
class ArtistListLifeSpan:
    ended: Optional[bool] = None
    begin: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ArtistListLifeSpan':
        assert isinstance(obj, dict)
        ended = from_union([from_none, lambda x: from_stringified_bool(from_str(x))], obj.get("ended"))
        begin = from_union([from_str, from_none], obj.get("begin"))
        return ArtistListLifeSpan(ended, begin)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ended"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))], self.ended)
        result["begin"] = from_union([from_str, from_none], self.begin)
        return result


@dataclass
class TagList:
    count: Optional[str] = None
    name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TagList':
        assert isinstance(obj, dict)
        count = from_union([from_str, from_none], obj.get("count"))
        name = from_union([from_str, from_none], obj.get("name"))
        return TagList(count, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_union([from_str, from_none], self.count)
        result["name"] = from_union([from_str, from_none], self.name)
        return result


@dataclass
class ArtistResult:
    id: Optional[str] = None
    type: Optional[str] = None
    ext_score: Optional[str] = None
    name: Optional[str] = None
    sort_name: Optional[str] = None
    country: Optional[str] = None
    area: Optional[Area] = None
    begin_area: Optional[Area] = None
    disambiguation: Optional[str] = None
    life_span: Optional[ArtistListLifeSpan] = None
    tag_list: Optional[List[TagList]] = None
    gender: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ArtistResult':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        type = from_union([from_str, from_none], obj.get("type"))
        ext_score = from_union([from_str, from_none], obj.get("ext:score"))
        name = from_union([from_str, from_none], obj.get("name"))
        sort_name = from_union([from_str, from_none], obj.get("sort-name"))
        country = from_union([from_str, from_none], obj.get("country"))
        area = from_union([Area.from_dict, from_none], obj.get("area"))
        begin_area = from_union([Area.from_dict, from_none], obj.get("begin-area"))
        disambiguation = from_union([from_str, from_none], obj.get("disambiguation"))
        life_span = from_union([ArtistListLifeSpan.from_dict, from_none], obj.get("life-span"))
        tag_list = from_union([lambda x: from_list(TagList.from_dict, x), from_none], obj.get("tag-list"))
        gender = from_union([from_str, from_none], obj.get("gender"))
        return ArtistResult(id, type, ext_score, name, sort_name, country, area, begin_area, disambiguation, life_span, tag_list, gender)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_str, from_none], self.id)
        result["type"] = from_union([from_str, from_none], self.type)
        result["ext:score"] = from_union([from_str, from_none], self.ext_score)
        result["name"] = from_union([from_str, from_none], self.name)
        result["sort-name"] = from_union([from_str, from_none], self.sort_name)
        result["country"] = from_union([from_str, from_none], self.country)
        result["area"] = from_union([lambda x: to_class(Area, x), from_none], self.area)
        result["begin-area"] = from_union([lambda x: to_class(Area, x), from_none], self.begin_area)
        result["disambiguation"] = from_union([from_str, from_none], self.disambiguation)
        result["life-span"] = from_union([lambda x: to_class(ArtistListLifeSpan, x), from_none], self.life_span)
        result["tag-list"] = from_union([lambda x: from_list(lambda x: to_class(TagList, x), x), from_none], self.tag_list)
        result["gender"] = from_union([from_str, from_none], self.gender)
        return result


@dataclass
class ArtistResults:
    artist_list: Optional[List[ArtistResult]] = None
    artist_count: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ArtistResults':
        assert isinstance(obj, dict)
        artist_list = from_union([lambda x: from_list(ArtistResult.from_dict, x), from_none], obj.get("artist-list"))
        artist_count = from_union([from_int, from_none], obj.get("artist-count"))
        return ArtistResults(artist_list, artist_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["artist-list"] = from_union([lambda x: from_list(lambda x: to_class(ArtistResult, x), x), from_none], self.artist_list)
        result["artist-count"] = from_union([from_int, from_none], self.artist_count)
        return result


def artist_results_from_dict(s: Any) -> ArtistResults:
    return ArtistResults.from_dict(s)


def artist_results_to_dict(x: ArtistResults) -> Any:
    return to_class(ArtistResults, x)
