from django.db import models

# NOTE:
# You may need to run "pip install Pillow" for images to work
# https://djangocentral.com/uploading-images-with-django/

USERNAME_LENGTH = 64
BIOGRAPHY_LENGTH = 200
IMAGE_FILE_LOCATION = 'images'


# https://stackoverflow.com/questions/51570254/django-change-name-of-image-from-imagefield
# Referenced to figure out how to access the username (line 26 and method account_url)

def account_url(instance, image):
  filetype = image.split('.')[1]
  return "{}/{}.{}".format(IMAGE_FILE_LOCATION, instance.username, filetype)

class Account(models.Model):
  # Main info
  username = models.CharField(max_length=USERNAME_LENGTH)
  points = models.IntegerField()

  # Optional
  bio = models.CharField(max_length=BIOGRAPHY_LENGTH)
  picture = models.ImageField(upload_to=account_url)

  def __str__(self):
    return self.username
