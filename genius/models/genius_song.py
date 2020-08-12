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
#     result = genius_song_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
import dateutil.parser


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


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class Artist:
    api_path: Optional[str] = None
    header_image_url: Optional[str] = None
    id: Optional[int] = None
    image_url: Optional[str] = None
    is_meme_verified: Optional[bool] = None
    is_verified: Optional[bool] = None
    name: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Artist':
        assert isinstance(obj, dict)
        api_path = from_union([from_str, from_none], obj.get("api_path"))
        header_image_url = from_union([from_str, from_none], obj.get("header_image_url"))
        id = from_union([from_int, from_none], obj.get("id"))
        image_url = from_union([from_str, from_none], obj.get("image_url"))
        is_meme_verified = from_union([from_bool, from_none], obj.get("is_meme_verified"))
        is_verified = from_union([from_bool, from_none], obj.get("is_verified"))
        name = from_union([from_str, from_none], obj.get("name"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Artist(api_path, header_image_url, id, image_url, is_meme_verified, is_verified, name, url)

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
class Album:
    api_path: Optional[str] = None
    cover_art_url: Optional[str] = None
    full_title: Optional[str] = None
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None
    artist: Optional[Artist] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Album':
        assert isinstance(obj, dict)
        api_path = from_union([from_str, from_none], obj.get("api_path"))
        cover_art_url = from_union([from_str, from_none], obj.get("cover_art_url"))
        full_title = from_union([from_str, from_none], obj.get("full_title"))
        id = from_union([from_int, from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        url = from_union([from_str, from_none], obj.get("url"))
        artist = from_union([Artist.from_dict, from_none], obj.get("artist"))
        return Album(api_path, cover_art_url, full_title, id, name, url, artist)

    def to_dict(self) -> dict:
        result: dict = {}
        result["api_path"] = from_union([from_str, from_none], self.api_path)
        result["cover_art_url"] = from_union([from_str, from_none], self.cover_art_url)
        result["full_title"] = from_union([from_str, from_none], self.full_title)
        result["id"] = from_union([from_int, from_none], self.id)
        result["name"] = from_union([from_str, from_none], self.name)
        result["url"] = from_union([from_str, from_none], self.url)
        result["artist"] = from_union([lambda x: to_class(Artist, x), from_none], self.artist)
        return result


@dataclass
class PurpleInteractions:
    pyong: Optional[bool] = None
    following: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleInteractions':
        assert isinstance(obj, dict)
        pyong = from_union([from_bool, from_none], obj.get("pyong"))
        following = from_union([from_bool, from_none], obj.get("following"))
        return PurpleInteractions(pyong, following)

    def to_dict(self) -> dict:
        result: dict = {}
        result["pyong"] = from_union([from_bool, from_none], self.pyong)
        result["following"] = from_union([from_bool, from_none], self.following)
        return result


@dataclass
class IqByAction:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'IqByAction':
        assert isinstance(obj, dict)
        return IqByAction()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class GeniusSongCurrentUserMetadata:
    permissions: Optional[List[str]] = None
    excluded_permissions: Optional[List[str]] = None
    interactions: Optional[PurpleInteractions] = None
    relationships: Optional[IqByAction] = None
    iq_by_action: Optional[IqByAction] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GeniusSongCurrentUserMetadata':
        assert isinstance(obj, dict)
        permissions = from_union([lambda x: from_list(from_str, x), from_none], obj.get("permissions"))
        excluded_permissions = from_union([lambda x: from_list(from_str, x), from_none], obj.get("excluded_permissions"))
        interactions = from_union([PurpleInteractions.from_dict, from_none], obj.get("interactions"))
        relationships = from_union([IqByAction.from_dict, from_none], obj.get("relationships"))
        iq_by_action = from_union([IqByAction.from_dict, from_none], obj.get("iq_by_action"))
        return GeniusSongCurrentUserMetadata(permissions, excluded_permissions, interactions, relationships, iq_by_action)

    def to_dict(self) -> dict:
        result: dict = {}
        result["permissions"] = from_union([lambda x: from_list(from_str, x), from_none], self.permissions)
        result["excluded_permissions"] = from_union([lambda x: from_list(from_str, x), from_none], self.excluded_permissions)
        result["interactions"] = from_union([lambda x: to_class(PurpleInteractions, x), from_none], self.interactions)
        result["relationships"] = from_union([lambda x: to_class(IqByAction, x), from_none], self.relationships)
        result["iq_by_action"] = from_union([lambda x: to_class(IqByAction, x), from_none], self.iq_by_action)
        return result


@dataclass
class CustomPerformance:
    label: Optional[str] = None
    artists: Optional[List[Artist]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CustomPerformance':
        assert isinstance(obj, dict)
        label = from_union([from_str, from_none], obj.get("label"))
        artists = from_union([lambda x: from_list(Artist.from_dict, x), from_none], obj.get("artists"))
        return CustomPerformance(label, artists)

    def to_dict(self) -> dict:
        result: dict = {}
        result["label"] = from_union([from_str, from_none], self.label)
        result["artists"] = from_union([lambda x: from_list(lambda x: to_class(Artist, x), x), from_none], self.artists)
        return result


@dataclass
class Description:
    plain: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Description':
        assert isinstance(obj, dict)
        plain = from_union([from_str, from_none], obj.get("plain"))
        return Description(plain)

    def to_dict(self) -> dict:
        result: dict = {}
        result["plain"] = from_union([from_str, from_none], self.plain)
        return result


@dataclass
class ClientTimestamps:
    updated_by_human_at: Optional[int] = None
    lyrics_updated_at: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ClientTimestamps':
        assert isinstance(obj, dict)
        updated_by_human_at = from_union([from_int, from_none], obj.get("updated_by_human_at"))
        lyrics_updated_at = from_union([from_int, from_none], obj.get("lyrics_updated_at"))
        return ClientTimestamps(updated_by_human_at, lyrics_updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result["updated_by_human_at"] = from_union([from_int, from_none], self.updated_by_human_at)
        result["lyrics_updated_at"] = from_union([from_int, from_none], self.lyrics_updated_at)
        return result


@dataclass
class Annotatable:
    api_path: Optional[str] = None
    client_timestamps: Optional[ClientTimestamps] = None
    context: Optional[str] = None
    id: Optional[int] = None
    image_url: Optional[str] = None
    link_title: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Annotatable':
        assert isinstance(obj, dict)
        api_path = from_union([from_str, from_none], obj.get("api_path"))
        client_timestamps = from_union([ClientTimestamps.from_dict, from_none], obj.get("client_timestamps"))
        context = from_union([from_str, from_none], obj.get("context"))
        id = from_union([from_int, from_none], obj.get("id"))
        image_url = from_union([from_str, from_none], obj.get("image_url"))
        link_title = from_union([from_str, from_none], obj.get("link_title"))
        title = from_union([from_str, from_none], obj.get("title"))
        type = from_union([from_str, from_none], obj.get("type"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Annotatable(api_path, client_timestamps, context, id, image_url, link_title, title, type, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["api_path"] = from_union([from_str, from_none], self.api_path)
        result["client_timestamps"] = from_union([lambda x: to_class(ClientTimestamps, x), from_none], self.client_timestamps)
        result["context"] = from_union([from_str, from_none], self.context)
        result["id"] = from_union([from_int, from_none], self.id)
        result["image_url"] = from_union([from_str, from_none], self.image_url)
        result["link_title"] = from_union([from_str, from_none], self.link_title)
        result["title"] = from_union([from_str, from_none], self.title)
        result["type"] = from_union([from_str, from_none], self.type)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class BoundingBox:
    width: Optional[int] = None
    height: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'BoundingBox':
        assert isinstance(obj, dict)
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        return BoundingBox(width, height)

    def to_dict(self) -> dict:
        result: dict = {}
        result["width"] = from_union([from_int, from_none], self.width)
        result["height"] = from_union([from_int, from_none], self.height)
        return result


@dataclass
class Medium:
    url: Optional[str] = None
    bounding_box: Optional[BoundingBox] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Medium':
        assert isinstance(obj, dict)
        url = from_union([from_str, from_none], obj.get("url"))
        bounding_box = from_union([BoundingBox.from_dict, from_none], obj.get("bounding_box"))
        return Medium(url, bounding_box)

    def to_dict(self) -> dict:
        result: dict = {}
        result["url"] = from_union([from_str, from_none], self.url)
        result["bounding_box"] = from_union([lambda x: to_class(BoundingBox, x), from_none], self.bounding_box)
        return result


@dataclass
class Avatar:
    tiny: Optional[Medium] = None
    thumb: Optional[Medium] = None
    small: Optional[Medium] = None
    medium: Optional[Medium] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Avatar':
        assert isinstance(obj, dict)
        tiny = from_union([Medium.from_dict, from_none], obj.get("tiny"))
        thumb = from_union([Medium.from_dict, from_none], obj.get("thumb"))
        small = from_union([Medium.from_dict, from_none], obj.get("small"))
        medium = from_union([Medium.from_dict, from_none], obj.get("medium"))
        return Avatar(tiny, thumb, small, medium)

    def to_dict(self) -> dict:
        result: dict = {}
        result["tiny"] = from_union([lambda x: to_class(Medium, x), from_none], self.tiny)
        result["thumb"] = from_union([lambda x: to_class(Medium, x), from_none], self.thumb)
        result["small"] = from_union([lambda x: to_class(Medium, x), from_none], self.small)
        result["medium"] = from_union([lambda x: to_class(Medium, x), from_none], self.medium)
        return result


@dataclass
class FluffyInteractions:
    following: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyInteractions':
        assert isinstance(obj, dict)
        following = from_union([from_bool, from_none], obj.get("following"))
        return FluffyInteractions(following)

    def to_dict(self) -> dict:
        result: dict = {}
        result["following"] = from_union([from_bool, from_none], self.following)
        return result


@dataclass
class UserCurrentUserMetadata:
    permissions: Optional[List[Any]] = None
    excluded_permissions: Optional[List[str]] = None
    interactions: Optional[FluffyInteractions] = None

    @staticmethod
    def from_dict(obj: Any) -> 'UserCurrentUserMetadata':
        assert isinstance(obj, dict)
        permissions = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("permissions"))
        excluded_permissions = from_union([lambda x: from_list(from_str, x), from_none], obj.get("excluded_permissions"))
        interactions = from_union([FluffyInteractions.from_dict, from_none], obj.get("interactions"))
        return UserCurrentUserMetadata(permissions, excluded_permissions, interactions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["permissions"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.permissions)
        result["excluded_permissions"] = from_union([lambda x: from_list(from_str, x), from_none], self.excluded_permissions)
        result["interactions"] = from_union([lambda x: to_class(FluffyInteractions, x), from_none], self.interactions)
        return result


@dataclass
class User:
    api_path: Optional[str] = None
    avatar: Optional[Avatar] = None
    header_image_url: Optional[str] = None
    human_readable_role_for_display: Optional[str] = None
    id: Optional[int] = None
    iq: Optional[int] = None
    login: Optional[str] = None
    name: Optional[str] = None
    role_for_display: Optional[str] = None
    url: Optional[str] = None
    current_user_metadata: Optional[UserCurrentUserMetadata] = None

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        api_path = from_union([from_str, from_none], obj.get("api_path"))
        avatar = from_union([Avatar.from_dict, from_none], obj.get("avatar"))
        header_image_url = from_union([from_str, from_none], obj.get("header_image_url"))
        human_readable_role_for_display = from_union([from_str, from_none], obj.get("human_readable_role_for_display"))
        id = from_union([from_int, from_none], obj.get("id"))
        iq = from_union([from_int, from_none], obj.get("iq"))
        login = from_union([from_str, from_none], obj.get("login"))
        name = from_union([from_str, from_none], obj.get("name"))
        role_for_display = from_union([from_str, from_none], obj.get("role_for_display"))
        url = from_union([from_str, from_none], obj.get("url"))
        current_user_metadata = from_union([UserCurrentUserMetadata.from_dict, from_none], obj.get("current_user_metadata"))
        return User(api_path, avatar, header_image_url, human_readable_role_for_display, id, iq, login, name, role_for_display, url, current_user_metadata)

    def to_dict(self) -> dict:
        result: dict = {}
        result["api_path"] = from_union([from_str, from_none], self.api_path)
        result["avatar"] = from_union([lambda x: to_class(Avatar, x), from_none], self.avatar)
        result["header_image_url"] = from_union([from_str, from_none], self.header_image_url)
        result["human_readable_role_for_display"] = from_union([from_str, from_none], self.human_readable_role_for_display)
        result["id"] = from_union([from_int, from_none], self.id)
        result["iq"] = from_union([from_int, from_none], self.iq)
        result["login"] = from_union([from_str, from_none], self.login)
        result["name"] = from_union([from_str, from_none], self.name)
        result["role_for_display"] = from_union([from_str, from_none], self.role_for_display)
        result["url"] = from_union([from_str, from_none], self.url)
        result["current_user_metadata"] = from_union([lambda x: to_class(UserCurrentUserMetadata, x), from_none], self.current_user_metadata)
        return result


@dataclass
class Author:
    attribution: Optional[float] = None
    pinned_role: Optional[str] = None
    user: Optional[User] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Author':
        assert isinstance(obj, dict)
        attribution = from_union([from_float, from_none], obj.get("attribution"))
        pinned_role = from_union([from_str, from_none], obj.get("pinned_role"))
        user = from_union([User.from_dict, from_none], obj.get("user"))
        return Author(attribution, pinned_role, user)

    def to_dict(self) -> dict:
        result: dict = {}
        result["attribution"] = from_union([to_float, from_none], self.attribution)
        result["pinned_role"] = from_union([from_str, from_none], self.pinned_role)
        result["user"] = from_union([lambda x: to_class(User, x), from_none], self.user)
        return result


@dataclass
class TentacledInteractions:
    cosign: Optional[bool] = None
    pyong: Optional[bool] = None
    vote: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TentacledInteractions':
        assert isinstance(obj, dict)
        cosign = from_union([from_bool, from_none], obj.get("cosign"))
        pyong = from_union([from_bool, from_none], obj.get("pyong"))
        vote = from_union([from_str, from_none], obj.get("vote"))
        return TentacledInteractions(cosign, pyong, vote)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cosign"] = from_union([from_bool, from_none], self.cosign)
        result["pyong"] = from_union([from_bool, from_none], self.pyong)
        result["vote"] = from_union([from_str, from_none], self.vote)
        return result


@dataclass
class AnnotationCurrentUserMetadata:
    permissions: Optional[List[str]] = None
    excluded_permissions: Optional[List[str]] = None
    interactions: Optional[TentacledInteractions] = None
    iq_by_action: Optional[IqByAction] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AnnotationCurrentUserMetadata':
        assert isinstance(obj, dict)
        permissions = from_union([lambda x: from_list(from_str, x), from_none], obj.get("permissions"))
        excluded_permissions = from_union([lambda x: from_list(from_str, x), from_none], obj.get("excluded_permissions"))
        interactions = from_union([TentacledInteractions.from_dict, from_none], obj.get("interactions"))
        iq_by_action = from_union([IqByAction.from_dict, from_none], obj.get("iq_by_action"))
        return AnnotationCurrentUserMetadata(permissions, excluded_permissions, interactions, iq_by_action)

    def to_dict(self) -> dict:
        result: dict = {}
        result["permissions"] = from_union([lambda x: from_list(from_str, x), from_none], self.permissions)
        result["excluded_permissions"] = from_union([lambda x: from_list(from_str, x), from_none], self.excluded_permissions)
        result["interactions"] = from_union([lambda x: to_class(TentacledInteractions, x), from_none], self.interactions)
        result["iq_by_action"] = from_union([lambda x: to_class(IqByAction, x), from_none], self.iq_by_action)
        return result


@dataclass
class Annotation:
    api_path: Optional[str] = None
    body: Optional[Description] = None
    comment_count: Optional[int] = None
    community: Optional[bool] = None
    custom_preview: Optional[str] = None
    has_voters: Optional[bool] = None
    id: Optional[int] = None
    pinned: Optional[bool] = None
    share_url: Optional[str] = None
    source: Optional[str] = None
    state: Optional[str] = None
    url: Optional[str] = None
    verified: Optional[bool] = None
    votes_total: Optional[int] = None
    current_user_metadata: Optional[AnnotationCurrentUserMetadata] = None
    authors: Optional[List[Author]] = None
    cosigned_by: Optional[List[Any]] = None
    rejection_comment: Optional[str] = None
    verified_by: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Annotation':
        assert isinstance(obj, dict)
        api_path = from_union([from_str, from_none], obj.get("api_path"))
        body = from_union([Description.from_dict, from_none], obj.get("body"))
        comment_count = from_union([from_int, from_none], obj.get("comment_count"))
        community = from_union([from_bool, from_none], obj.get("community"))
        custom_preview = from_union([from_str, from_none], obj.get("custom_preview"))
        has_voters = from_union([from_bool, from_none], obj.get("has_voters"))
        id = from_union([from_int, from_none], obj.get("id"))
        pinned = from_union([from_bool, from_none], obj.get("pinned"))
        share_url = from_union([from_str, from_none], obj.get("share_url"))
        source = from_union([from_str, from_none], obj.get("source"))
        state = from_union([from_str, from_none], obj.get("state"))
        url = from_union([from_str, from_none], obj.get("url"))
        verified = from_union([from_bool, from_none], obj.get("verified"))
        votes_total = from_union([from_int, from_none], obj.get("votes_total"))
        current_user_metadata = from_union([AnnotationCurrentUserMetadata.from_dict, from_none], obj.get("current_user_metadata"))
        authors = from_union([lambda x: from_list(Author.from_dict, x), from_none], obj.get("authors"))
        cosigned_by = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("cosigned_by"))
        rejection_comment = from_union([from_str, from_none], obj.get("rejection_comment"))
        verified_by = from_union([from_str, from_none], obj.get("verified_by"))
        return Annotation(api_path, body, comment_count, community, custom_preview, has_voters, id, pinned, share_url, source, state, url, verified, votes_total, current_user_metadata, authors, cosigned_by, rejection_comment, verified_by)

    def to_dict(self) -> dict:
        result: dict = {}
        result["api_path"] = from_union([from_str, from_none], self.api_path)
        result["body"] = from_union([lambda x: to_class(Description, x), from_none], self.body)
        result["comment_count"] = from_union([from_int, from_none], self.comment_count)
        result["community"] = from_union([from_bool, from_none], self.community)
        result["custom_preview"] = from_union([from_str, from_none], self.custom_preview)
        result["has_voters"] = from_union([from_bool, from_none], self.has_voters)
        result["id"] = from_union([from_int, from_none], self.id)
        result["pinned"] = from_union([from_bool, from_none], self.pinned)
        result["share_url"] = from_union([from_str, from_none], self.share_url)
        result["source"] = from_union([from_str, from_none], self.source)
        result["state"] = from_union([from_str, from_none], self.state)
        result["url"] = from_union([from_str, from_none], self.url)
        result["verified"] = from_union([from_bool, from_none], self.verified)
        result["votes_total"] = from_union([from_int, from_none], self.votes_total)
        result["current_user_metadata"] = from_union([lambda x: to_class(AnnotationCurrentUserMetadata, x), from_none], self.current_user_metadata)
        result["authors"] = from_union([lambda x: from_list(lambda x: to_class(Author, x), x), from_none], self.authors)
        result["cosigned_by"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.cosigned_by)
        result["rejection_comment"] = from_union([from_str, from_none], self.rejection_comment)
        result["verified_by"] = from_union([from_str, from_none], self.verified_by)
        return result


@dataclass
class Range:
    content: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Range':
        assert isinstance(obj, dict)
        content = from_union([from_str, from_none], obj.get("content"))
        return Range(content)

    def to_dict(self) -> dict:
        result: dict = {}
        result["content"] = from_union([from_str, from_none], self.content)
        return result


@dataclass
class DescriptionAnnotation:
    type: Optional[str] = None
    annotator_id: Optional[int] = None
    annotator_login: Optional[str] = None
    api_path: Optional[str] = None
    classification: Optional[str] = None
    fragment: Optional[str] = None
    id: Optional[int] = None
    is_description: Optional[bool] = None
    path: Optional[str] = None
    range: Optional[Range] = None
    song_id: Optional[int] = None
    url: Optional[str] = None
    verified_annotator_ids: Optional[List[Any]] = None
    annotatable: Optional[Annotatable] = None
    annotations: Optional[List[Annotation]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DescriptionAnnotation':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("_type"))
        annotator_id = from_union([from_int, from_none], obj.get("annotator_id"))
        annotator_login = from_union([from_str, from_none], obj.get("annotator_login"))
        api_path = from_union([from_str, from_none], obj.get("api_path"))
        classification = from_union([from_str, from_none], obj.get("classification"))
        fragment = from_union([from_str, from_none], obj.get("fragment"))
        id = from_union([from_int, from_none], obj.get("id"))
        is_description = from_union([from_bool, from_none], obj.get("is_description"))
        path = from_union([from_str, from_none], obj.get("path"))
        range = from_union([Range.from_dict, from_none], obj.get("range"))
        song_id = from_union([from_int, from_none], obj.get("song_id"))
        url = from_union([from_str, from_none], obj.get("url"))
        verified_annotator_ids = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("verified_annotator_ids"))
        annotatable = from_union([Annotatable.from_dict, from_none], obj.get("annotatable"))
        annotations = from_union([lambda x: from_list(Annotation.from_dict, x), from_none], obj.get("annotations"))
        return DescriptionAnnotation(type, annotator_id, annotator_login, api_path, classification, fragment, id, is_description, path, range, song_id, url, verified_annotator_ids, annotatable, annotations)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_type"] = from_union([from_str, from_none], self.type)
        result["annotator_id"] = from_union([from_int, from_none], self.annotator_id)
        result["annotator_login"] = from_union([from_str, from_none], self.annotator_login)
        result["api_path"] = from_union([from_str, from_none], self.api_path)
        result["classification"] = from_union([from_str, from_none], self.classification)
        result["fragment"] = from_union([from_str, from_none], self.fragment)
        result["id"] = from_union([from_int, from_none], self.id)
        result["is_description"] = from_union([from_bool, from_none], self.is_description)
        result["path"] = from_union([from_str, from_none], self.path)
        result["range"] = from_union([lambda x: to_class(Range, x), from_none], self.range)
        result["song_id"] = from_union([from_int, from_none], self.song_id)
        result["url"] = from_union([from_str, from_none], self.url)
        result["verified_annotator_ids"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.verified_annotator_ids)
        result["annotatable"] = from_union([lambda x: to_class(Annotatable, x), from_none], self.annotatable)
        result["annotations"] = from_union([lambda x: from_list(lambda x: to_class(Annotation, x), x), from_none], self.annotations)
        return result


@dataclass
class Media:
    provider: Optional[str] = None
    start: Optional[int] = None
    type: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Media':
        assert isinstance(obj, dict)
        provider = from_union([from_str, from_none], obj.get("provider"))
        start = from_union([from_int, from_none], obj.get("start"))
        type = from_union([from_str, from_none], obj.get("type"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Media(provider, start, type, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["provider"] = from_union([from_str, from_none], self.provider)
        result["start"] = from_union([from_int, from_none], self.start)
        result["type"] = from_union([from_str, from_none], self.type)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class ProducerArtist:
    api_path: Optional[str] = None
    header_image_url: Optional[str] = None
    id: Optional[int] = None
    image_url: Optional[str] = None
    is_meme_verified: Optional[bool] = None
    is_verified: Optional[bool] = None
    name: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ProducerArtist':
        assert isinstance(obj, dict)
        api_path = from_union([from_str, from_none], obj.get("api_path"))
        header_image_url = from_union([from_str, from_none], obj.get("header_image_url"))
        id = from_union([from_int, from_none], obj.get("id"))
        image_url = from_union([from_str, from_none], obj.get("image_url"))
        is_meme_verified = from_union([from_bool, from_none], obj.get("is_meme_verified"))
        is_verified = from_union([from_bool, from_none], obj.get("is_verified"))
        name = from_union([from_str, from_none], obj.get("name"))
        url = from_union([from_str, from_none], obj.get("url"))
        return ProducerArtist(api_path, header_image_url, id, image_url, is_meme_verified, is_verified, name, url)

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
class SongRelationship:
    relationship_type: Optional[str] = None
    type: Optional[str] = None
    songs: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SongRelationship':
        assert isinstance(obj, dict)
        relationship_type = from_union([from_str, from_none], obj.get("relationship_type"))
        type = from_union([from_str, from_none], obj.get("type"))
        songs = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("songs"))
        return SongRelationship(relationship_type, type, songs)

    def to_dict(self) -> dict:
        result: dict = {}
        result["relationship_type"] = from_union([from_str, from_none], self.relationship_type)
        result["type"] = from_union([from_str, from_none], self.type)
        result["songs"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.songs)
        return result


@dataclass
class Stats:
    accepted_annotations: Optional[int] = None
    contributors: Optional[int] = None
    iq_earners: Optional[int] = None
    transcribers: Optional[int] = None
    unreviewed_annotations: Optional[int] = None
    verified_annotations: Optional[int] = None
    hot: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Stats':
        assert isinstance(obj, dict)
        accepted_annotations = from_union([from_int, from_none], obj.get("accepted_annotations"))
        contributors = from_union([from_int, from_none], obj.get("contributors"))
        iq_earners = from_union([from_int, from_none], obj.get("iq_earners"))
        transcribers = from_union([from_int, from_none], obj.get("transcribers"))
        unreviewed_annotations = from_union([from_int, from_none], obj.get("unreviewed_annotations"))
        verified_annotations = from_union([from_int, from_none], obj.get("verified_annotations"))
        hot = from_union([from_bool, from_none], obj.get("hot"))
        return Stats(accepted_annotations, contributors, iq_earners, transcribers, unreviewed_annotations, verified_annotations, hot)

    def to_dict(self) -> dict:
        result: dict = {}
        result["accepted_annotations"] = from_union([from_int, from_none], self.accepted_annotations)
        result["contributors"] = from_union([from_int, from_none], self.contributors)
        result["iq_earners"] = from_union([from_int, from_none], self.iq_earners)
        result["transcribers"] = from_union([from_int, from_none], self.transcribers)
        result["unreviewed_annotations"] = from_union([from_int, from_none], self.unreviewed_annotations)
        result["verified_annotations"] = from_union([from_int, from_none], self.verified_annotations)
        result["hot"] = from_union([from_bool, from_none], self.hot)
        return result


@dataclass
class WriterArtist:
    api_path: Optional[str] = None
    header_image_url: Optional[str] = None
    id: Optional[int] = None
    image_url: Optional[str] = None
    is_meme_verified: Optional[bool] = None
    is_verified: Optional[bool] = None
    name: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'WriterArtist':
        assert isinstance(obj, dict)
        api_path = from_union([from_str, from_none], obj.get("api_path"))
        header_image_url = from_union([from_str, from_none], obj.get("header_image_url"))
        id = from_union([from_int, from_none], obj.get("id"))
        image_url = from_union([from_str, from_none], obj.get("image_url"))
        is_meme_verified = from_union([from_bool, from_none], obj.get("is_meme_verified"))
        is_verified = from_union([from_bool, from_none], obj.get("is_verified"))
        name = from_union([from_str, from_none], obj.get("name"))
        url = from_union([from_str, from_none], obj.get("url"))
        return WriterArtist(api_path, header_image_url, id, image_url, is_meme_verified, is_verified, name, url)

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
class GeniusSong:
    annotation_count: Optional[int] = None
    api_path: Optional[str] = None
    apple_music_id: Optional[str] = None
    apple_music_player_url: Optional[str] = None
    description: Optional[Description] = None
    embed_content: Optional[str] = None
    featured_video: Optional[bool] = None
    full_title: Optional[str] = None
    header_image_thumbnail_url: Optional[str] = None
    header_image_url: Optional[str] = None
    id: Optional[int] = None
    lyrics_owner_id: Optional[int] = None
    lyrics_placeholder_reason: Optional[str] = None
    lyrics_state: Optional[str] = None
    path: Optional[str] = None
    pyongs_count: Optional[str] = None
    recording_location: Optional[str] = None
    release_date: Optional[datetime] = None
    release_date_for_display: Optional[str] = None
    song_art_image_thumbnail_url: Optional[str] = None
    song_art_image_url: Optional[str] = None
    stats: Optional[Stats] = None
    title: Optional[str] = None
    title_with_featured: Optional[str] = None
    url: Optional[str] = None
    current_user_metadata: Optional[GeniusSongCurrentUserMetadata] = None
    album: Optional[Album] = None
    custom_performances: Optional[List[CustomPerformance]] = None
    description_annotation: Optional[DescriptionAnnotation] = None
    featured_artists: Optional[List[Any]] = None
    lyrics_marked_complete_by: Optional[str] = None
    media: Optional[List[Media]] = None
    primary_artist: Optional[Artist] = None
    producer_artists: Optional[List[ProducerArtist]] = None
    song_relationships: Optional[List[SongRelationship]] = None
    verified_annotations_by: Optional[List[Any]] = None
    verified_contributors: Optional[List[Any]] = None
    verified_lyrics_by: Optional[List[Any]] = None
    writer_artists: Optional[List[WriterArtist]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GeniusSong':
        assert isinstance(obj, dict)
        annotation_count = from_union([from_int, from_none], obj.get("annotation_count"))
        api_path = from_union([from_str, from_none], obj.get("api_path"))
        apple_music_id = from_union([from_str, from_none], obj.get("apple_music_id"))
        apple_music_player_url = from_union([from_str, from_none], obj.get("apple_music_player_url"))
        description = from_union([Description.from_dict, from_none], obj.get("description"))
        embed_content = from_union([from_str, from_none], obj.get("embed_content"))
        featured_video = from_union([from_bool, from_none], obj.get("featured_video"))
        full_title = from_union([from_str, from_none], obj.get("full_title"))
        header_image_thumbnail_url = from_union([from_str, from_none], obj.get("header_image_thumbnail_url"))
        header_image_url = from_union([from_str, from_none], obj.get("header_image_url"))
        id = from_union([from_int, from_none], obj.get("id"))
        lyrics_owner_id = from_union([from_int, from_none], obj.get("lyrics_owner_id"))
        lyrics_placeholder_reason = from_union([from_str, from_none], obj.get("lyrics_placeholder_reason"))
        lyrics_state = from_union([from_str, from_none], obj.get("lyrics_state"))
        path = from_union([from_str, from_none], obj.get("path"))
        pyongs_count = from_union([from_str, from_none], obj.get("pyongs_count"))
        recording_location = from_union([from_str, from_none], obj.get("recording_location"))
        release_date = from_union([from_datetime, from_none], obj.get("release_date"))
        release_date_for_display = from_union([from_str, from_none], obj.get("release_date_for_display"))
        song_art_image_thumbnail_url = from_union([from_str, from_none], obj.get("song_art_image_thumbnail_url"))
        song_art_image_url = from_union([from_str, from_none], obj.get("song_art_image_url"))
        stats = from_union([Stats.from_dict, from_none], obj.get("stats"))
        title = from_union([from_str, from_none], obj.get("title"))
        title_with_featured = from_union([from_str, from_none], obj.get("title_with_featured"))
        url = from_union([from_str, from_none], obj.get("url"))
        current_user_metadata = from_union([GeniusSongCurrentUserMetadata.from_dict, from_none], obj.get("current_user_metadata"))
        album = from_union([Album.from_dict, from_none], obj.get("album"))
        custom_performances = from_union([lambda x: from_list(CustomPerformance.from_dict, x), from_none], obj.get("custom_performances"))
        description_annotation = from_union([DescriptionAnnotation.from_dict, from_none], obj.get("description_annotation"))
        featured_artists = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("featured_artists"))
        lyrics_marked_complete_by = from_union([from_str, from_none], obj.get("lyrics_marked_complete_by"))
        media = from_union([lambda x: from_list(Media.from_dict, x), from_none], obj.get("media"))
        primary_artist = from_union([Artist.from_dict, from_none], obj.get("primary_artist"))
        producer_artists = from_union([lambda x: from_list(ProducerArtist.from_dict, x), from_none], obj.get("producer_artists"))
        song_relationships = from_union([lambda x: from_list(SongRelationship.from_dict, x), from_none], obj.get("song_relationships"))
        verified_annotations_by = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("verified_annotations_by"))
        verified_contributors = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("verified_contributors"))
        verified_lyrics_by = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("verified_lyrics_by"))
        writer_artists = from_union([lambda x: from_list(WriterArtist.from_dict, x), from_none], obj.get("writer_artists"))
        return GeniusSong(annotation_count, api_path, apple_music_id, apple_music_player_url, description, embed_content, featured_video, full_title, header_image_thumbnail_url, header_image_url, id, lyrics_owner_id, lyrics_placeholder_reason, lyrics_state, path, pyongs_count, recording_location, release_date, release_date_for_display, song_art_image_thumbnail_url, song_art_image_url, stats, title, title_with_featured, url, current_user_metadata, album, custom_performances, description_annotation, featured_artists, lyrics_marked_complete_by, media, primary_artist, producer_artists, song_relationships, verified_annotations_by, verified_contributors, verified_lyrics_by, writer_artists)

    def to_dict(self) -> dict:
        result: dict = {}
        result["annotation_count"] = from_union([from_int, from_none], self.annotation_count)
        result["api_path"] = from_union([from_str, from_none], self.api_path)
        result["apple_music_id"] = from_union([from_str, from_none], self.apple_music_id)
        result["apple_music_player_url"] = from_union([from_str, from_none], self.apple_music_player_url)
        result["description"] = from_union([lambda x: to_class(Description, x), from_none], self.description)
        result["embed_content"] = from_union([from_str, from_none], self.embed_content)
        result["featured_video"] = from_union([from_bool, from_none], self.featured_video)
        result["full_title"] = from_union([from_str, from_none], self.full_title)
        result["header_image_thumbnail_url"] = from_union([from_str, from_none], self.header_image_thumbnail_url)
        result["header_image_url"] = from_union([from_str, from_none], self.header_image_url)
        result["id"] = from_union([from_int, from_none], self.id)
        result["lyrics_owner_id"] = from_union([from_int, from_none], self.lyrics_owner_id)
        result["lyrics_placeholder_reason"] = from_union([from_str, from_none], self.lyrics_placeholder_reason)
        result["lyrics_state"] = from_union([from_str, from_none], self.lyrics_state)
        result["path"] = from_union([from_str, from_none], self.path)
        result["pyongs_count"] = from_union([from_str, from_none], self.pyongs_count)
        result["recording_location"] = from_union([from_str, from_none], self.recording_location)
        result["release_date"] = from_union([lambda x: x.isoformat(), from_none], self.release_date)
        result["release_date_for_display"] = from_union([from_str, from_none], self.release_date_for_display)
        result["song_art_image_thumbnail_url"] = from_union([from_str, from_none], self.song_art_image_thumbnail_url)
        result["song_art_image_url"] = from_union([from_str, from_none], self.song_art_image_url)
        result["stats"] = from_union([lambda x: to_class(Stats, x), from_none], self.stats)
        result["title"] = from_union([from_str, from_none], self.title)
        result["title_with_featured"] = from_union([from_str, from_none], self.title_with_featured)
        result["url"] = from_union([from_str, from_none], self.url)
        result["current_user_metadata"] = from_union([lambda x: to_class(GeniusSongCurrentUserMetadata, x), from_none], self.current_user_metadata)
        result["album"] = from_union([lambda x: to_class(Album, x), from_none], self.album)
        result["custom_performances"] = from_union([lambda x: from_list(lambda x: to_class(CustomPerformance, x), x), from_none], self.custom_performances)
        result["description_annotation"] = from_union([lambda x: to_class(DescriptionAnnotation, x), from_none], self.description_annotation)
        result["featured_artists"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.featured_artists)
        result["lyrics_marked_complete_by"] = from_union([from_str, from_none], self.lyrics_marked_complete_by)
        result["media"] = from_union([lambda x: from_list(lambda x: to_class(Media, x), x), from_none], self.media)
        result["primary_artist"] = from_union([lambda x: to_class(Artist, x), from_none], self.primary_artist)
        result["producer_artists"] = from_union([lambda x: from_list(lambda x: to_class(ProducerArtist, x), x), from_none], self.producer_artists)
        result["song_relationships"] = from_union([lambda x: from_list(lambda x: to_class(SongRelationship, x), x), from_none], self.song_relationships)
        result["verified_annotations_by"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.verified_annotations_by)
        result["verified_contributors"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.verified_contributors)
        result["verified_lyrics_by"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.verified_lyrics_by)
        result["writer_artists"] = from_union([lambda x: from_list(lambda x: to_class(WriterArtist, x), x), from_none], self.writer_artists)
        return result


def genius_song_from_dict(s: Any) -> GeniusSong:
    return GeniusSong.from_dict(s)


def genius_song_to_dict(x: GeniusSong) -> Any:
    return to_class(GeniusSong, x)
