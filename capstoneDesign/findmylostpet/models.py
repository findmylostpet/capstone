from django.db import models
from accounts.models import Profile
from django.contrib.auth.models import User

# Create your models here.

class Member(models.Model):
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

class LostNotice(models.Model):
    Title=models.CharField(max_length=20,null=True)
    State=models.CharField(max_length=20,null=True)#실종1 연락중2 완료3
    PubDate=models.DateTimeField()
    MissingDate=models.DateTimeField()
    Text=models.TextField()
    Phone=models.CharField(max_length=20,null=True)
    Author=models.ForeignKey(User, on_delete = models.CASCADE,null=True)
    Gratuity=models.IntegerField(null=True)

    Si=models.CharField(max_length=20,null=True)
    Gu=models.CharField(max_length=20,null=True)
    Dong=models.CharField(max_length=20,null=True)
    
class FindNotice(models.Model):
    Title=models.CharField(max_length=20,null=True)
    State=models.CharField(max_length=20,null=True)#실종1 연락중2 완료3
    PubDate=models.DateTimeField()
    MissingDate=models.DateTimeField()
    Text=models.TextField()
    Phone=models.CharField(max_length=20,null=True)
    Author=models.ForeignKey(User, on_delete = models.CASCADE,null=True)

    Si=models.CharField(max_length=20,null=True)
    Gu=models.CharField(max_length=20,null=True)
    Dong=models.CharField(max_length=20,null=True)

    def Text_summary(self):
        return self.Text[:10]
    
class Dog(models.Model): 
    Name=models.CharField(max_length=20)
    Breed=models.CharField(max_length=20)
    Sex=models.CharField(max_length=20,null=True)
    Color=models.CharField(max_length=20,null=True)
    rep_image_url=models.CharField(max_length=20,null=True)
    LostNoticeNum=models.ForeignKey(LostNotice, on_delete = models.CASCADE,null=True)
    FindNoticeNum=models.ForeignKey(FindNotice, on_delete = models.CASCADE,null=True)
    Eye2Nose =  models.FloatField(max_length=20,null=True)
    Eye2Ears =  models.FloatField(max_length=20,null=True)
    '''
    def __str__(self):
        return self.Name
    '''
class Photo(models.Model):
    Photo=models.FileField(upload_to = 'lostList/images/',default='')
   # Photo=models.FileField(upload_to = '../capstone/media/lostList/images',default='')
    DogNumber=models.ForeignKey(Dog, on_delete = models.CASCADE)
    '''
    def __str__(self):
        return self.DogNumber
    '''

class FindLocation(models.Model):
    Si=models.CharField(max_length=20,null=True)
    Gu=models.CharField(max_length=20,null=True)
    Dong=models.CharField(max_length=20,null=True)