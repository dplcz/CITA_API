from io import BytesIO
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from config.config import config
from PIL import Image

cos_config = CosConfig(Region=config['upload.conf']['region'], SecretId=config['upload.conf']['secret_id'],
                       SecretKey=config['upload.conf']['secret_key'], Token=config['upload.conf']['token'])
client = CosS3Client(cos_config)


def resize_img(img_content: bytes, width: int, height: int, filename, file_type) -> bool:
    img = Image.open(BytesIO(img_content))
    out = img.resize((width, height), Image.ANTIALIAS)
    ouy_bytes = BytesIO()
    out.save(ouy_bytes, format=file_type)

    return upload_file(ouy_bytes.getvalue(), filename)


def upload_file(file_content: bytes, filename) -> bool:
    try:
        response = client.put_object(
            Bucket=config['upload.conf']['bucket'],
            Body=file_content,
            Key=filename,
            EnableMD5=False
        )
        return True
    except Exception:
        return False
