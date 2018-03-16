import settings
import logging
import os
import sys

logger = logging.getLogger(__name__)


def parse_response(video_id, response):
    data = response.json()
    if settings.TIME:
        thumbnails = [data]
    else:
        thumbnails = data['data']
    try:
        links = []
        for thumbnail in thumbnails:
            if thumbnail['active'] == settings.ACTIVE:
                for size in thumbnail['sizes']:
                    if size['width'] == settings.WIDTH:
                        link = size[settings.LINK_TYPE]
                        links.append(link)
        if len(links) == 0:
            logger.warning('Thumbnails for %s with the following settings are not found: active - %s, width - %s'
                           % (video_id, settings.ACTIVE, settings.WIDTH))
        else:
            if settings.TIME:
                logger.info('Set new thumbnail for video %s' % video_id)
            else:
                logger.info('Got thumbnails info about video %s' % video_id)
        return links
    except Exception as e:
        logger.error('Exception %s while parsing response %s' % (e, response.text))


def get_filename(video_id, index):
    current_dir = os.getcwd()
    if not os.path.exists(os.path.join(current_dir, 'downloads')):
        os.makedirs(os.path.join(current_dir, 'downloads'))
    if settings.ACTIVE:
        if settings.TIME:
            file_name = '{}_offset_{}.jpg'.format(video_id, settings.TIME)
        else:
            file_name = '{}_default.jpg'.format(video_id)
    else:
        file_name = '{}_inactive_{}.jpg'.format(video_id, index)
    return os.path.join(current_dir, 'downloads', file_name)


def write_file(file_name, response):
    try:
        with open(file_name, 'wb') as file:
            for chunk in response:
                file.write(chunk)
        logger.info('File %s is saved' % file_name)
    except Exception as e:
        logger.error('Error while writing file %s - %s' % (file_name, e))


def configure_logging():
    logging.basicConfig(
        filename=None,
        level=logging.DEBUG,
        format='%(asctime)s: %(levelname)7s: [%(name)s]: %(message)s',
        datefmt='%H:%M:%S'
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def check_configuration():
    if not hasattr(settings, 'ACTIVE'):
        sys.exit("Your configuration file doesn't have ACTIVE parameter")
    if not isinstance(settings.ACTIVE, bool):
        sys.exit("ACTIVE must be boolean")
    if getattr(settings, 'TIME', None) and not settings.ACTIVE:
        sys.exit("Wrong configuration - ACTIVE=%s, TIME=%s" % (settings.ACTIVE, settings.TIME))
