from io import BytesIO
from PIL import Image


# Argument : bytes of an image
# Return: bytes of image
def resize_image(data):
    im = Image.open(BytesIO(data))
    image_type = im.format
    width, height = im.size
    # Shrink size to 50%
    new_size = int(width / 2), int(height / 2)
    new_im = im.resize(new_size)
    bio = BytesIO()
    # Save image instance to BytesIO object
    new_im.save(bio, image_type)
    # Get bytes of BytesIO object and return
    return bio.getvalue()


def compute_score(scores):
    WEIGHT = 100
    for k, v in scores.items():
        scores[k] = "{0:.2f}".format(v * WEIGHT)
    return scores


def best_match(scores):
    temp = [(k, v) for k, v in scores.items() if v == max(scores.values())]
    return temp[0][0], temp[0][1]
