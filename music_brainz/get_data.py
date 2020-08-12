import logging

import musicbrainzngs

from typing import List, Dict

from logger import logger
from music_brainz.models.album import Album, Track
from music_brainz.models.release import MediumList, Release, TrackList
from music_brainz.models.release import release_from_dict
from music_brainz.models.artist_results import ArtistResults
from utils.misc_utils import clean_text, compare_strings, check_for_excluded

INVALID_SECONDARY_TYPES = ['dj-mix', 'live', 'compilation', 'soundtrack', 'mixtape/street', 'demo']

LOGGER = logger.setup_logger('root', logging.DEBUG)


def get_album_art_urls(release_id):
    urls = None
    image_list = musicbrainzngs.get_image_list(release_id)
    if 'images' in image_list:
        if len(image_list['images']) == 0:
            return None
        if len(image_list['images']) >= 1:
            if image_list['images'][0]:
                if image_list['images'][0]['thumbnails']:
                    urls = image_list['images'][0]['thumbnails']

    return urls


def get_artist_data(artist):
    musicbrainzngs.set_useragent("Lyrical Beatdown", "0.2", "brock@teka.com")
    a_res = musicbrainzngs.search_artists(artist, strict=True, limit=5)

    if a_res:
        artist_results = ArtistResults().from_dict(a_res)
        if artist_results.artist_list and len(artist_results.artist_list) > 0:
            artist_result = get_closest_musicbrainz_match(artist, artist_results)

            if artist_result:
                return artist_result

    return None


def compare_albums(same_albums: Dict[str, List[Release]]):
    c_album = None
    if len(same_albums) == 1:
        return None
    if len(same_albums) > 0:
        for l in same_albums.values():
            if len(l) == 1:
                return None
            elif len(l) == 0:
                return None
            i = 0
            for a in l:
                if i == 0:
                    c_album = Album().from_mb_release(a, None, 'Silverstein')
                    i += 1
                    continue
                else:
                    i += 1
                    t_album = Album().from_mb_release(a, None, 'Silverstein')
                    if compare_strings(t_album.mb_data.title, c_album.mb_data.title):
                        continue
                    print(c_album.mb_data.title, end=' -- ')
                    print(t_album.mb_data.title)

                    c_lim = len(c_album.tracks) - 1
                    t_lim = len(t_album.tracks) - 1
                    if c_lim == t_lim:
                        continue
                    lim = t_lim
                    if c_lim > t_lim:
                        lim = c_lim
                    for x in range(0, lim):
                        if x <= t_lim:
                            if t_album.tracks[x].disambiguation:
                                print("{} ({})".format(t_album.tracks[x].title, t_album.tracks[x].disambiguation),
                                      end=' -- ')
                            # print("{} ({})".format(t_album.tracks[x].title, t_album.tracks[x].disambiguation),
                            #       end=' -- ')
                        if x <= c_lim:
                            if c_album.tracks[x].disambiguation:
                                print("{} ({})".format(c_album.tracks[x].title, c_album.tracks[x].disambiguation),
                                      end=' ')
                            # print("{} ({})".format(c_album.tracks[x].title, c_album.tracks[x].disambiguation), end=' ')
                        # print('')
            # print('------')


def group_same_albums(albums):
    same_albums = {}

    for a in albums:
        if len(same_albums) == 0:
            same_albums[clean_text(a.title)] = []
            same_albums[clean_text(a.title)].append(a)
        else:
            exists = False
            for k in same_albums.keys():
                if compare_strings(a.title, k, relaxed=True):
                    exists = True
                    if a.title != k:
                        if len(a.title) < len(k):
                            same_albums[k] = same_albums[a.title]
                            del same_albums[a.title]
                            same_albums[k].append(a)
                            break
                    same_albums[k].append(a)

            if not exists:
                same_albums[clean_text(a.title)] = []
                same_albums[clean_text(a.title)].append(a)

    return same_albums


def is_title_in_original(original_track_list: List[TrackList], release_title):
    for track in original_track_list:
        if compare_strings(track.recording.title, release_title, very_relaxed=True):
            return True
    return False


def invalid_disambiguation(disambiguation):
    invalid_disambiguations = ['acoustic', 'voice note', 'demo version', 'demo', 're-recording', 'karaoke',
                               'music video']
    for inv_dis in invalid_disambiguations:
        if compare_strings(disambiguation, inv_dis):
            return True

    return False


def get_artist_albums_from_mb(mb_artist):
    albums: List[Release] = []

    musicbrainzngs.set_useragent("Lyrical Beatdown", "0.2", "brock@teka.com")

    if mb_artist:
        artist_id = mb_artist.id

        artist_releases = musicbrainzngs.browse_releases(artist=artist_id, release_type=["album"],
                                                         includes=['media', 'recordings', 'discids',
                                                                   'release-groups', 'labels'],
                                                         release_status=['official'], limit=100)
        releases = {**artist_releases}

        offset = len(releases['release-list'])

        if offset <= artist_releases['release-count']:
            for x in range(0, 100):
                # , releases['release-count']
                if offset >= artist_releases['release-count']:
                    break

                artist_releases = musicbrainzngs.browse_releases(artist=artist_id, release_type=["album"],
                                                                 includes=['media', 'recordings', 'discids',
                                                                           'release-groups', 'labels'],
                                                                 release_status=['official'], limit=100,
                                                                 offset=offset)

                releases['release-list'].extend(artist_releases['release-list'])

                offset = offset + len(artist_releases['release-list'])

        if releases:
            if 'release-list' in releases:
                for release in releases['release-list']:
                    if 'status' in release:
                        if release['status'].lower() == 'official':
                            try:
                                _release = release_from_dict(release)
                            except AssertionError as ae:
                                logger.debug(LOGGER, release['title'])
                                continue
                            skip = False
                            if _release.release_group.secondary_type_list and len(
                                    _release.release_group.secondary_type_list) > 0:
                                for st in _release.release_group.secondary_type_list:
                                    if st.lower() in INVALID_SECONDARY_TYPES:
                                        skip = True
                                        # logger.debug(LOGGER,
                                        print(
                                            'Skipping {} due to having an invalid secondary type: {}'.format(
                                                _release.title, st))
                                    else:
                                        # logger.debug(LOGGER,
                                        print(
                                            "{} has secondary type: {}".format(_release.title, st))

                            if not skip:
                                albums.append(_release)

        if len(albums) == 0:
            return None

        same_albums = group_same_albums(albums)

        valid_albums = []

        for album_key in same_albums:
            # logger.log(LOGGER,  '\n{}'.format(album_key))
            valid_albums.append(many_to_one_album(same_albums[album_key], mb_artist.name))

        # The album didn't get appended to the same albums dict
        if len(valid_albums) == 0 and len(albums) == 1:
            valid_albums.append(many_to_one_album(albums, mb_artist.name))

        logger.debug(LOGGER, '\n\nValid Albums:')
        print('\n\nValid Albums:')
        for va in valid_albums:
            # logger.debug(LOGGER,"\n{}".format(va.mb_data.title))
            print("\n{}".format(va.mb_data.title))
            for track in va.tracks:
                # logger.debug(LOGGER,"-- {}".format(track.title))
                print("-- {}".format(track.title))
            logger.debug(LOGGER, "\n{}: Bonus Tracks".format(va.mb_data.title))
            print("\n{}: Bonus Tracks".format(va.mb_data.title))
            for bonus_track in va.bonus_tracks:
                # logger.debug(LOGGER, "-- {}".format(bonus_track.title))
                print("-- {}".format(bonus_track.title))

        return valid_albums

    return None


def get_closest_musicbrainz_match(artist_name, artist_results: ArtistResults):
    for artist in artist_results.artist_list:
        if compare_strings(artist.name, artist_name):
            return artist
    return None


def us_or_xw(release):
    if release.country:
        if release.country.lower() == 'us' or release.country.lower() == 'xw' or release.country.lower() == 'xe':
            return True
    return False


def get_original(releases):
    original: Release = releases[0]

    original_set = False

    cover_art = False

    for release in releases:
        if release.release_group.first_release_date:
            if release.date == release.release_group.first_release_date:
                original = release
                original_set = True
                break

    if not original_set:
        for release in releases:
            if release.date and original.date:
                if release.date < original.date:
                    # logger.log(LOGGER,  "Release ({}) is older than original({})".format(release.date, original.date))
                    original = release
                    original_set = True

    if original.cover_art_archive:
        if original.cover_art_archive.front:
            cover_art = True

    if original.label_info_count == 0:
        for release in releases:
            if release.label_info_count > 0:
                for l in release.label_info_list:
                    if l.label:
                        if l.label.name:
                            original.label_info_count = release.label_info_count
                            original.label_info_list = release.label_info_list
                            break

    if not cover_art:
        for release in releases:
            if release.cover_art_archive:
                if release.cover_art_archive.front:
                    original.sub_cover_art = release.id
                    break

    if not cover_art and not original.sub_cover_art:
        logger.debug(LOGGER, 'No cover art found for {}'.format(original.title))

    if original.label_info_count == 0:
        logger.debug(LOGGER, 'No label found for {}'.format(original.title))

    return original


def medium_list_to_track_list(medium_list: List[MediumList]):
    new_medium_list: List[MediumList] = []

    valid_medium_formats = ['CD', 'Enhanced CD', 'Digital Media']

    for medium in medium_list:
        if medium.format:
            for valid_format in valid_medium_formats:
                if compare_strings(medium.format, valid_format):
                    new_medium_list.append(medium)

    new_track_list: List[TrackList] = []

    for new_medium in new_medium_list:
        if new_medium.track_count > 0:
            for track in new_medium.track_list:
                exists = False
                if not check_for_excluded(track.recording.title):
                    if track.recording.disambiguation:
                        logger.debug(LOGGER, "{} has disambiguation: {}".format(track.recording.title,
                                                                                track.recording.disambiguation))
                    if len(new_track_list) > 0:
                        for new_track in new_track_list:
                            if compare_strings(new_track.recording.title, track.recording.title):
                                exists = True
                        if not exists:
                            new_track_list.append(track)
                            # logger.error(LOGGER, "Track was already in track list when building new medium list")
                    else:
                        new_track_list.append(track)

    return new_track_list


def get_bonus_tracks(us_releases, original, original_track_list):
    bonus_tracks = []

    for release in us_releases:
        if release.id == original.id:
            continue
        if release.medium_count and release.medium_count > 0:
            if original.medium_count and original.medium_count > 0:
                release_track_list = medium_list_to_track_list(release.medium_list)
                for track in release_track_list:
                    exists = False
                    bonus_track = check_release_track_is_bonus(track, original.title,
                                                               original_track_list)
                    if bonus_track:
                        if len(bonus_tracks) > 0:
                            for bt in bonus_tracks:
                                if compare_strings(bt.title, bonus_track.title):
                                    exists = True
                                    break
                            if not exists:
                                bonus_tracks.append(bonus_track)
                        else:
                            bonus_tracks.append(bonus_track)

    return bonus_tracks


def check_release_track_is_bonus(track, original_title, original_track_list):
    if track.recording:
        logger.debug(LOGGER, "\nNot on original: {}".format(track.recording.title))
        if track.recording.disambiguation:
            logger.debug(LOGGER, "-- {} has disambiguation: {}".format(
                track.recording.title, track.recording.disambiguation))
        if check_for_excluded(track.recording.title):
            return None
        if not is_title_in_original(original_track_list,
                                    track.recording.title):
            bonus_track = Track(track.id, track.recording.title, track.recording.length,
                                track.recording.disambiguation, track.number, track)
            return bonus_track
        else:
            logger.debug(LOGGER, "-- Title: {} was in album: {}".format(
                track.recording.title, original_title))
    return None


def many_to_one_album(album_list, artist_name, include_bonus_tracks=True):
    # if no albums exist, return None
    if len(album_list) == 0:
        logger.debug(LOGGER, 'No albums found for "many_to_one" conversion, skipping...')
        return None

    original = None

    # if a single album exists, there's no need to proceed, return the single album
    if len(album_list) == 1:
        original = album_list[0]

    # get all US, EU, or Worldwide releases
    us_releases = [x for x in album_list if us_or_xw(x)]

    # if there are no US releases, revert back to the original album list
    if len(us_releases) == 0:
        us_releases = album_list

    # if there is only one US (or EU, XE) release, return the single release
    if len(us_releases) == 1:
        original = us_releases[0]

    album_art_urls = None
    if not original:
        original: Release = get_original(us_releases)

    if original.cover_art_archive:
        if original.cover_art_archive.front:
            if original.id:
                album_art_urls = get_album_art_urls(original.id)
    if not album_art_urls:
        if original.sub_cover_art:
            album_art_urls = get_album_art_urls(original.sub_cover_art)

    if not album_art_urls:
        logger.debug(LOGGER, 'No Album Art found for {}'.format(original.title))

    # TODO: complete this section to include bonus tracks in album if requested
    original_track_list = medium_list_to_track_list(original.medium_list)

    bonus_tracks = []

    if include_bonus_tracks:
        bonus_tracks = get_bonus_tracks(us_releases, original, original_track_list)

    tracks: List[Track] = []

    for track in original_track_list:
        new_track = Track(track.id, track.recording.title, track.recording.length,
                          track.recording.disambiguation, track.number, track)
        tracks.append(new_track)

    album: Album = Album().from_mb_release(original, album_art_urls, artist_name, tracks, bonus_tracks)

    return album


if __name__ == '__main__':
    logger.set_logging(False)
    # ARTISTS = ['Senses Fail', 'The Used', 'Taking Back Sunday', 'Underoath']
    ARTISTS = ['The Used']
    for artist in ARTISTS:
        mb_artist = get_artist_data(artist)
        albums = get_artist_albums_from_mb(mb_artist)
