from rest_framework import generics,viewsets,filters,status,permissions
from AllModels.models import Post,Comment
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from django.http import HttpResponse
from rest_framework.views import APIView



class PostList(viewsets.ModelViewSet):
    queryset = Post.PostManager.order_by("-Published")
    serializer_class = PostSerializer

class CreatePost(viewsets.ModelViewSet):
    queryset = Post.PostManager.all()
    parser_classes  = [MultiPartParser,FormParser]
    serializer_class = PostSerializer
    permisssion_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ] 
   

    def post(self, request, format=None):
        title = request.data["title"]
        content = request.data["content"]
        excerpt = request.data["excerpt"]
        campus = request.data["campus"]
        category = request.data["category"]
        images = request.data["images"]
        subAuthor = request.data["subAuthor"]
        Post.objects.create(status=status, subAuthor=subAuthor, title=title, excerpt=excerpt,
         content=content, category=category, campus=campus, images=images)
        return HttpResponse({"message": "post created successfully"}, status=200)



class PostDetail(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostFeatured(viewsets.ModelViewSet):
    queryset = Post.PostManager.all().filter(featured=True)
    serializer_class = PostSerializer


class PostCategory(APIView):
    serializer_class = PostSerializer
    # permission_classes = (permissions.AllowAny,)
    
    def post(self,request,format= None,):
        data = self.request.data
        print(data)
        category = data['categorys']
        queryset = Post.PostManager.order_by('-Published').filter(category__iexact=category)

        serializer = PostSerializer(queryset,many = True)
        return Response(serializer.data)
        
class PostTrending(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.PostManager.all().filter(trending=True)

class PostListSearch(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    # '^' Starts-with search.
    # '=' Exact matches.
    search_fields = ['slug']

class Comments(generics.ListAPIView):
    serializer_class = CommentSerializer
   

    def get_queryset(self, *args, **kwargs):
        item = self.kwargs.get('pk')
        post = get_object_or_404(Post,id=item,status = "Published")
        comment = post.comments.filter(status=True)
        return comment

    @classmethod
    def get_extra_actions(*args, **kwargs):
        return []
        


class postComment(viewsets.ModelViewSet):
    queryset = Comment.objects.none()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticated,]

    



#   def get_object(self, queryset=None, **kwargs):
#         item = self.kwargs.get('pk')
#         post = get_object_or_404(Post, id=item)
#         comments = post.comment.filter(item=item)
#         return comments

    # def get_queryset(self, *args, **kwargs):
    #     # pk = self.kwargs.get(self.lookup_url_kwarg)
    #     post = get_object_or_404(Post,slug=self.kwargs["slug"])
    #     comments = post.comments.all()
    #     return comments

    
    
 
 
 
    # def get_object(self, queryset=None, **kwargs):
    #     item = self.kwargs.get('pk')
    #     if item is not None:
    #         items = (int(id) for id in item.split(','))
    #         return Comment.objects.filter(post=str(items))
    #     else:
    #         queryset = Comment.objects.all()
            


# def get_object(self, queryset=None, **kwargs):
#         item = self.kwargs.get('pk')
#         return get_object_or_404( Comment, post=item)
    # def get_queryset(self):
    #     pid = self.kwargs.get(self.lookup_url_kwarg)
    #     return Comment.objects.filter(pid)
    
    # def get_queryset(self, *args, **kwargs):
    #     pid = self.kwargs.get(self.lookup_url_kwarg)
    #     # postobj = get_object_or_404(Post,id=id)
    #     comments = Comment.objects.filter(pid=pid)
    #     return comments
    

