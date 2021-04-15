from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    class PostManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status = "Published")

    
    options = (
        ("Draft","Draft"),
        ("Published", "Published")
    )

    Categories =(
        ("News", "News"),
        ("Politics", "Politics"),
        ("Education", "Education"),
        ("Blog", "Blog"),
        ("Article", "Article"),
        ("Entertainment", "Entertainment")
        )
    Campuses =(
        ("University", "University"),
        ("HTU", "HTU"),
        ("Legon", "Legon"),
        ("KNUST", "KNUST"),
        ("UCC", "UCC"),
        ("UHAS", "UHAS"),
        ("KTU", "KTU")
        )    
    def upload_location(instance, filename):
        return 'post/{filename}'.format(filename=filename)

    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='blog_post', default="1")
    subAuthor = models.CharField(max_length=50,default="Fuji")
    title = models.CharField(max_length=250)
    images = models.ImageField(_("Image"), upload_to=upload_location, blank=True,null=True)
    excerpt = models.TextField()
    content = models.TextField()
    slug = models.SlugField(max_length = 250, unique_for_date = "Published")
    Published = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=250,choices = options,default = "Published")
    category = models.CharField(max_length=50, choices = Categories, default = 'News')
    campus = models.CharField(max_length=50, choices = Campuses, default = 'University')
    featured = models.BooleanField(default= False)
    trending = models.BooleanField(default= False)
    objects = models.Manager() #default manager
    PostManager = PostManager()#custom manager

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.featured:
            try:
                temp= Post.objects.get(featured = True)
                if self !=temp:
                    featured = False
            except Post.DoesNotExist:
                pass
        super(Post, self).save(*args, **kwargs)
            
    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-Published",)

class Comment(models.Model):
    profile = models.ForeignKey("AllModels.Profile",on_delete=models.CASCADE,default="1")
    post = models.ForeignKey(Post, related_name= "comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    body = models.TextField()        
    comment_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default = True)

    def __str__(self):
        return self.body

class Profile(models.Model):
    prouser = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile/",default ="null")
    bio = models.TextField(blank=True,default ="null")
    interest = models.TextField(blank=True,default ="null")
    university = models.CharField(max_length=250,blank=True,default ="null")
    created = models.DateTimeField(auto_now=False, auto_now_add=True,blank=True)
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(prouser=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.prouser.username
        

