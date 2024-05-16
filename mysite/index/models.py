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
  is_verified = models.BooleanField(default=False)
  score = models.IntegerField(default=0)
  
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
  child = models.ManyToManyField("self", blank=True, symmetrical=False)
  url = models.URLField(max_length=255, blank=True)
  theory_pack = models.ManyToManyField('Theory', blank=True)
  task_pack = models.ManyToManyField('TaskSimple', blank=True)
  

  def __str__(self):
    return self.name
    
class PageTaskTheoryOther(models.Model):
  title = models.CharField(max_length=255, default='Без названия')
  author = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
  
  def __str__(self):
    return self.title
  
  class Meta:
    abstract = True

class TaskSimple(PageTaskTheoryOther):
  question = models.TextField(blank=True)
  answer = models.TextField(blank=True)
  category = models.ManyToManyField('TaskCategory', related_name="tasks", blank=True)

  
class Theory(PageTaskTheoryOther):
  information = models.TextField(blank=True)
  category = models.ManyToManyField('TaskCategory', related_name="theory", blank=True)

  
class TaskCategory(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name
  
class TaskCompleted(models.Model):
  user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
  task = models.ForeignKey('TaskSimple', on_delete=models.CASCADE, blank=True, null=True)
  completed = models.BooleanField(default=False)

class DictionaryPage(Page):
  word = models.TextField(blank=True)
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

