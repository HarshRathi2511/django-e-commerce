
from allauth.account.forms import SignupForm,LoginForm
from user.models import Profile, UserDetail
class MyCustomSignupForm(SignupForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)
        UserDetail.objects.create(user=user)
        Profile.objects.create(user=user)
        # Add your own processing here.

        # You must return the original result.
        return user

class MyCustomLoginForm(LoginForm):

    def login(self, *args, **kwargs):

        # Add your own processing here.
        UserDetail.objects.create(user=self.user)
        Profile.objects.create(user=self.user)
        # You must return the original result.
        return super(MyCustomLoginForm, self).login(*args, **kwargs)