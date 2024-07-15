from django import forms

from .models import Users
from .models import Images
from .models import Containers
from .models import Databases


class UsersForm(forms.ModelForm):
    # due_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Users
        fields = ["user_name", "email"]


class ImagesForm(forms.ModelForm):
    tag = forms.CharField(initial="none")

    class Meta:
        model = Images
        fields = ["image_name", "tag"]


class ServersForm(forms.ModelForm):
    database_name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

    class Meta:
        model = Containers
        fields = ["container_name", "image", "port", "database_name", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the image field queryset to show images
        self.fields["image"].queryset = Images.objects.all()
        self.fields["image"].label_from_instance = (
            lambda obj: f"{obj.image_name} {obj.tag}"
        )

    def save(self, commit=True):
        container_instance = super().save(commit=False)
        database_name = self.cleaned_data["database_name"]

        # Save the container first
        if commit:
            container_instance.save()

        # Update or create the database entry
        database, created = Databases.objects.update_or_create(
            container=container_instance, defaults={"database_name": database_name}
        )

        return container_instance
