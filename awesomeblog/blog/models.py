from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from markdown import markdown
from taggit.managers import TaggableManager

from ..core.models import PublishableModel
from ..core.permissions import CollaboratorsBlogPostPermissions
from ..seo.models import SeoModel


class BlogPostCategory(SeoModel):
    """Category for Blog Post"""

    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=256, unique=True)
    description = models.TextField(blank=True)
    background_image = models.ImageField(
        upload_to="blogpost-category-images", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Blog Post Category"
        verbose_name_plural = "Blog Post Categories"

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse(
    #         "blog:category", kwargs={"slug": self.slug }
    #     )


class Blog(SeoModel, PublishableModel):
    """Blog model"""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=128, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BlogPost(SeoModel, PublishableModel):
    """Post for the blog"""

    PUBLIC = "PU"
    DRAFT = "DR"
    PRIVATE = "PR"
    BLOG_POST_ACCESS_CHOICES = [
        (PUBLIC, "PUBLIC"),
        (DRAFT, "DRAFT"),
        (PRIVATE, "PRIVATE"),
    ]

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="posts")

    access = models.CharField(
        max_length=20,
        choices=BLOG_POST_ACCESS_CHOICES,
        default=PRIVATE,
        verbose_name=_("Access"),
        help_text=_(
            "Whether the blog post should remain private (for you only), or public or draft"
        ),
        blank=False,
        null=False,
    )
    category = models.ForeignKey(
        BlogPostCategory,
        blank=True,
        null=True,
        related_name="blogposts",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="blogposts",
    )
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="BlogPostCollaborator",
        related_name="collaborator_on_blog_post",
        blank=True,
        verbose_name="Collaborators",
        help_text=_("The users that collaborate on this blog post"),
    )
    slug = models.SlugField(max_length=256, unique=True)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    body = models.TextField(blank=True)
    body_html = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:blogpost_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-updated", "title"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        permissions = (
            (
                CollaboratorsBlogPostPermissions.CREATE_BLOG_POSTS.codename,
                "Collaborator can create blog posts.",
            ),
            (
                CollaboratorsBlogPostPermissions.VIEW_BLOG_POSTS.codename,
                "Collaborator can view blog posts.",
            ),
            (
                CollaboratorsBlogPostPermissions.UPDATE_BLOG_POSTS.codename,
                "Collaborator can update blog posts.",
            ),
            (
                CollaboratorsBlogPostPermissions.DELETE_BLOG_POSTS.codename,
                "Collaborator can delete blog posts.",
            ),
        )
        print(permissions)

    def save(self, *args, **kwargs):
        if self.body:
            self.body_html = markdown(self.body)
        super(BlogPost, self).save(*args, **kwargs)


class BlogPostImage(models.Model):
    """Image for the blog post"""

    blogpost = models.ForeignKey(
        BlogPost, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="blogpost_images", blank=False)
    sort_order = models.PositiveIntegerField()
    alt = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ["sort_order"]

    def get_ordering_queryset(self):
        return self.blogpost.images.all()


class BlogPostCollaborator(models.Model):
    """Collaborator for the blog post"""

    collaborator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blogpost_collaborators",
        verbose_name=_("Collaborator"),
    )
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="blogpost_collaborators",
        verbose_name=_("Blogpost"),
    )
    collaboration_created = models.DateTimeField(auto_now_add=True)
    collaboration_updated = models.DateTimeField(auto_now=True)
    collaboration_reason = models.CharField(max_length=256, blank=True)

    class Meta:
        ordering = ["post__updated"]
        unique_together = ("collaborator", "post")
        verbose_name = pgettext_lazy(
            "Blog Post collaborators verbose name (singular form)",
            "blog post collaborator",
        )
        verbose_name_plural = pgettext_lazy(
            "Blog Post collaborators verbose name (plural form)",
            "blog post collaborators",
        )
