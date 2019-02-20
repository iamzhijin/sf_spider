from django import forms

class RegistForm(forms.Form):
    username = forms.CharField(
        error_messages={'required': u'用户名不可为空', 'max_length': u'用户名超过6位'}, 
        max_length=6
    )
    password = forms.CharField(
        error_messages={'required': u'密码不可为空', 'min_length': u'密码至少6位'},
        min_length=6
    )
    email = forms.EmailField(error_messages={'required': u'邮箱不可为空'})