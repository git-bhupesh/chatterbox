from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image']
        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': "What's on your mind?",
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Write a comment...',
                'class': 'form-control form-control-sm',
            }),
        }