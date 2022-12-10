# from turtle import title
# from venv import create
from django.db import models

# Create your models here.
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='departname', 
        max_length=32)
    def __str__(self):
        return self.title

class Personnel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='姓名', max_length=16)
    pwd = models.CharField(verbose_name='密码', max_length=16)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', 
        max_digits=10, decimal_places=2)
    create_time = models.DateTimeField(verbose_name='创建日期')
    depart = models.ForeignKey(verbose_name='所属部门', 
        to='Department', to_field='id', on_delete=models.CASCADE)

class Admin(models.Model):
    unm = models.CharField(verbose_name="用户名", max_length=16)
    pwd = models.CharField(verbose_name="密码", max_length=16)
    def __str__(self):
        return self.unm