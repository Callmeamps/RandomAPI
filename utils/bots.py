from .slooth import slooth_bot
from .review_bot import review_bot, get_goal
from .writer import writer_bot
from .artist import post_prompt_gen
from .utilities import image_gen


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

def write_new_post_w_image(title, topic, post_format, platform, required_result="increase engagement"):
    research = slooth_bot(topic=topic)
    goal = get_goal(platform=platform, topic=topic,required_result=required_result)
    image_prompt = prompt_gen(title=title, topic=topic)
    image_res = image_gen(prompt=image_prompt)

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
            yield
        else: print(f"Review: {review_results}")

    print(final_post)
    return {"final_post": final_post.content, "image": image_res}

if __name__ == '__main__':
    pass

