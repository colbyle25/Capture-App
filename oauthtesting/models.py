from django.db import models

# NOTE:
# You may need to run "pip install Pillow" for images to work
# https://djangocentral.com/uploading-images-with-django/

USERNAME_LENGTH = 64
BIOGRAPHY_LENGTH = 200

TEXT_LENGTH = 200  # Max text message length
COORDINATE_DECIMAL_PLACES = 6  # How many digits after the decimal place should longitude/latitude have?

IMAGE_FILE_LOCATION = 'images'
DRAWING_FILE_LOCATION = 'drawing'

DEFAULT_POINTS = 1  # How many points should a point of interest (POI) give?

# https://stackoverflow.com/questions/51570254/django-change-name-of-image-from-imagefield
# Referenced to figure out how to access the username (line 26 and method account_url)


def account_url(instance, image):
    filetype = image.split('.')[-1]
    return "{}/{}.{}".format(IMAGE_FILE_LOCATION, instance.username, filetype)


class Account(models.Model):
    # Main info
    username = models.CharField(max_length=USERNAME_LENGTH, unique=True, primary_key=True)
    points = models.IntegerField()

    # Optional
    bio = models.CharField(max_length=BIOGRAPHY_LENGTH)
    picture = models.ImageField(upload_to=account_url)

    def __str__(self):
        return self.username


class Friends(models.Model):
    user1 = models.ForeignKey(Account, related_name="user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(Account, related_name="user2", on_delete=models.CASCADE)

    # Primary Key
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user1', 'user2'], name='friend_key')]

    def __str__(self):
        return str(self.user1) + " is friends with " + str(self.user2)


# Point of Interest
class POI(models.Model):
    pid = models.IntegerField(primary_key=True)
    time = models.DateTimeField()
    points = models.IntegerField(default=DEFAULT_POINTS)
    longitude = models.DecimalField(max_digits=COORDINATE_DECIMAL_PLACES + 2,
                                    decimal_places=COORDINATE_DECIMAL_PLACES)
    latitude = models.DecimalField(max_digits=COORDINATE_DECIMAL_PLACES + 2,
                                   decimal_places=COORDINATE_DECIMAL_PLACES)

    def __str__(self):
        return "Point of Interest at " + str(self.longitude) + ", " + str(self.latitude) + " worth " + str(self.points)


class Captured(models.Model):
    pid = models.ForeignKey(POI, on_delete=models.CASCADE, primary_key=True)
    username = models.ForeignKey(Account, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.username) + " captured " + str(self.time)


class Message(models.Model):
    username = models.ForeignKey(Account, on_delete=models.CASCADE)
    time = models.DateTimeField()
    longitude = models.DecimalField(max_digits=COORDINATE_DECIMAL_PLACES + 2,
                                    decimal_places=COORDINATE_DECIMAL_PLACES)
    latitude = models.DecimalField(max_digits=COORDINATE_DECIMAL_PLACES + 2,
                                   decimal_places=COORDINATE_DECIMAL_PLACES)

    # Primary Key
    class Meta:
        constraints = [models.UniqueConstraint(fields=['username', 'time'], name='message_id')]


class TextMessage(Message):
    text = models.CharField(max_length=TEXT_LENGTH)

    def __str__(self):
        return str(self.username) + ": " + str(self.text)


class DrawingMessage(Message):
    data = models.FileField(upload_to=DRAWING_FILE_LOCATION)

    def __str__(self):
        return str(self.username) + ": " + str(self.data)


class Like(models.Model):
    poster = models.ForeignKey(Message, on_delete=models.CASCADE)
    liker = models.ForeignKey(Account, on_delete=models.CASCADE)
    time = models.DateTimeField()

    # Primary Key
    class Meta:
        constraints = [models.UniqueConstraint(fields=['poster', 'liker'], name='like_id')]

    def __str__(self):
        return str(self.liker) + " liked " + str(self.poster) + "'s post from " + str(self.time)
