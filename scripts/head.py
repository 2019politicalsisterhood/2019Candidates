from google_images_download import google_images_download
from political_sisterhood.candidate.models import Candidate
import logging
from django.core.files.base import ContentFile
from PIL import Image as PImage
from django.core.files import File
logger = logging.getLogger(__name__)
import os


def run():
    for candidate in Candidate.objects.filter(image=""):
        try:
            response = google_images_download.googleimagesdownload()
            absolute_image_paths = response.download({
                                                      "keywords": candidate.full_name,
                                                      "print_urls":True,
                                                      "limit": 1,
                                                    })
            for result, value in absolute_image_paths.items():
                if value:
                    f = open(value[0], 'rb')
                    img = File(f)
                    candidate.image.save(candidate.slug + '.jpg', img , save=True)
                    candidate.save()
        except Exception as e:
            logger.error(e)