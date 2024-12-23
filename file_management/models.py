from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Folder(models.Model):
    """
    The Folder model tracks the folder hierarchy
    using a Parent-Child relationship.
    Folders are unique per owner and parent directory
    """
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subfolders', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'parent', 'owner')



class File(models.Model):
    """
    One file belongs to a specific folder and has metadata
    like size and upload path.

    Files are unique per folder and owner.
    """
    name = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder, null=True, blank=True, related_name='files', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='uploads/')
    size = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'folder', 'owner')


class SharedItem(models.Model):
    """
    Allows sharing files or folders with other users

    This model tracks the shared item's type(file or folder) and their IDs 
    for flexible sharing
    """
    item_type_choices = (
        ('file', 'File'),
        ('folder', 'Folder'),
    )
    item_type = models.CharField(max_length=10, choices=item_type_choices)
    item_id = models.PositiveIntegerField()
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_items')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_shared_items')
    shared_at = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('item_type', 'item_id', 'shared_with')