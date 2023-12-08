import os
import json

from .utilities import json_completion

def get_goal(platform, topic, required_result):
    res = json_completion(
        system="You're help set goals, based on the information provided, create a list of goals for posts. Give your result as 'goal'",
        user=f"Platform: {platform}, Topic: {topic} Results: {required_result}",
        seed=222123
    )

    data = json.loads(res.content)
    goals = data['goal']
    return goals

# Review Posts
# (Review Bot: goal/s, posts)
def review_bot(goals, posts):
# - Grade posts based on the goal/s
    json_review = json_completion(
                    system="You are an assessment assistant designed to review posts and grade them, based on a goal, with a numeric score between 1 & 5. Give your result as an 'overall_score'.",
                    user=f"Goals: {goals} \n Posts: {posts}",
                    seed=111111
                    )
    data = json.loads(json_review.content)
    overall_score = data['overall_score']

    if (overall_score >= 3):
        result = True
    elif(overall_score < 3):
        result = False
    else: result = json_review
    
    print(f"Review:\n{json_review}\nResult: {result}")
    return result

if __name__ == '__main__':
    pass
