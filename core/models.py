import uuid
import os
from django.db import models
from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER, EMAIL_RECEIVER


def technology_file_path(instance, file_name):
    """Generate file path for new technology image"""
    ext = file_name.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/technology/', file_name)


class Technology(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to=technology_file_path,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


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
        try:
            if self.name['en'] and self.name['fr']:
                if len(self.name) != 2:
                    raise ValueError(error_name + " Found an extra field.")
                else:
                    if (not isinstance(self.name['en'], str)
                            or not isinstance(self.name['fr'], str)):
                        raise ValueError(
                            "'en' and 'fr' keys must be of type str."
                        )
            else:
                raise ValueError(error_name)
        except KeyError:
            raise ValueError(error_name)
        except TypeError:
            raise ValueError(error_name)

        # Description field
        error_description = ('Skill object description must be an'
                             + ' object with only the "en" and "fr" keys.')
        try:
            if self.description['en'] and self.description['fr']:
                if len(self.description) != 2:
                    raise ValueError(error_description +
                                     " Found an extra field.")
                else:
                    if (not isinstance(self.description['en'], str)
                            or not isinstance(self.description['fr'], str)):
                        raise ValueError(
                            "'en' and 'fr' keys must be of type str."
                        )
            else:
                raise ValueError(error_description)
        except KeyError:
            raise ValueError(error_description)
        except TypeError:
            raise ValueError(error_description)

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


class Review(models.Model):
    author = models.CharField(max_length=50)
    message = models.JSONField()
    update_code = models.CharField(max_length=50, blank=True)
    modified = models.BooleanField(default=False)

    def __str__(self):
        return self.message['en']

    def save(self, *args, **kwargs):
        error_message = ("Fail")
        try:
            if self.message['en'] and self.message['fr']:
                if len(self.message) != 2:
                    raise ValueError(error_message + " Found an extra field.")
                else:
                    if (not isinstance(self.message['en'], str)
                            or not isinstance(self.message['fr'], str)):
                        raise ValueError(
                            "'en' and 'fr' keys must be of type str."
                        )
            else:
                raise ValueError(error_message)
        except KeyError:
            raise ValueError(error_message)
        except TypeError:
            raise ValueError(error_message)

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
