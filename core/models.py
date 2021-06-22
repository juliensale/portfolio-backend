from django.db import models


class Skill(models.Model):
    name = models.JSONField()
    description = models.JSONField()
    date = models.JSONField()

    def __str__(self):
        return self.name['en']

    def save(self, *args, **kwargs):
        error_message = 'Skill object name must be an object with only the "en" and "fr" keys.'
        try:
            if self.name['en'] and self.name['fr']:
                if len(self.name) == 2:
                    super(Skill, self).save(*args, **kwargs)
                else:
                    raise ValueError(error_message + " Found an extra field.")
            else:
                raise ValueError(error_message)
        except KeyError:
            raise ValueError(error_message)
