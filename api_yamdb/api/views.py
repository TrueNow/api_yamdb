from django.shortcuts import get_object_or_404
from .serializers import ReviewSerializer, CommentSerializer
from reviews.models import Comment, Review, User, Title
from rest_framework.viewsets import ModelViewSet


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer


    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id),
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id),
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)
