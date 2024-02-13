from django.urls import path

from content.views import *

urlpatterns = [
    path('chapters/', get_chapters, name='get_chapters'),
    path('chapters/add/', add_chapter, name='add_chapter'),
    path('chapters/get/', list_chapters_with_details, name='list_chapters_with_details'),
    path('chapters/<int:chapter_id>/', get_chapter_by_id, name='get_chapter_by_id'),
    path('chapters/<int:chapter_id>/edit/', edit_chapter, name='edit_chapter'),
    path('chapters/<int:chapter_id>/delete/', delete_chapter, name='delete_chapter'),

    path('coding_challenges/add/', add_coding_challenge, name='add_coding_challenge'),
    path('coding_challenges/', get_coding_challenges, name='get_coding_challenges'),
    path('coding_challenges/<int:challenge_id>/', get_coding_challenge_by_id, name='get_coding_challenge_by_id'),
    path('coding_challenges/<int:challenge_id>/edit/', edit_coding_challenge, name='edit_coding_challenge'),
    path('coding_challenges/<int:challenge_id>/delete/', delete_coding_challenge, name='delete_coding_challenge'),
]