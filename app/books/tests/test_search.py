import pytest

from books.models import Book

pytestmark = pytest.mark.django_db


@pytest.fixture
def books(user, other_user):
    return Book.objects.bulk_create(
        [
            Book(
                title="ABC",
                genre="History",
                publication_date="1995-01-05",
                author=user,
            ),
            Book(
                title="E 123",
                publication_date="2000-12-20",
                author=user,
            ),
            Book(
                title="Test Book",
                genre="Novel",
                publication_date="2023-08-20",
                comments_allowed=True,
                author=user,
            ),
            Book(
                title="Example Magic Title",
                genre="Fantasy",
                publication_date="2019-05-11",
                author=user,
            ),
            Book(
                title="EFG1 title here",
                publication_date="2001-02-20",
                author=other_user,
            ),
            Book(
                title="Foo Bar tests",
                genre="Fantasy",
                publication_date="2023-01-01",
                comments_allowed=True,
                author=other_user,
            ),
            Book(
                title="321 Testing title",
                genre="History",
                publication_date="2020-1-16",
                comments_allowed=True,
                author=other_user,
            ),
        ]
    )


@pytest.mark.parametrize(
    "query_string, expected_book_indices",
    [
        ("title=test", {4, 7, 8}),
        ("genre=fantasy", {0, 5, 7}),
        ("author=Doe", {0, 2, 3, 4, 5}),
        ("publication_date=2023-08-20", {4}),
        ("publication_date_from=2022-01-01", {0, 1, 4, 7}),
        ("publication_date_to=2001-02-20", {2, 3, 6}),
        ("genre=fanta&genre=Novel", {0, 4, 5, 7}),
        ("title=magic&genre=fantasy", {0, 5}),
        ("title=titl&genre=fantasy&genre=history", {5, 8}),
        ("title=test&publication_date_from=2020-05-10", {4, 7}),
        ("publication_date=2000-12-20&publication_date=2020-1-16", {3, 8}),
    ],
)
def test_search(client, book, other_book, books, query_string, expected_book_indices):
    existing_books = [book, other_book, *books]
    book_indices = {book.id: index for index, book in enumerate(existing_books)}

    response = client.get(f"/books/?{query_string}")
    data = response.json()["results"]
    returned_book_indices = {book_indices[book["id"]] for book in data}

    assert response.status_code == 200

    for book in data:
        assert set(book) == {
            "id",
            "title",
            "genre",
            "publication_date",
            "comments_allowed",
            "author",
        }

    assert len(data) == len(expected_book_indices)
    assert returned_book_indices == expected_book_indices
