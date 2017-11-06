from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#Clase base para usuario
class MyUserManager(BaseUserManager):

     def create_user(self, username, password=None):
         if not username:
             raise ValueError('Es necesario tener un nombre de usuario')
         user = self.model(username=username,)
         user.set_password(password)
         user.save(using=self._db)
         return user

     def create_superuser(self, username, password):
         user = self.create_user(username,password=password,)
         user.is_admin = True
         user.save(using=self._db)
         return user

class ManagerUser(models.Model):
     user = models.ForeignKey('NormalUser',  null=True, blank = True)
     org_name = models.CharField(verbose_name = 'Name of the org', max_length = 50)

     class Meta:
         verbose_name        = 'Organization'
         verbose_name_plural = 'Organizations'

     def __str__(self):
         return "%s(%s)" % (self.org_name ,self.user)


class NormalUser(AbstractBaseUser):

     email = models.EmailField(verbose_name='email', max_length=255, unique=True)
     username = models.CharField(verbose_name = 'Nombre de usuario', max_length = 50, unique = True)
     manager = models.ForeignKey(ManagerUser, verbose_name = 'Manager', null=True, blank = True)
     created = models.DateTimeField(verbose_name = 'Creado', editable = False, auto_now_add = True)
     modified = models.DateTimeField(verbose_name = 'Actualizado', editable = False, auto_now = True)
     is_active = models.BooleanField(verbose_name = 'Activo',default=True)
     is_admin = models.BooleanField(verbose_name = 'Administrador', default=False)

     objects = MyUserManager()
     USERNAME_FIELD = 'username'
     REQUIRED_FIELDS = []
     class Meta:
         verbose_name        = 'User'
         verbose_name_plural = 'Users'

     @property
     def is_superuser(self):
         return self.is_admin


     @property
     def is_staff(self):
         return self.is_admin
