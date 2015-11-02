import json

QUIT_STRING = '\\q'
playlist = []


def save():
    filename = read_input('Save to file name: ')
    json_file = open(filename, mode='w')
    json_string = json.dumps(playlist).replace('"', '\'')
    json_file.write(json_string.encode('utf-8'))
    json_file.close()
    print 'Saved playlist JSON to file %s' % filename


def save_and_quit():
    save()
    quit()


def read_input(message):
    line = raw_input(message)
    if line.strip() == QUIT_STRING:
        quit()
    return line


def read_media():
    display_time = read_input('Display time (in seconds, positive int): ')
    if not display_time.isdigit():
        print 'Display time must be a digit'
        return None
    elif int(display_time) < 0:
        print 'Display time must be positive'
        return None

    content_url = read_input('Content URL: ')
    content_type = read_input('Content type (web_page/image/video): ')
    valid_types = ('web_page', 'image', 'video')
    if content_type not in valid_types:
        print 'Content type must be one of: %s, %s, %s' % valid_types
        return None
    media = {
        'time': display_time,
        'uri': content_url,
        'type': content_type
    }
    return media


def load_json_file():
    global playlist
    filepath = read_input('Write relative filepath of JSON file: ')
    json_file = open(filepath, mode='r')
    json_string = json_file.read()
    playlist = json.loads(json_string)
    print 'Loaded playlist:'
    show_media()


def show_media():
    if len(playlist) == 0:
        print 'No media in playlist'
        return
    index = 1
    for media in playlist:
        print '%s) %s' % (index, repr(media))
        index += 1


def remove_media():
    if len(playlist) == 0:
        print 'No media to remove'
        return
    print 'Choose index of media to remove:'
    index = 1
    for media in playlist:
        print '%s) %s' % (index, repr(media))

    del_index = read_input('Index of media to be removed: ')
    if not del_index.isdigit():
        print 'The choice must be one of the numbers provided'
        return
    del playlist[int(del_index)-1]


def add_media():
    media = read_media()
    if media is not None:
        playlist.append(media)
        print 'Added media %s' % repr(media)
    else:
        print 'Did not add media'


MENU_OPTIONS = (
    {
        'name': 'Show media',
        'handler': show_media
    },
    {
        'name': 'Add media',
        'handler': add_media
    },
    {
        'name': 'Remove media',
        'handler': remove_media
    },
    {
        'name': 'Save JSON to file',
        'handler': save
    },
    {
        'name': 'Load existing JSON file',
        'handler': load_json_file
    },
    {
        'name': 'Save and quit',
        'handler': save_and_quit
    },
    {
        'name': 'Quit without saving',
        'handler': quit
    }
)


def show_menu():
    while True:
        print '\nSelect an option:'
        index = 1
        for option in MENU_OPTIONS:
            print '%s) %s' % (index, option['name'])
            index += 1
        choice = read_input('Selection: ')
        if not choice.isdigit():
            print 'Choice must be a number'
            continue
        print '\n'
        handler = MENU_OPTIONS[int(choice)-1]['handler']
        handler()


def run():
    print 'This program will generate an ordered JSON playlist.'
    print 'Write %s and press enter to quit.\n' % QUIT_STRING
    show_menu()

if __name__ == '__main__':
    run()
