from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name=models.CharField(max_length=255)
    slug=models.SlugField(blank=True)
    parent=models.ForeignKey('self',null=True,blank=True,related_name='children',on_delete=models.CASCADE)
    order_index=models.IntegerField(default=0)
    def save(self,*a,**kw):
        if not self.slug:self.slug=slugify(self.name)
        super().save(*a,**kw)
    def __str__(self):return self.name

class Document(models.Model):
    title=models.CharField(max_length=255)
    file=models.FileField(upload_to='docs/')
    category=models.ForeignKey(Category,related_name='documents',on_delete=models.PROTECT)
    version=models.CharField(max_length=50,blank=True)
    def __str__(self):return self.title
