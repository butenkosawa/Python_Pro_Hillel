import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


class Post:
    def __init__(self, id: int, title: str, body: str):
        self.id = id
        self.title = title
        self.body = body


class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.posts: list[Post] = []

    def add_post(self, post: Post):
        self.posts.append(post)

    def average_title_length(self) -> float:
        titles_length = sum(len(post.title) for post in self.posts)
        return titles_length / len(self.posts) if self.posts else 0.0

    def average_body_length(self) -> float:
        bodies_length = sum(len(post.body) for post in self.posts)
        return bodies_length / len(self.posts) if self.posts else 0.0


class BlogAnalytics:
    def __init__(self):
        self.users: list[User] = []

    def fetch_data(self):
        """Fetch users and their posts."""
        response = requests.get(f"{BASE_URL}/users")
        users_data = response.json()
        for user_data in users_data:
            user = User(id=user_data['id'], name=user_data['name'])
            # Fetch posts for the user
            response_posts = requests.get(f"{BASE_URL}/posts?userId={user.id}")
            posts_data = response_posts.json()
            for post_data in posts_data:
                post = Post(id=post_data['id'], title=post_data['title'], body=post_data['body'])
                user.add_post(post)
            self.users.append(user)

    def user_with_longest_average_body(self) -> User:
        users_by_average_body = sorted(self.users, key=lambda user: user.average_body_length())
        return users_by_average_body[-1]

    def user_with_longest_average_title(self) -> User:
        users_by_average_title = sorted(self.users, key=lambda user: user.average_title_length())
        return users_by_average_title[-1]

    def users_with_many_long_titles(self) -> list[User]:
        return list(filter(lambda user: user.average_title_length() > 40, self.users))


if __name__ == "__main__":
    analytics = BlogAnalytics()
    analytics.fetch_data()

    longest_body_user = analytics.user_with_longest_average_body()
    longest_title_user = analytics.user_with_longest_average_title()
    long_title_users = analytics.users_with_many_long_titles()

    print(
        f"User with longest average body length: "
        f"{longest_body_user.name} ({longest_body_user.average_body_length():.2f})"
    )
    print(
        f"User with longest average title length: "
        f"{longest_title_user.name} ({longest_title_user.average_title_length():.2f})"
    )

    print("Users with average title length > 40:")
    for user in long_title_users:
        print(f"{user.name} ({user.average_title_length():.2f})")
