# from api.model.album_lyrics import AlbumLyrics
#
#
# def write_to_csv(artist, album_words_list):
#     import csv
#     with open('../csv_files/{}.csv'.format(artist), mode='w', newline='') as artist_file:
#         fieldnames = ['album', 'simple_words', 'complex_words', 'total_words', '% simple', '% complex']
#         artist_writer = csv.DictWriter(artist_file, fieldnames=fieldnames)
#         artist_writer.writeheader()
#         for a in album_words_list:
#             if a:
#                 row = create_row(a)
#                 artist_writer.writerow(row)
#
#
# def create_row(a: AlbumLyrics):
#     percent_simple = prcnt(a.unique_word_count, a.total_word_count)
#     percent_complex = prcnt(a.unique_complex_word_count, a.total_word_count)
#
#     row = {'album': a.album, 'simple_words': a.unique_word_count,
#            'complex_words': a.unique_complex_word_count, 'total_words': a.total_word_count, '% simple': percent_simple,
#            '% complex': percent_complex}
#
#     return row
#
#

#
#
# if __name__ == '__main__':
#     print(prcnt(566, 1704))
