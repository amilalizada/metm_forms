from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe
import json
# Create your models here.
class Forms(models.Model):

    name = models.CharField('Name',max_length=1024)
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Forma")
        verbose_name_plural = ("Formalar")

    def __str__(self):
        return self.name

        

class Fields(models.Model):
    form = models.ForeignKey(Forms,on_delete=models.CASCADE, db_index=True, related_name='form_relation')
    field_choices = [
        ('1', 'text'),
        ('2', 'integer'),
        ('3', 'datetime'),
        ('4', 'date'),
        ('5', 'textarea'),
        ('6', 'email'),
        ('7', 'select'),

    ]
    label = models.CharField('Label', max_length=256)
    types = models.CharField('Tipler',max_length=50, choices=field_choices)
    default_value = models.CharField('Default Value', max_length=256, blank=True , null=True)
    requirement = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Fields")
        verbose_name_plural = ("Fields")

    def __str__(self):
        return self.label

    def get_type(self):
        return self.types

class Values(models.Model):
    fields = models.ForeignKey(Fields,on_delete=models.CASCADE, db_index=True, related_name='field_relation')
    value = models.TextField(max_length=1000)

    class Meta:
        verbose_name = ("Deyer")
        verbose_name_plural = ("Deyerler")

class Types(models.Model):
    #informations
    types = models.CharField('Adı',max_length=20)

    # moderations
    is_published = models.BooleanField('is published', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tag'

    def __str__(self):
        return self.tag_name

class Emails(models.Model):
    #informations
    forms = models.ForeignKey(Forms,on_delete=models.CASCADE, db_index=True, related_name='email_relation')
    email = models.CharField('Email',max_length=100)
    # moderations
    is_published = models.BooleanField('is published', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'email'
        verbose_name_plural = 'emails'

    def __str__(self):
        return self.email

class SecondValues(models.Model):
    forms = models.ForeignKey(Forms, verbose_name='Forms', on_delete=models.CASCADE,blank= True,null=True, related_name = 'list_of_value')

    datas = models.CharField('Datalar', max_length=1000)

    
class Question(models.Model):
    type_choise =  [
        ('1', 'Test'),
        ('2', 'Video'),
        ('3', ' Voice Record'),
        ('4', ' Text'),
    ]
    title = models.CharField('Title',max_length=50)
    description = models.TextField('Description')
    correct_answer = models.CharField('Correct answer',max_length=125)
    
    type = models.CharField('Tipler',max_length=50, choices=type_choise)
    
    is_auto = models.BooleanField('Is aouto', default=1)
    # subject = models.ForeignKey()

    class Meta():
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        # ordering = ('-created_at', '-title')

    def __str__(self):
        return f"{self.title}" 