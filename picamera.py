from picamera2 import Picamera2, Preview
import time
from libcamera import Transform 

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (1024, 768)},
											 transform=Transform(vflip=True))
picam2.configure(config)
#picam2.start_preview(Preview.QTGL)
picam2.start_preview(Preview.DRM)

picam2.start()
time.sleep(2)

picam2.capture_file("test.jpg")

