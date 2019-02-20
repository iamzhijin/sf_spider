from django import forms
from .models import Crawls

class CrawlForm(forms.Form):
    crawl_name = forms.CharField(
        max_length=30,
        required = True,
        error_messsages={'max_length': '爬虫名称不可超过30个字符', 'required': '爬虫名称不可为空'}
    )

    code = forms.CharField(
        max_length=50,
        required=True,
        error_messages={'max_length': '爬虫编码不可超过50字符', 'required': '爬虫编码不可为空'}
    )

    # crawl_file = forms.FileField(
    #     required=True,
    #     error_messages={'required': '请上传爬虫文件'}
    # )

    source = forms.CharField(
        max_length=100,
        required=True,
        error_message={'max_length': '数据源字段不可超过100', 'required': '数据源字段不可为空'}
    )


class FielUploadModelForm(forms.ModelForm):
    class Meta:
        model = Crawls
