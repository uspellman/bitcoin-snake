import random

# Collect various inputs from the user
user_input = input("Enter a First Name: ")
user_color = input("Enter your favorite color: ")
user_animal = input("Enter your favorite animal: ")
user_place = input("Enter your favorite place: ")
user_emotion = input("Enter how you're feeling right now: ")

# List of possible responses for initial greeting
responses = [
    f"Hello {user_input}, how are you feeling today?",
    f"Great to see you, {user_input}! What's new?",
    f"Welcome, {user_input}! How's your day going?",
    f"Hi {user_input}! Hope you're having a wonderful day!",
    f"Hey there {user_input}! What brings you here today?"
]

# Print initial greeting
print(random.choice(responses))

# List of poem templates
poem_templates = [
    f"""
In a world of {user_color} dreams,
{user_input} wandered by the streams.
A {user_animal} appeared with grace,
Near the magical {user_place}.
Feeling {user_emotion}, heart so bright,
Under the stars that shine at night.
    """,
    
    f"""
Down in {user_place} where {user_input} goes,
Where the {user_color} wind gently blows.
A {user_animal} dances in the light,
Making {user_emotion} feelings take flight.
    """,
    
    f"""
{user_input} and their {user_animal} friend,
Walking through {user_place} without end.
The sky turned {user_color} above their head,
{user_emotion} thoughts left unsaid.
    """,
    
    f"""
{user_color} like the morning sun,
{user_input}'s adventure has begun.
In {user_place} with their {user_animal} guide,
{user_emotion} feelings they cannot hide.
    """
]

print("\nNow, I'll create a special poem just for you...")
print(random.choice(poem_templates))

