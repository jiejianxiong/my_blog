from django import forms
from django.contrib.auth.models import User
from .models import Profile

# 登录表单
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 注册用户表单
class UserRegisterForm(forms.ModelForm):
    # 复写user的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username','email')

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致，请重试')
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone','avatar','bio')
