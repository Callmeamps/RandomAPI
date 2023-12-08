from .utilities import completion

# Create New Post
# (Writer Bot: title, topic, format, platform, scheduled)
def writer_bot(title, topic, post_format, platform, research, is_scheduled=False):
# - Get topics latest information
# - Write a draft
    draft = completion(
        system="You are a writing assitant, write about the topics provided to you. You'll usually be given a title and a topic with some research. You will have to write a well constructed piece matching the format of the platform you are writing for.",
        user=f"""
Title: {title}
Topic: {topic}
Research: {research}
Format: {post_format}
Platform: {platform}
        """
    )
    return draft

if __name__ == '__main__':
    pass
