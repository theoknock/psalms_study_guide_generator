import openai
import os
import sys
import docx
from docx import Document

try:
    openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
    sys.stderr.write(
        """\nSet up your API key; add OPENAI_API_KEY as a secret.\n""")
    exit(1)

psalms = [{'psalm': 40}, {'psalm': 10}, {'psalm': 12}, {'psalm': 23}, {
    'psalm': 35}, {'psalm': 41}, {'psalm': 88}, {'psalm': 139}, {'psalm': 141}]

# - Role: Bible Study Group Leader or Bible Teacher or Christian Studies Instructor
# - Key Responsibilities: Guide group members in understanding and applying biblical principles in their lives; effectively communicate biblical truths, and facilitate discussions to ensure understanding and engagement; cultivate a sense of community and belonging among group members; encourage active participation, and foster an environment where group members feel safe to share and explore their faith.
# - Knowledge or Expertise: Have a strong grasp of the Bible, basic Christian theology, and the historical and cultural contexts in which the Bible was written. Proficient in teaching, communication, and organization, while also displaying spiritual maturity, humility, and a willingness to engage in continual learning and self-development.


# - Tone and Formality: Academic, authoritative, and enthusiastic, spirited, eager
# - Level of Detail: Biblical references and citations from peer-reviewed theological publications
# - Preferred References: The Bible and peer-reviewed theological publications
# - Examples or Analogies: Structured sermons or academic and peer-reviewed theological  publications
# - Avoidance of Ambiguity: Use related biblical references to clarify any other references that are ambiguous in meaning

def create_prompts(psalm):
    return (
        f"Write a 5 to 6 sentence introduction to the spiritual and emotional elements of Psalm {psalm}, and try to connect its meaning and purpose with that of Christian faith. Use the King James Version.",
        f"Provide the full text of Psalm {psalm}. Use the King James Version.",
        f"Create a study guide for Psalm {psalm} that covers the entire psalm with verses being grouped by relationship; precede the study guide with “Study Guide”. Write a concise, one-line header that describes the topical relationship of groups of related verses (set the text style of the header to bold). Next, write a two-part, one paragraph summary that 1) begins with a single topic sentence, which expands on the header and  summarizes the main point presented by the group of verses (set the topic sentence text style to bold), and then reference the Bible book, chapter and verses that comprise the main point (put the reference in parentheses).; and, 2) continuing in the same paragraph, a more detailed summary (5 to 6 sentences in length) that further clarifies the intent and meaning of the main point ((set the text style of the header to regular).  Include the entire psalm (all verses) in the series of main points. After each main point, present one to three questions related to the verses that focus their attention to the most significant aspect(s) of the main point (precede the questions with “Focus”). Follow each question with an answer. Following the questions and answers “Focus” section, ask one to three questions that invite and encourage the reader to reflect on the material and its applicability to their personal experiences, and to relay those experiences by and through their answers to each; precede the questions with “Reflect”. There should be no punctuation after any of these. Do not number anything, but do bullet the reflection questions.  After all the main points are written, write a summary of the main points (or psalm) overall, highlighting their overall (or collective)  meaning and purpose, and connect that meaning and purpose with that of Christian faith and/or divine attributes of God (both communicable and incommunicable), as well as His purpose for man. After each main point, present one to three questions related to the verses that focus their attention to the most significant aspect(s) of the main point (precede the questions with “Focus”). Follow each question with an answer. Following the questions and answers “Focus” section, ask one to three questions that invite and encourage the reader to reflect on the material and its applicability to their personal experiences, and to relay those experiences by and through their answers to each; precede the questions with “Reflect”. There should be no punctuation after any of these. Do not number anything, but do bullet the reflection questions.r answers to each; precede the questions with “Reflect”. There should be no punctuation after any of these. Do not number anything, but do bullet the reflection questions. Use the King James Version.",
        f"Describe all the ways Psalm {psalm} embodies or reflects God’s nature in two sections: 1. divine (incommunicable) attributes; and, 2. communicable  attributes. Include biblical references, if applicable. Use the King James Version.",
        f"Relate the person and teachings of Jesus Christ and Psalm {psalm}, particularly, as they pertain to the gospel. Include supporting Bible verses for every connection made, especially if there is a match between the words of Jesus and verses in this psalm. Use the King James Version.",
        f"List all of the psalms that are identical or highly similar to Psalm {psalm}, whether in part or in whole. Explain the similarities in as much detail as possible. Use the King James Version."
    )


def user_content(psalm, prompts):
    content = []
    for prompt in prompts(psalm):
        prompt_dict = {"role": "user", "content": prompt}
        content.append(prompt_dict)
    return content


# Maintain the grouping of the prompts as a single message
# Process the response so that each prompt's response is handled separately
# Send the prompts in one message
# Process the grouped responses separately

# Created a conversation object that simulates starting a new conversation with the system role, followed by the user role for each prompt.
# All prompts are sent together as part of one messages object in the call to openai.ChatCompletion.create.
# Responses are expected to be in grouped_response.choices, with the assumption that they are separated by newlines (\n). The script then processes these grouped responses by splitting them at newlines and printing each one separately, preceded by its prompt index and the psalm number.

# The API will receive all prompts at once for each psalm but will return them in a single response object. The script then processes that object to handle each response separately.

# conversation = [{"role": "system", "content": "Let's start a new psalm study guide but, before we do, let me tell you a little bit about myself and my intentions for my audience: - Role: Bible Study Group Leader or Bible Teacher or Christian Studies Instructor - Key Responsibilities: Guide group members in understanding and applying biblical principles in their lives effectively communicate biblical truths, and facilitate discussions to ensure understanding and engagement cultivate a sense of community and belonging among group members encourage active participation, and foster an environment where group members feel safe to share and explore their faith. - Knowledge or Expertise: Have a strong grasp of the Bible, basic Christian theology, and the historical and cultural contexts in which the Bible was written. Proficient in teaching, communication, and organization, while also displaying spiritual maturity, humility, and a willingness to engage in continual learning and self-development. - Tone and Formality: Academic, authoritative, and enthusiastic, spirited, eager - Level of Detail: Biblical references and citations from peer-reviewed theological publications - Preferred References: The Bible and peer-reviewed theological publications - Examples or Analogies: Structured sermons or academic and peer-reviewed theological  publications - Avoidance of Ambiguity: Use related biblical references to clarify any other references that are ambiguous in meaning"}]

def get_responses_for_psalm(psalm):
    for prompt in create_prompts(psalm):
        response = openai.ChatCompletion.create(
        # model="gpt-4-1106-preview",
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
        )
        return response


for psalm in psalms:
    for prompt in create_prompts(psalm['psalm']):
        response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": prompt}]
        )
        print(str(f"\n\n" + response.choices[0].message['content'] + f"\n\n"))

# for psalm in psalms:
#     response = openai.ChatCompletion.create(
#         model="gpt-4-1106-preview",
#         messages=user_content(40, prompts),
#         # max_tokens=400,
#         # temperature=1,
#         # top_p=1,
#         # n=3
#     )

#     file_out = str(f"/Users/xcodedeveloper/Desktop/pip_install/script-guide-creator_psalms/out/Psalm {psalm} Scripture Guide.docx")
#     file_in = str(f"/Users/xcodedeveloper/Desktop/pip_install/script-guide-creator_psalms/in/Psalms_Template.docx")
#     doc = Document()

#     for message in response.choices:
#        paragraph = doc.add_paragraph(str(message.content))
# #        paragraph.styles = doc.styles['BodyPS']
#         print(message)

#     doc.save(file_out)
