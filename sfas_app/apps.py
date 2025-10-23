from django.apps import AppConfig


class SfasAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sfas_app'



# from django.apps import AppConfig
# from django.db.utils import OperationalError, ProgrammingError

# class SfasAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'sfas_app'

#     def ready(self):
#         from .models import Categories
#         try:
#             if not Categories.objects.exists():
#                 Categories.objects.bulk_create([
#                     Categories(name='Product', description='Physical or digital goods'),
#                     Categories(name='Service', description='Provided services or labor'),
#                     Categories(name='Other', description='Miscellaneous or uncategorized'),
#                 ])
#         except (OperationalError, ProgrammingError):
#             # Happens during initial migration when table doesn't exist yet
#             pass