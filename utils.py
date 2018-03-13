import settings
import logging
import os

logger = logging.getLogger(__name__)


def parse_response(video_id, response):
    if response.status_code == 200:
        data = response.json()
        try:
            links = []
            for picture in data['data']:
                if picture['active'] == settings.ACTIVE:
                    for size in picture['sizes']:
                        if size['width'] == settings.WIDTH:
                            link = size[settings.LINK_TYPE]
                            links.append(link)
            if len(links) == 0:
                logger.warning('Thumbnails for %s with the following settings are not found: active - %s, width - %s'
                               % (video_id, settings.ACTIVE, settings.WIDTH))
            else:
                logger.info('Got thumbnails info about video %s' % video_id)
            return links
        except Exception as e:
            logger.error('Exception while parsing response %s' % response.text)


def get_filename(video_id, index):
    current_dir = os.getcwd()
    if not os.path.exists(os.path.join(current_dir, 'downloads')):
        os.makedirs(os.path.join(current_dir, 'downloads'))
    if settings.ACTIVE:
        file_name = '{}_default.jpg'.format(video_id)
    else:
        file_name = '{}_{}.jpg'.format(video_id, index)
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
