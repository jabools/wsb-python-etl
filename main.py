from argparse import ArgumentParser
from connection import Connection
from songs_manager import SongsManager
import time


def get_args():
    parser = ArgumentParser(description='Artists rating application.')
    parser.add_argument('--path', dest='path', type=str, required=True)
    parser.add_argument('--tracks', dest='tracks', type=str, required=True)
    parser.add_argument('--plays', dest='plays', type=str, required=True)

    return parser.parse_args()


def main():
    start_time = time.time()
    args = get_args()

    connection = Connection(args.path)
    connection.init(args.tracks, args.plays)

    songs_manager = SongsManager(connection.connection)

    best_artist = songs_manager.best_artist()
    print('*** BEST ARTIST ***\n\'' + str(best_artist[0]) + '\' with ' + str(best_artist[1]) + ' plays.\n')
    print('*** TOP 5 MOST PLAYED SONGS ***')

    for artist, title, plays in songs_manager.top_listened_songs():
        print('{0} - {1} was played {2} times'.format(artist, title.strip(), plays))

    connection.disconnect()

    stop_time = time.time()

    print('\nAll queries executed within {0} seconds.'.format(stop_time - start_time))


if __name__ == '__main__':
    main()
