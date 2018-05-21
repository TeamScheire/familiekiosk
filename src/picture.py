import os
from PIL import Image

class Picture():
    def __init__(self, file_path, quality=20):
        self.file_path = file_path
        self.compressed_file_path = self.file_path.replace(".jpg", "_comp.jpg")
        self.quality = quality

    def load(self):
        self.img = Image.open(open(self.file_path, "rb"))

    def compress(self):
        if os.path.isfile(self.compressed_file_path):
            os.remove(self.compressed_file_path)
        else:
            self.img.save(self.compressed_file_path, 'JPEG', 
                          subsampling=0, quality=self.quality)

    def remove(self):
        try:
            os.remove(self.file_path)
            os.remove(self.compressed_file_path)
        except:
            pass
