import re
from core.app import azure_ocr
from azure.ai.vision.imageanalysis.models import VisualFeatures


def ocr_placas(image):

    # Extract text (OCR) from an image stream. This will be a synchronously (blocking) call.
    result = azure_ocr.analyze(
        image_data=image,
        visual_features=[VisualFeatures.READ]
    )

    # Print text (OCR) analysis results to the console
    plate = ''
    if result.read is not None and len(result.read.blocks) > 0:
        for line in result.read.blocks[0].lines:
            print('LINE: ', line)
            if bool(re.search(r'\d', line.text)):
                plate = line.text.replace(' ', '')
                break

    return plate
