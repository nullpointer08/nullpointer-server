from magic import from_file
from mimetypes import guess_type
import logging

logger =logging.getLogger(__name__)

VIDEO = 'V'
IMAGE = 'I'
WEB_PAGE = 'W'
MEDIA_CHOICES = (
    (VIDEO, 'video'),
    (IMAGE, 'image'),
    (WEB_PAGE, 'web_page'),
)


def determine_media_type(file_path):
    mime = from_file(file_path, mime=True)
    file_type = mime.split('/', 1)[0]
    media_type = None
    for choice in MEDIA_CHOICES:
        if choice[1] == file_type:
            media_type = choice[0]

    if not media_type or len(media_type) > 1:
        raise TypeError("media type error: ", file_type)
    return media_type


def determine_media_type_from_filename(filename):
    type = guess_type(filename, strict=True)[0].split('/',1)[0]
    logger.debug("TYPE: %s", type)
    if type in MEDIA_CHOICES:
        return True
    return False