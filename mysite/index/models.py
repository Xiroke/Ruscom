from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    

class GuidebookTopics(models.Model):
    name = models.CharField(max_length=255)
    subtopics = models.ForeignKey("self", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class TaskPage(Page):
    question = models.CharField(max_length=255, blank=True)
    answer = models.CharField(max_length=255, blank=True)
    # category = models.ManyToManyField(TaskCategory, related_name="tasks")

    content_panels = Page.content_panels + [
        FieldPanel('question'),
        FieldPanel('answer'),
        # FieldPanel('category'),
    ]


class DictionaryPage(Page):
    word = models.CharField(max_length=255, blank=True)
    image_word = models.ImageField(max_length=255, blank=True, upload_to='images/dictionary/')
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('image_word'),
        FieldPanel('word'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('word'),
    ]





class ArticleManyToMany(models.Model):
    category = models.ForeignKey("ArticleCategory", on_delete=models.CASCADE)
    arricle = models.ForeignKey("ArticlePage", on_delete=models.CASCADE)

class ArticleCategory(models.Model):
    name = models.TextField()

class ArticlePage(Page):
    date = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=True)
    views = models.IntegerField(default=0)
    category = models.ManyToManyField(ArticleCategory, through="ArticleManyToMany")
    
    search_fields = Page.search_fields + [
        index.SearchField('author'),
        index.SearchField('date'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('category'),
    ]
