from utils import configure_logging
from v1meo import Vimeo

configure_logging()

video_ids = [259651498]

client = Vimeo()
data = client.get_data(video_ids)
client.download_thumbups(data)
