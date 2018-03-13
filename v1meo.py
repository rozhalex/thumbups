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
        self.files_saved = 0
        self.links = 0

    def get_data(self, videos_ids):
        if len(videos_ids) == len(set(videos_ids)):
            logger.info("Got %s videos to proceed" % len(videos_ids))
        else:
            logger.info("Got %s videos to proceed. Only %s are unique" % (len(videos_ids), len(set(videos_ids))))
        data = {video_id: [] for video_id in videos_ids}
        for video_id in set(videos_ids):
            try:
                response = self.get(settings.API_URL.format(video_id), params={"fields": "sizes,active"}, timeout=10)
                if response.status_code == 200:
                    picture_links = parse_response(video_id, response)
                    data[video_id] = picture_links
                    self.links += 1
                else:
                    logger.error("Failed to get thumbup's link for video_id=%s - %s" % (video_id, response.text))
            except Exception as e:
                logger.error("Failed to get thumbup's link for video_id=%s - %s" % (video_id, e))
        logger.info("Found thumbups for %s/%s videos" % (self.links, len(set(videos_ids))))
        return data

    def download_thumbups(self, data):
        videos_with_thumbups = 0
        for video_id, links in data.items():
            files = 0
            for i, link in enumerate(links, 1):
                try:
                    response = self.get(link, stream=True)
                    if response.status_code == 200:
                        file_name = get_filename(video_id, i)
                        write_file(file_name, response)
                        self.files_saved += 1
                        files += 1
                    else:
                        logger.error('Failed to download thumbup for video %s - %s' % (video_id, response.text))
                except Exception as e:
                    logger.error('Failed to download thumbup for video %s - %s' % (video_id, e))
            if files > 0:
                videos_with_thumbups += 1
        logger.info('Downloaded %s files for %s/%s videos' % (self.files_saved, videos_with_thumbups, len(data)))
