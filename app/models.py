from django.db import models
from accounts.models import Account
import uuid
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
# Create your models here.

VOTE_CHOICES = (
    ('UP', 1),
    ('DOWN', -1)
)


class Vote(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    value = models.IntegerField(choices=VOTE_CHOICES)


class Reply(models.Model):
    is_chosen = models.BooleanField(default=False)
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          unique=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField(max_length=500, blank=True, null=False)

    def __str__(self):
        return self.body[:100]


# class Tag(models.Model):
#     name = models.CharField(max_length=100, blank=False, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Article.Status.PUBLISHED)


class Article(models.Model):
    # optional_field =
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    slug = models.SlugField(max_length=250, blank=True,
                            unique_for_date='publish')

    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=300, blank=False, null=False)
    body = models.TextField(max_length=10000, blank=True, null=False)

    thumbnail = models.ImageField(
        upload_to="articles/%y/%m/%d", default="pic.jpg")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # tags = models.ManyToManyField('Tag', blank=True)
    publish = models.DateTimeField(default=timezone.now)

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # custom manager.
    tags = TaggableManager()
    # extra_fields = models.ManyToManyField(
    #     'your_app.ExtraField',
    #     verbose_name=_('Extra fields'),
    #     blank=True, null=True,
    # )

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ('-publish',)
        indexes = [models.Index(fields=['-publish']),]

    def get_absolute_url(self):
        return reverse('article_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug,
                             self.id])

# class ExtraFieldType(models.Model):
#     """
#     Model to create custom information holders.
#     :name: Name of the attribute.
#     :description: Description of the attribute.
#     :model: Can be set in order to allow the use of only one model.
#     :fixed_values: Can transform related exta fields into choices.
#     """
#     name = models.CharField(
#         max_length=100,
#         verbose_name=_('Name'),
#     )

#     description = models.CharField(
#         max_length=100,
#         blank=True, null=True,
#         verbose_name=_('Description'),
#     )

#     model = models.CharField(
#         max_length=10,
#         choices=(
#             ('YourModel', 'YourModel'),
#             # which models do you want to add extra fields to?
#             ('AnotherModel', 'AnotherModel'),
#         ),
#         verbose_name=_('Model'),
#         blank=True, null=True,
#     )

#     fixed_values = models.BooleanField(
#         default=False,
#         verbose_name=_('Fixed values'),
#     )

#     class Meta:
#         ordering = ['name', ]

#     def __unicode__(self):
#         return '{0}'.format(self.name)


# class ExtraField(models.Model):
#     """
#     Model to create custom fields.
#     :field_type: Connection to the field type.
#     :value: Current value of this extra field.
#     """
#     field_type = models.ForeignKey(
#         'your_app.ExtraFieldType',
#         verbose_name=_('Field type'),
#         related_name='extra_fields',
#         help_text=_('Only field types with fixed values can be chosen to add'
#                     ' global values.'),
#     )

#     value = models.CharField(
#         max_length=200,
#         verbose_name=_('Value'),
#     )

#     class Meta:
#         ordering = ['field_type__name', ]

#     def __unicode__(self):
#         return '{0} ({1}) - {2}'.format(
#             self.field_type, self.field_type.get_model_display() or 'general',
#             self.value)
