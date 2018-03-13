from utils import configure_logging
from v1meo import Vimeo
import sys

configure_logging()

if len(sys.argv[1:]) > 0:
    video_ids = sys.argv[1:]
else:
    video_ids = [257287904, 174711575, 253228558]  # put video_ids here or pass them in the command line

client = Vimeo()
data = client.get_data(video_ids)
client.download_thumbups(data)
