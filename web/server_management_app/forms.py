from django import forms
from .models import Users
from .models import Images
from .models import Containers


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
    class Meta:
        model = Containers
        fields = ["container_name", "image", "port"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the image field queryset to show images
        self.fields["image"].queryset = Images.objects.all()
        self.fields["image"].label_from_instance = (
            lambda obj: f"{obj.image_name} {obj.tag}"
        )
