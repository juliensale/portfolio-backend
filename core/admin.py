from django.contrib import admin
from core.models import Review, Technology, Project


class ReviewAdmin(admin.ModelAdmin):
    pass


class TechnologyAdmin(admin.ModelAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Review, ReviewAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Project, ProjectAdmin)
