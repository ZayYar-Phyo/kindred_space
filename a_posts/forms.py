from django.forms import ModelForm
from django import forms
from .models import Post, Review
from .prefectures import PREFECTURE_CHOICES


# post creation form
class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'title', 'reason', 'body', 'tags', 'prefecture', 'latitude', 'longitude', 'show_general_area_only', 'display_area']
        labels = {
            'title': 'タイトル',
            'body': 'キャプション',
            'tags': 'カテゴリー',
            'post_type': '',
            'reason': '',
            'prefecture': '都道府県',
            'latitude': '緯度',
            'longitude': '経度',
            'show_general_area_only': '大まかな地域のみ表示',
            'display_area': '市区町村・駅名など',
        }
        widgets = {
            'post_type': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'placeholder': 'タイトルを入力して下さい', 'class': 'w-full rounded-lg p-3 bg-[rgba(232,240,254,1)]', 'required': True}),
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'このアイテムについての思いやりのメッセージを記入してください...', 'class': 'font1 text-1xl'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'なぜこれを提供しますか？', 'class': 'font1 text-1xl'}),
            'tags': forms.CheckboxSelectMultiple(),
            'prefecture': forms.Select(attrs={'class': 'w-full rounded-lg p-3 bg-[rgba(232,240,254,1)] h-[3.3rem]'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'display_area': forms.TextInput(attrs={'placeholder': '市区町村、駅名などを入力 (例: 梅田駅)', 'class': 'w-full rounded-lg p-3 bg-[rgba(232,240,254,1)]', 'autocomplete': 'off'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['prefecture'].required = True
        self.fields['prefecture'].empty_label = '都道府県を選択してください'
    

 
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
            'title': forms.TextInput(attrs={'placeholder': 'タイトルを入力して下さい', 'class': 'w-full rounded-lg p-3 bg-[rgba(232,240,254,1)]', 'required': True}),
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