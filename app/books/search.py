from django.db.models import Q
from django.utils.dateparse import parse_date


def parse_date_safe(date_string):
    try:
        date_obj = parse_date(date_string)
    except (TypeError, ValueError):
        return None
    return date_obj


def filter_books(request, queryset):
    """Return given book queryset, filtered by query parameters.

    Searchable query parameters that correspond to database fields are:
    title, genre, author (either first or last name), and publication_date.

    Each of the above can take multiple values (by passing the key value pair multiple
    times in the URL), consisting logical OR relations between those same-keyed values.

    Parameters publication_date_from and publication_date_to are single valued, and
    keep only results whose publication_date is "greater than or equal", and "less than
    or equal" the given value, respectively.

    Ultimately, those filter groups are joined with logical AND relations, and used to
    fetch the end results.
    """
    title_filters = Q()
    titles = request.GET.getlist("title")
    for title in titles:
        if title:
            title_filters |= Q(title__icontains=title)

    genre_filters = Q()
    genres = request.GET.getlist("genre")
    for genre in genres:
        if genre:
            genre_filters |= Q(genre__icontains=genre)

    author_filters = Q()
    authors = request.GET.getlist("author")
    for author in authors:
        if author:
            author_filters |= Q(author__first_name__icontains=author) | Q(
                author__last_name__icontains=author
            )

    date_filters = Q()
    dates = request.GET.getlist("publication_date")
    for date in dates:
        date_obj = parse_date_safe(date)
        if date_obj is not None:
            date_filters |= Q(publication_date=date_obj)

    date_from_filter = Q()
    date_from = request.GET.get("publication_date_from")
    date_obj = parse_date_safe(date_from)
    if date_obj is not None:
        date_from_filter = Q(publication_date__gte=date_obj)

    date_to_filter = Q()
    date_to = request.GET.get("publication_date_to")
    date_obj = parse_date_safe(date_to)
    if date_obj is not None:
        date_to_filter = Q(publication_date__lte=date_obj)

    filters = (
        title_filters
        & genre_filters
        & author_filters
        & date_filters
        & date_from_filter
        & date_to_filter
    )
    return queryset.filter(filters)
