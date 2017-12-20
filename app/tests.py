from django.test import TestCase
from django.urls import reverse
from app.models import Document, Video, Comment
from app.forms import CommentForm


# Create your tests here.
class TestCommentForm(TestCase):
    def test_save_creates_associated_comment(self):
        doc = Document.objects.create()

        form = CommentForm(doc, {'comment': 'Hello World'})
        form.full_clean()
        comment = form.save()

        self.assertEqual(doc.comment_set.count(), 1)
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertEqual(comment.document, doc)
