import vimeo
import settings
import logging
from utils import parse_response, get_filename, write_file

logger = logging.getLogger(__name__)


class Vimeo(vimeo.VimeoClient):
    def __init__(self):
        super(Vimeo, self).__init__(
            token=settings.ACCESS_TOKEN,
            key=settings.CLIENT_ID,
            secret=settings.CLIENT_SECRET
        )

    def get_data(self, videos_ids):
        data = {}
        for video_id in videos_ids:
            try:
                response = self.get(settings.API_URL.format(video_id))
                if response.status_code == 200:
                    picture_links = parse_response(video_id, response)
                    data[video_id] = picture_links
                else:
                    logger.error("Failed to get thumbup's link for video_id=%s - %s" % (video_id, response.text))
            except Exception as e:
                logger.error("Failed to get thumbup's link for video_id=%s - %s" % (video_id, e))
        return data

    def download_thumbups(self, data):
        for video_id, links in data.items():
            for i, link in enumerate(links, 1):
                try:
                    response = self.get(link, stream=True)
                    if response.status_code == 200:
                        file_name = get_filename(video_id, i)
                        write_file(file_name, response)
                    else:
                        logger.error('Failed to download thumbup for video %s - %s' % (video_id, response.text))
                except Exception as e:
                    logger.error('Failed to download thumbup for video %s - %s' % (video_id, e))
