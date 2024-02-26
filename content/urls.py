from django.urls import path

from content.views import *

urlpatterns = [
    path('chapters/', get_chapters, name='get_chapters'),
    path('chapters/add/', add_chapter, name='add_chapter'),
    path('chapters/get/', list_chapters_with_details, name='list_chapters_with_details'),
    path('chapters/<int:chapter_id>/', get_chapter_by_id, name='get_chapter_by_id'),
    path('chapters/<int:chapter_id>/edit/', edit_chapter, name='edit_chapter'),
    path('chapters/<int:chapter_id>/delete/', delete_chapter, name='delete_chapter'),
    path('chapters/<int:chapter_id>/challenges/', get_chapter_with_challenges_by_id,
         name='get_chapter_with_challenges_by_id'),

    path('coding_challenges/add/', add_coding_challenge, name='add_coding_challenge'),
    path('coding_challenges/', get_coding_challenges, name='get_coding_challenges'),
    path('coding_challenges/<int:challenge_id>/', get_coding_challenge_by_id, name='get_coding_challenge_by_id'),
    path('coding_challenges/<int:challenge_id>/edit/', edit_coding_challenge, name='edit_coding_challenge'),
    path('coding_challenges/<int:challenge_id>/delete/', delete_coding_challenge, name='delete_coding_challenge'),

    path('courses/add_course/', add_course, name='add_course'),
    path('courses/update_course/<int:course_id>/', update_course, name='update_course'),
    path('courses/delete_course/<int:course_id>/', delete_course, name='delete_course'),
    path('courses/get_all_courses/', get_all_courses, name='get_all_courses'),
    path('courses/get_course_by_id/<int:course_id>/', get_course_by_id, name='get_course_by_id'),
]
