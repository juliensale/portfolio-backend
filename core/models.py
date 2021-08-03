import uuid
import os
from django.db import models
from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER, EMAIL_RECEIVER
from cloudinary.models import CloudinaryField

from django.dispatch import receiver
from django.db.models.signals import pre_delete
import cloudinary


def technology_file_path(instance, file_name):
    """Generate file path for new technology image"""
    ext = file_name.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/technology/', file_name)


def check_translated_field(field, error_message=''):

    try:
        if field['en'] and field['fr']:
            if len(field) != 2:
                raise ValueError(error_message + " Found an extra field.")
            else:
                if (not isinstance(field['en'], str)
                        or not isinstance(field['fr'], str)):
                    raise ValueError(
                        error_message + "'en' and 'fr' keys must"
                        + " be of type str."
                    )
        else:
            raise ValueError(error_message)
    except KeyError:
        raise ValueError(error_message)
    except TypeError:
        raise ValueError(error_message)


def check_translated_MDX_field(field, error_message=''):
    try:
        if field['en'] and field['fr']:
            if len(field) != 2:
                raise ValueError(error_message + " Found an extra field.")
            else:
                if (not isinstance(field['en'], list)
                        or not isinstance(field['fr'], list)):
                    raise ValueError(
                        error_message + "'en' and 'fr' keys must"
                        + " be of type list."
                    )
                else:
                    for line in field['en']:
                        if not isinstance(line, str):
                            raise ValueError(
                                error_message + "'en' key entries "
                                + "must be strings"
                            )
                    for line in field['fr']:
                        if not isinstance(line, str):
                            raise ValueError(
                                error_message + "'fr' key entries"
                                + " must be strings"
                            )
        else:
            raise ValueError(error_message)
    except KeyError:
        raise ValueError(error_message)
    except TypeError:
        raise ValueError(error_message)


class Technology(models.Model):
    name = models.CharField(max_length=50)
    image = CloudinaryField('image')

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=Technology)
def technology_photo_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)


class Skill(models.Model):
    name = models.JSONField()
    description = models.JSONField()
    date = models.JSONField()
    technology = models.ForeignKey(
        Technology,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.name['en']

    def save(self, *args, **kwargs):
        # Name field
        error_name = ('Skill object name must be an'
                      + ' object with only the "en" and "fr" keys.')
        check_translated_field(self.name, error_name)

        # Description field
        error_description = ('Skill object description must be an'
                             + ' object with only the "en" and "fr" keys.')
        check_translated_MDX_field(self.description, error_description)

        # Date field
        if not isinstance(self.date, list):
            raise ValueError('Skill date must be a list.')
        elif len(self.date) != 2:
            raise ValueError('Skill date must be of length 2')
        elif (not isinstance(self.date[0], int)
              or not isinstance(self.date[1], int)):
            raise ValueError('Month and year must be integers.')
        else:
            if self.date[0] < 1 or self.date[0] > 12:
                raise ValueError('Month must be in [1, 12].')
            if self.date[1] < 2000 or self.date[1] > 2100:
                raise ValueError('Year must be in [2000, 2100]')

        super(Skill, self).save(*args, **kwargs)


class Project(models.Model):
    name = models.JSONField()
    description = models.JSONField()
    image = CloudinaryField('image', blank=True, null=True)
    github = models.URLField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    client = models.CharField(max_length=100, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)

    def __str__(self):
        return self.name['en']

    def save(self, *args, **kwargs):
        check_translated_field(self.name, "Project name error: wrong typing.")
        check_translated_MDX_field(
            self.description, "Project description error: wrong typing.")
        is_creating = self.pk is None
        super(Project, self).save(*args, **kwargs)
        if is_creating:
            Review.objects.create(
                author=self.client,
                message="",
                project=self
            )


@receiver(pre_delete, sender=Project)
def project_photo_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)


class Review(models.Model):
    author = models.CharField(max_length=50, blank=True, default="")
    message = models.TextField(blank=True, default="")
    update_code = models.CharField(max_length=50, blank=True)
    modified = models.BooleanField(default=False)
    project = models.OneToOneField(
        Project, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.update_code = str(uuid.uuid4())
            send_mail(
                '[Portfolio]: New Review Code',
                f'The code is: {self.update_code}',
                EMAIL_HOST_USER,
                (EMAIL_RECEIVER,),
                fail_silently=False
            )
        else:
            self.modified = True
        super(Review, self).save(*args, **kwargs)
