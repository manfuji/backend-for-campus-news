from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import PostDetail, PostList, Comments, postComment, PostListSearch, CreatePost, PostFeatured, PostCategory,PostTrending
app_name = 'Post'


router = routers.DefaultRouter()
router.register('detail', PostDetail, 'details'),
router.register('post', PostList, 'postlist'),
router.register('createpost', CreatePost, 'createpost'),
router.register('postcomment', postComment, 'postcomment'),
router.register('search', PostListSearch, 'search'),
router.register('featured', PostFeatured, 'featured'),
router.register('trending', PostTrending, 'trending'),

urlpatterns = [
 path('comments/<int:pk>/', Comments.as_view(), name="comment"),
 path('category',PostCategory.as_view(),name="category"),
#  path('api/createposts',CreatePost.as_view(),name= "createpost"),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += router.urls
# urlpatterns 

















# urlpatterns = [
#     path("api/detail/<int:pk>/",PostDetail.as_view(),name="postview"),
#     path("api/post",PostList.as_view(), name = "postlist"),
#     path('api/comments',Comments.as_view(), name = "comment"),
#     path('api/postcomment/<int:post>/',postComment.as_view(), name = "postcomment"),


# ]