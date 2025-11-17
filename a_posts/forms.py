from django.forms import ModelForm
from django import forms
from .models import Post, Review


# post creation form
class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'title', 'image', 'reason', 'body', 'tags', 'latitude', 'longitude', 'show_general_area_only', 'display_area']
        labels = {
            'title': 'タイトル',
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
            'title': forms.TextInput(attrs={'placeholder': '例: 自転車を譲ります、英語レッスン募集中', 'class': 'w-full rounded-lg p-3 bg-[rgba(232,240,254,1)]', 'required': True}),
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'このアイテムについての思いやりのメッセージを記入してください...', 'class': 'font1 text-1xl'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'なぜこれを提供しますか？', 'class': 'font1 text-1xl'}),
            'tags': forms.CheckboxSelectMultiple(),
            'latitude': forms.NumberInput(attrs={'step': '0.000001', 'placeholder': '例: 35.681236', 'required': True}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001', 'placeholder': '例: 139.767125', 'required': True}),
            'display_area': forms.TextInput(attrs={'readonly': True, 'placeholder': '例: 大阪府 大阪市 北区'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True

 
# post edit form       
class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'tags']
        labels = {
            'title': 'タイトル',
            'body': 'キャプション',
            'tags': 'カテゴリー',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '例: 自転車を譲ります、英語レッスン募集中', 'class': 'w-full rounded-lg p-3 bg-[rgba(232,240,254,1)]', 'required': True}),
            'body': forms.Textarea(attrs={'rows': 3,  'class': 'font1 text-1xl'}),
            'tags': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True


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