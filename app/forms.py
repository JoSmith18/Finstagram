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
        self.document.comment_set.create(comment=self.cleaned_data['comment'])


class FilterForm(forms.Form):
    options = (('', ''), ('Black&White', 'Black&White'), ('BLUR', 'BLUR'),
               ('CONTOUR', 'CONTOUR'), ('DETAIL', 'DETAIL'),
               ('EDGE_ENHANCE_MORE',
                'EDGE_ENHANCE_MORE'), ('EMBOSS', 'EMBOSS'), ('FIND_EDGES',
                                                             'FIND_EDGES'),
               ('SMOOTH_MORE', 'SMOOTH_MORE'), ('SHARPEN', 'SHARPEN'))
    filters = forms.ChoiceField(choices=options)

    def get_filter(self):
        return {
            'BLUR': ImageFilter.GaussianBlur(2),
            'CONTOUR': ImageFilter.CONTOUR,
            'EMBOSS': ImageFilter.EMBOSS,
            'DETAIL': ImageFilter.DETAIL,
            'EDGE_ENHANCE_MORE': ImageFilter.EDGE_ENHANCE_MORE,
            'FIND_EDGES': ImageFilter.FIND_EDGES,
            'SMOOTH_MORE': ImageFilter.SMOOTH_MORE,
            'SHARPEN': ImageFilter.SHARPEN,
            'Black&White': 'Black'
        }.get(self.cleaned_data['filters'], None)
