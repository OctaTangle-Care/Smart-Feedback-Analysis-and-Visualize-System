# from django.apps import AppConfig


# class SfasAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'sfas_app'



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
        


from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


class SfasAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sfas_app'

    def ready(self):
        from .models import ProductCategory
        try:
            if not ProductCategory.objects.exists():
                ProductCategory.objects.bulk_create([
                    ProductCategory(category_name='Laptop'),
                    ProductCategory(category_name='Electronics'),
                    ProductCategory(category_name='Home Appliances'),
                    ProductCategory(category_name='Toys'),
                    ProductCategory(category_name='Jewelry'),
                    ProductCategory(category_name='Clothing'),
                    ProductCategory(category_name='Home & Kitchen'),
                    ProductCategory(category_name='Books'),
                    ProductCategory(category_name='Sports & Outdoors'),
                    ProductCategory(category_name='Other'),
                ])
        except (OperationalError, ProgrammingError):
            # Happens during initial migrations when the table doesn't exist yet
            pass
