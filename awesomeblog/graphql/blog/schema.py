import graphene
from graphene_django import DjangoObjectType

from ...blog.models import Blog, BlogPost, BlogPostCategory, BlogPostCollaborator
from ...users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("name", "first_name", "email", "user_name")


class BlogType(DjangoObjectType):
    class Meta:
        model = Blog
        fields = ("id", "slug", "name", "description", "posts")


class BlogPostCategoryType(DjangoObjectType):
    class Meta:
        model = BlogPostCategory
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "background_image",
            "background_image_alt",
        )


class BlogPostType(DjangoObjectType):
    class Meta:
        model = BlogPost
        fields = (
            "id",
            "blog",
            "access",
            "category",
            "blog",
            "author",
            "collaborators",
            "slug",
            "title",
            "description",
            "body",
            "body_html",
            "created",
            "updated",
        )


class BlogPostCollaboratorType(DjangoObjectType):
    class Meta:
        model = BlogPostCollaborator
        fields = ("collaborator", "post")


class BlogQueries(graphene.ObjectType):
    blog_by_name = graphene.Field(BlogType, name=graphene.String(required=True))
    all_blog_posts = graphene.List(BlogPostType)

    def resolve_blog_by_name(root, info, name):
        try:
            return Blog.objects.get(name=name)
        except Blog.DoesNotExist:
            return None

    def resolve_all_blog_posts(root, info):
        return (
            BlogPost.objects.select_related("blog", "author", "category")
            .prefetch_related("collaborators")
            .filter(access="PU")
            .published()
        )
