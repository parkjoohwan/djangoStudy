from django import forms

class ImageForm(forms.Form):
    imagefile = forms.FileField(
        label = '파일을 선택하세요',
        help_text = '최대 42MB 까지 업로드 가능합니다.'
    )