from io import BytesIO
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from config.config import config
from PIL import Image
import httpx


class ImageUploader:
    def __init__(self):
        self.type = config['conf']['upload']['type']
        if self.type == 'cos':
            cos_config = CosConfig(Region=config['conf']['upload']['cos']['region'],
                                   SecretId=config['conf']['upload']['cos']['secret_id'],
                                   SecretKey=config['conf']['upload']['cos']['secret_key'],
                                   Token=config['conf']['upload']['cos']['token'])
            self.client = CosS3Client(cos_config)

    def resize_img(self, img_content: bytes, width: int, height: int, filename, file_type):
        img = Image.open(BytesIO(img_content))
        out = img.resize((width, height), Image.ANTIALIAS)
        ouy_bytes = BytesIO()
        out.save(ouy_bytes, format=file_type)

        return self.upload_file(ouy_bytes.getvalue(), filename)

    def upload_file(self, file_content: bytes, filename):
        if self.type == 'cos':
            try:
                response = self.client.put_object(
                    Bucket=config['conf']['upload'][self.type]['bucket'],
                    Body=file_content,
                    Key=filename,
                    EnableMD5=False
                )
                return True
            except Exception:
                return False
        elif self.type == 'lsky':
            try:
                headers = {'Accept': 'application/json',
                           'Authorization': config['conf']['upload'][self.type]['authorization']}
                response = httpx.post(config['conf']['upload'][self.type]['host'] + 'upload', headers=headers,
                                      files={'file': (filename, file_content)}).json()
                return response['data']['links']['url'], response['data']['key']
            except Exception:
                return None

    def delete_file(self, keys: list) -> bool:
        if self.type == 'lsky':
            keys.remove('')
            for key in keys:
                try:
                    headers = {'Accept': 'application/json',
                               'Authorization': config['conf']['upload'][self.type]['authorization']}
                    response = httpx.delete(config['conf']['upload'][self.type]['host'] + 'images/{}'.format(key),
                                            headers=headers).json()
                    if response['status']:
                        continue
                    else:
                        return False
                except Exception:
                    return False
            return True

        pass
