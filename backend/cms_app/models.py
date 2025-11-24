from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['parent__id', 'order_index', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Document(models.Model):
    STATUS_CHOICES = (('current','Актуальный'),('archived','Устаревший'))
    title = models.CharField(max_length=512)
    file = models.FileField(upload_to='documents/')
    category = models.ForeignKey(Category, related_name='documents', on_delete=models.PROTECT)
    version = models.CharField(max_length=64, blank=True)
    author = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='current')
    checksum = models.CharField(max_length=128, blank=True)
    size = models.BigIntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.version})" if self.version else self.title

class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, related_name='versions', on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/versions/')
    version_label = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    changelog = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.document.title} - {self.version_label}"

class AuditLog(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=64)
    object_type = models.CharField(max_length=64)
    object_id = models.CharField(max_length=64, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp.isoformat()} {self.action} {self.object_type}"
