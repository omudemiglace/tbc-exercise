from django.contrib import admin

from . import models

for model_name in models.__all__:
    model_class = getattr(models, model_name)

    if not admin.site.is_registered(model_class) and model_name != "BaseModel":
        admin.site.register(model_class)
