from django.db import models


class Skill(models.Model):
    name = models.JSONField()
    description = models.JSONField()
    date = models.JSONField()

    def __str__(self):
        return self.name['en']

    def save(self, *args, **kwargs):
        error_name = 'Skill object name must be an object with only the "en" and "fr" keys.'
        try:
            if self.name['en'] and self.name['fr']:
                if len(self.name) != 2:
                    raise ValueError(error_name + " Found an extra field.")
            else:
                raise ValueError(error_name)
        except KeyError:
            raise ValueError(error_name)
        except TypeError:
            raise ValueError(error_name)

        error_description = 'Skill object description must be an object with only the "en" and "fr" keys.'
        try:
            if self.description['en'] and self.description['fr']:
                if len(self.description) != 2:
                    raise ValueError(error_description +
                                     " Found an extra field.")
            else:
                raise ValueError(error_description)
        except KeyError:
            raise ValueError(error_description)
        except TypeError:
            raise ValueError(error_description)

        super(Skill, self).save(*args, **kwargs)
