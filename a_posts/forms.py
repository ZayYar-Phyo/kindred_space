from django.forms import ModelForm
from django import forms
from .models import Post, Review


# post creation form
class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'image', 'reason', 'body', 'tags', 'latitude', 'longitude', 'show_general_area_only', 'display_area']
        labels = {
            'body': 'キャプション',
            'tags': 'カテゴリー',
            'post_type': '',
            'reason': '',
            'image': '画像',
            'latitude': '緯度',
            'longitude': '経度',
            'show_general_area_only': '大まかな地域のみ表示',
            'display_area': '表示エリア',
        }
        widgets = {
            'post_type': forms.HiddenInput(),  # Hidden, controlled by toggle buttons
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'このアイテムについての思いやりのメッセージを記入してください...', 'class': 'font1 text-1xl'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'なぜこれを提供しますか？', 'class': 'font1 text-1xl'}),
            'tags': forms.CheckboxSelectMultiple(),
            'latitude': forms.NumberInput(attrs={'step': '0.000001', 'placeholder': '例: 35.681236', 'required': True}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001', 'placeholder': '例: 139.767125', 'required': True}),
            'display_area': forms.TextInput(attrs={'readonly': True, 'placeholder': '例: 大阪府 大阪市 北区'}),
        }

 
# post edit form       
class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'tags']
        labels = {
            'body': '',
            'tags': 'Categories',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3,  'class': 'font1 text-1xl'}),
            'tags': forms.CheckboxSelectMultiple(),
        }


# review submission form
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': '評価',
            'comment': 'コメント（任意）',
        }
        widgets = {
            'rating': forms.RadioSelect(choices=[(5, '⭐⭐⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (3, '⭐⭐⭐'), (2, '⭐⭐'), (1, '⭐')]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'このユーザーとの取引体験を教えてください...', 'class': 'w-full border rounded-lg p-3'}),
        }