from django.db import models


class Skill(models.Model):
    name = models.JSONField()
    description = models.JSONField()
    date = models.JSONField()

    def __str__(self):
        return self.name['en']

    def save(self, *args, **kwargs):
        # Name field
        error_name = 'Skill object name must be an object with only the "en" and "fr" keys.'
        try:
            if self.name['en'] and self.name['fr']:
                if len(self.name) != 2:
                    raise ValueError(error_name + " Found an extra field.")
                else:
                    if not isinstance(self.name['en'], str) or not isinstance(self.name['fr'], str):
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
        error_description = 'Skill object description must be an object with only the "en" and "fr" keys.'
        try:
            if self.description['en'] and self.description['fr']:
                if len(self.description) != 2:
                    raise ValueError(error_description +
                                     " Found an extra field.")
                else:
                    if not isinstance(self.description['en'], str) or not isinstance(self.description['fr'], str):
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
        elif not isinstance(self.date[0], int) or not isinstance(self.date[1], int):
            raise ValueError('Month and year must be integers.')
        else:
            if self.date[0] < 1 or self.date[0] > 12:
                raise ValueError('Month must be in [1, 12].')
            if self.date[1] < 2000 or self.date[1] > 2100:
                raise ValueError('Year must be in [2000, 2100]')

        super(Skill, self).save(*args, **kwargs)


class Technology(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
