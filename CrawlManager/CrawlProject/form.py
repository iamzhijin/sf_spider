from django import forms

class ProjectForm(forms.Form):
    project_name = forms.CharField(
        max_length=30,
        required=True,
        error_messages={"required": "项目名称不可为空", "max_length": "项目名称最大名称为30"}
    )
    code = forms.CharField(
        max_length=10,
        required=True,
        error_messages={"required": "项目编码不可为空", "max_length": "项目编码最大名称为10"}
    )