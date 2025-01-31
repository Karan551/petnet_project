from django import template
from store.models import Category, Product

register = template.Library()


@register.inclusion_tag("core/menu.html")
def menu():
    categories = Category.objects.all()
    

    return {"categories": categories}

