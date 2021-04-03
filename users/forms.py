from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User

class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'username')

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'username')