from app.models import Document, Video, Comment
from PIL import ImageFilter
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=24)
    password = forms.CharField(widget=forms.PasswordInput())


class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'password1', 'password2', )


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('image', 'caption', 'topic')

    def __init__(self, posted_by=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.posted_by = posted_by

    def save(self):
        self.instance.posted_by = self.posted_by
        self.instance.save()


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('video', 'caption', 'posted_by')


class CommentForm(forms.Form):
    comment = forms.CharField()

    def __init__(self, document=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = document

    def save(self):
        return self.document.comment_set.create(
            comment=self.cleaned_data['comment'])


class CommentOnVideoForm(forms.Form):
    comment = forms.CharField()

    def __init__(self, video=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.video = video

    def save(self):
        return self.video.commentvid_set.create(
            comment=self.cleaned_data['comment'])


class FilterForm(forms.Form):
    options = [('', ''), ('Lettertext', 'Lettertext'), ('Andy', 'Andy Warhol'),
               ('Random', 'Random'), ('AKA', 'AKA'), ('Jo\'s Custom Filter',
                                                      'Jo\'s Custom Filter', ),
               ('Black&White', 'Black & White'), ('BLUR', 'Blur'), ('CONTOUR',
                                                                    'Contour'),
               ('DETAIL',
                'Detail'), ('EDGE_ENHANCE_MORE',
                            'Extra Edge-Enhance'), ('EMBOSS',
                                                    'Emboss'), ('FIND_EDGES',
                                                                'Find Edges'),
               ('SMOOTH_MORE',
                'Extra Smooth'), ('SHARPEN',
                                  'Sharpen'), ('ColorScale',
                                               'Color Scale'), ('Minimalist',
                                                                'Minimalist')]
    filters = forms.ChoiceField(choices=options)

    def get_filter(self):
        return {
            'Random': 'Random',
            'BLUR': ImageFilter.GaussianBlur(2),
            'CONTOUR': ImageFilter.CONTOUR,
            'EMBOSS': ImageFilter.EMBOSS,
            'DETAIL': ImageFilter.DETAIL,
            'EDGE_ENHANCE_MORE': ImageFilter.EDGE_ENHANCE_MORE,
            'FIND_EDGES': ImageFilter.FIND_EDGES,
            'SMOOTH_MORE': ImageFilter.SMOOTH_MORE,
            'SHARPEN': ImageFilter.SHARPEN,
            'Black&White': 'Black',
            'Jo\'s Custom Filter': 'Jofilt',
            'AKA': 'AKA',
            'Andy': 'Andy',
            'ColorScale': 'ColorScale',
            'Minimalist': 'Minimalist',
            'Lettertext': 'Lettertext',
        }.get(self.cleaned_data['filters'], None)
