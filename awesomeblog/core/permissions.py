from enum import Enum


class BasePermissionEnum(Enum):
    @property
    def codename(self):
        return self.value.split(".")[1]


class CollaboratorsBlogPostPermissions(BasePermissionEnum):
    CREATE_BLOG_POSTS = "blog.create_blog_posts"
    VIEW_BLOG_POSTS = "blog.view_blog_posts"
    UPDATE_BLOG_POSTS = "blog.edit_blog_posts"
    DELETE_BLOG_POSTS = "blog.delete_blog_posts"
