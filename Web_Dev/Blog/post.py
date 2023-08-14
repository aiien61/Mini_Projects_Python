from typing import Iterable


class Post:
    def __init__(self, id: int, title: str, subtitle: str, body: str):
        self.post_id = id
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.next = None


class Post_List:

    def __init__(self, posts: Iterable):
        self.head = None
        if posts:
            self.add_posts(posts)


    def __iter__(self):
        node = self.head
        while node:
            yield node
            node = node.next


    def __len__(self):
        for i, _ in enumerate(self, start=1):
            pass
        return i


    def __getitem__(self, key):
        for post in self:
            if post.post_id == key:
                return post


    def add_post(self, post: dict):
        if not self.head:
            self.head = Post(**post)
            return None
        
        node = self.head
        while node.next:
            node = node.next

        node.next = Post(**post)
        return None


    def add_posts(self, posts: Iterable):
        index = 0
        if not self.head:
            self.head = Post(**posts[index])
            index += 1

        node = self.head
        while node.next:
            node = node.next

        while index < len(posts):
            node.next = Post(**posts[index])
            node = node.next
            index += 1
        return None
