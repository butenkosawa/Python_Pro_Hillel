import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com"


class Comment:
    def __init__(self, id: int, post_id: int, name: str, email: str, body: str):
        self.id = id
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body


class CommentModerator:
    def __init__(self):
        self.comments: list[Comment] = []
        self.flagged_comments: list[Comment] = []

    def fetch_comments(self):
        response_comments = requests.get(f"{BASE_URL}/comments")
        comments_data = response_comments.json()
        for comment_data in comments_data:
            comment = Comment(
                id=comment_data['id'],
                post_id=comment_data['postId'],
                name=comment_data['name'],
                email=comment_data['email'],
                body=comment_data['body']
            )
            self.comments.append(comment)

    def flag_suspicious_comments(self):
        for comment in self.comments:
            if "libero" in comment.body.lower() or "aut" in comment.body.lower():
                self.flagged_comments.append(comment)

    def group_by_post(self) -> dict[int, list[Comment]]:
        grouped_comments = {}
        for comment in self.flagged_comments:
            if comment.post_id not in grouped_comments:
                grouped_comments[comment.post_id] = []
            grouped_comments[comment.post_id].append(comment)
        return grouped_comments

    def top_spammy_emails(self, n: int = 5) -> dict[str, int]:
        spammy_emails = {}
        email_count = {}
        for comment in self.comments:
            if comment.email not in email_count:
                email_count[comment.email] = 0
            email_count[comment.email] += 1

        sorted_emails = sorted(email_count.items(), key=lambda x: x[1], reverse=True)
        for email, count in sorted_emails[:n]:
            spammy_emails.update({email: count})

        return spammy_emails

    def export_flagged_to_json(self, filename: str = "flagged_comments.json"):
        with open(filename, 'w') as file:
            flagged_data = [
                {
                    "id": comment.id,
                    "post_id": comment.post_id,
                    "name": comment.name,
                    "email": comment.email,
                    "body": comment.body
                } for comment in self.flagged_comments
            ]

            json.dump(flagged_data, file, indent=4)


if __name__ == "__main__":
    moderator = CommentModerator()
    moderator.fetch_comments()
    moderator.flag_suspicious_comments()
    grouped_comments = moderator.group_by_post()
    spammy_emails = moderator.top_spammy_emails()
    moderator.export_flagged_to_json()

    print(
        f"Summary of fetched comments:\n"
        f"   Total comments fetched: {len(moderator.comments)}\n"
        f"   Total flagged comments: {len(moderator.flagged_comments)}\n"
    )
    print("\nNumber of flagged comments per post:")
    for comment in grouped_comments:
        print(f"   Post ID {comment}: {len(grouped_comments[comment])} flagged comments.")

    print("\nList of the top 5 most spammy emails:")
    for email, amount in spammy_emails.items():
        print(f"   Email '{email}' spammed {amount} times")

    print(f"\nFlagged comments exported to 'flagged_comments.json' successfully.")
