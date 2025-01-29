from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

CSS_CLASS = "w-full px-4 py-2 rounded-xl text-lg md:text-xl outline-none focus:ring-1 focus:ring-indigo-600 mb-6 block"


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # customize label here
        self.fields["username"].label = "Username :"
        self.fields["email"].label = "Email :"
        self.fields["password1"].label = "Password :"
        self.fields["password2"].label = "Confirm Password :"

        # add autocomplete
        self.fields["username"].widget.attrs["autocomplete"] = "username"

        # add placeholder
        self.fields["username"].widget.attrs["placeholder"] = "Enter User name ....."
        self.fields["email"].widget.attrs["placeholder"] = "Enter Your email here ....."
        self.fields["password1"].widget.attrs["placeholder"] = "Enter Your Password Here ...."
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Your Password ....."

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = CSS_CLASS


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # customize label here
        self.fields["username"].label = "Username :"
        self.fields["password"].label = "Password :"
        
        # add autocomplete
        self.fields["username"].widget.attrs["autocomplete"] = "username"

        # add placeholder
        self.fields["username"].widget.attrs["placeholder"] = "Enter User name ....."
        
        self.fields["password"].widget.attrs["placeholder"] = "Enter Your Password Here ...."

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = CSS_CLASS
