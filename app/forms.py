from django import forms
from app.models import Document, Video, Comment
from PIL import ImageFilter


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('image', 'caption', 'posted_by')


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
    options = [
        ('', ''),
        ('Lettertext','Lettertext'),
        ('Andy', 'Andy Warhol'),
        ('Random', 'Random'),
        ('AKA', 'AKA'),
        ('Jo\'s Custom Filter', 'Jo\'s Custom Filter', ),
        ('Black&White', 'Black & White'),
        ('BLUR', 'Blur'),
        ('CONTOUR', 'Contour'),
        ('DETAIL', 'Detail'),
        ('EDGE_ENHANCE_MORE', 'Extra Edge-Enhance'),
        ('EMBOSS', 'Emboss'),
        ('FIND_EDGES', 'Find Edges'),
        ('SMOOTH_MORE', 'Extra Smooth'),
        ('SHARPEN', 'Sharpen'),
        ('ColorScale', 'Color Scale'),
        ('Minimalist', 'Minimalist')
    ]
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
