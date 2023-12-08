from .slooth import slooth_bot
from .review_bot import review_bot, get_goal
from .writer import writer_bot


def write_new_post(title, topic, post_format, platform, required_result="increase engagement"):
    research = slooth_bot(topic=topic)
    goal = get_goal(platform=platform, topic=topic,required_result=required_result)

    while True:
        print("Getting Started: Drafting...")
        draft = writer_bot(title, topic, post_format, platform, research)
        final_post = ""
        print("Submitting Results...")
        review_results = review_bot(posts=draft, goals=goal)
        print(str(review_results))
        if (review_results is False):
            print("Draft failed")
        elif (review_results):
            print("Draft Succedded")
            final_post = draft
            break

        print(final_post)
    return final_post.content
#    - if schedule is true
#       - Submit to queue
#    - else if schedule is false
#       - Post to platform
# - else if review failed
#    - write new draft
#    - submit for review
if __name__ == '__main__':
    pass

