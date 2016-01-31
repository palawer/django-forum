from main.models import Forum, Topic, Post

# all forums
forums = Forum.objects.all()

# check last post id
for forum in forums:
    last_post = Post.objects.filter(forum=forum).order_by('-id')[0]
    print forum.id, forum.last_post.id, last_post.id

# check posts count
for forum in forums:
    total_posts = Post.objects.filter(forum=forum).count()
    print forum.id, forum.posts, total_posts

# check topics count
for forum in forums:
    total_topics = Topic.objects.filter(forum=forum).count()
    print forum.id, forum.topics, total_topics

# all topics
topics = Topic.objects.all()

# check first post id
for topic in topics:
    first_post = Post.objects.filter(topic=topic).order_by('id')[0]
    if topic.first_post.id != first_post.id:
        print topic.id, topic.first_post.id, first_post.id

# check last post id
for topic in topics:
    last_post = Post.objects.filter(topic=topic).order_by('-id')[0]
    if topic.last_post.id != last_post.id:
        print topic.id, topic.last_post.id, last_post.id

# check replies count
for topic in topics:
    replies = Post.objects.filter(topic=topic).count() - 1
    if topic.replies != replies:
        print topic.id, topic.replies, replies

