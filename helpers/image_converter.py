from pathlib import Path
import secrets
import base64

PATH_OF_BACKEND = Path(__file__).parents[1].absolute()
ASSETS_PATH = Path(PATH_OF_BACKEND.absolute() / 'assets')


def generate_image_name():
    img_name = secrets.token_hex(32) + '.png'
    return img_name


def save_image(profile_image: str):
    img_bytes = base64.b64decode(profile_image)
    img_path = Path.joinpath(ASSETS_PATH, generate_image_name())
    with open(img_path, 'wb') as imgwriter:
        imgwriter.write(img_bytes)
    return img_path.as_posix()


if __name__ == '__main__':
    print(Path.joinpath(ASSETS_PATH, generate_image_name()).as_posix())
