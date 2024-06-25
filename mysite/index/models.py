from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index

from polymorphic.models import PolymorphicModel

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
  
  
class GuidebookTopicsModel(models.Model):
  name = models.CharField(max_length=255)
  child = models.ManyToManyField("self", blank=True, symmetrical=False)
  guidebook_item = models.ManyToManyField('GuidebookItemModel', blank=True)

  def __str__(self):
    return self.name
    
class GuidebookItemModel(PolymorphicModel):
  title = models.CharField(max_length=255, default='Без названия')
  author = models.ForeignKey('User', on_delete=models.CASCADE)
  
  def __str__(self):
    return self.title
  

class TaskSimpleModel(GuidebookItemModel):
  """The class Task"""
  question = models.TextField(blank=True)
  answer = models.TextField(blank=True)
  category = models.ManyToManyField('TaskCategoryModel', related_name="tasks")

  def __repr__(self):
    return f'<TaskSimple>'
  
class TaskDifficultАrchitectureModel(GuidebookItemModel):
  """The class consists of TaskSimple"""
  task_simple = models.ManyToManyField('TaskSimpleModel', blank=True)
  category = models.ManyToManyField('TaskCategoryModel', related_name="tasksDifficultArchitectureModel")

  def __repr__(self):
    return f'<TaskDifficultАrchitectureModel>'
  
class TheoryModel(GuidebookItemModel):
  information = models.TextField(blank=True)
  category = models.ManyToManyField('TaskCategoryModel', related_name="theory")

  def __repr__(self):
    return f'<Theory>'
  
class TaskCategoryModel(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name
  
class TaskCompletedModel(models.Model):
  user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
  task = models.ForeignKey('TaskSimpleModel', on_delete=models.CASCADE, blank=True, null=True)
  completed = models.BooleanField(default=False)

class DictionaryModel(models.Model):
  word = models.CharField(max_length=255, default='Без названия')
  information = models.TextField(default='Информация отсутсвует')

