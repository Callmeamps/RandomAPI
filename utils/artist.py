from .utilities import image_gen, completion

def post_prompt_gen(title, topic):
    res = completion(
        system="You're an AI Image Generation Prompt Generator, based on the title and topic of a post, write a prompt to generate the image for the post.",
        user=f"Title: {title}, Topic: {topic}",
    )

    return res

def insta_prompt_gen(caption=None, keywords=None):
    res = completion(
        system="You're an AI Image Generation Prompt Generator, based on the caption or keywords of a post, write a prompt to generate the image for the post.",
        user=f"Caption: {caption}, Keywords: {keywords}",
    )

    return res


def create_image(prompt):
    image_gen(prompt)