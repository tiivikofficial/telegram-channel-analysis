#!/usr/bin/env python3
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import matplotlib.pyplot as plt

# Replace these with your actual credentials from https://my.telegram.org
api_id = "******"  # Example: 1234567 (must be an integer)
api_hash = '*****'  # Your API hash (string)

# Specify the channel username or ID (e.g., '@my_channel')
channel_username = '@my_channel'

# Create a Telegram client instance with a session name
client = TelegramClient('session_name', api_id, api_hash)

# A simple heuristic function to identify potential fake followers.
# This function marks a user as fake if:
#   - The user does not have a profile photo.
#   - The user does not have a username.
#   - The length of the first name is less than 3 characters.
# Note: This is a naive approach and may not be 100% accurate.
def is_fake_follower(user):
    # Get the user's first name if available; otherwise, use an empty string.
    first_name = user.first_name if user.first_name else ""
    # Check conditions. You can improve or modify these rules based on your requirements.
    if (user.photo is None) and (not user.username) and (len(first_name.strip()) < 3):
        return True
    else:
        return False

async def main():
    # Retrieve the channel entity using its username or ID
    channel = await client.get_entity(channel_username)
    
    offset = 0
    limit = 100  # Number of members to fetch per request
    all_participants = []
    
    print("Collecting channel participants, please wait...")
    
    # Continuously fetch participants until there are no more left.
    while True:
        participants = await client(GetParticipantsRequest(
            channel=channel,
            filter=ChannelParticipantsSearch(''),
            offset=offset,
            limit=limit,
            hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)
        print(f"Collected {len(all_participants)} members so far.")
    
    print(f"Total participants collected: {len(all_participants)}")
    
    # Separate users based on the presence of a profile photo.
    users_with_photo = [user for user in all_participants if user.photo]
    users_without_photo = [user for user in all_participants if not user.photo]
    
    count_with_photo = len(users_with_photo)
    count_without_photo = len(users_without_photo)
    
    print(f"Participants with profile photo: {count_with_photo}")
    print(f"Participants without profile photo: {count_without_photo}")
    
    # List users who do not have a profile photo with their numeric ID and basic info
    print("\nListing participants without a profile photo:")
    for user in users_without_photo:
        # Extract basic details. Note: some fields may be None.
        user_id = user.id
        first_name = user.first_name if user.first_name else ''
        last_name = user.last_name if hasattr(user, 'last_name') and user.last_name else ''
        username = user.username if hasattr(user, 'username') and user.username else ''
        full_name = (first_name + ' ' + last_name).strip()
        print(f"ID: {user_id} | Name: {full_name} | Username: {username}")
    
    # Identify potential fake followers using the simple heuristic
    potential_fake_followers = [user for user in users_without_photo if is_fake_follower(user)]
    
    print("\nIdentified potential fake followers:")
    for user in potential_fake_followers:
        # Extract basic details
        user_id = user.id
        first_name = user.first_name if user.first_name else ''
        last_name = user.last_name if hasattr(user, 'last_name') and user.last_name else ''
        username = user.username if hasattr(user, 'username') and user.username else ''
        full_name = (first_name + ' ' + last_name).strip()
        print(f"ID: {user_id} | Name: {full_name} | Username: {username}")
    
    print(f"\nTotal potential fake followers identified: {len(potential_fake_followers)}")
    
    # Plot a pie chart to display the distribution of profile photo presence
    labels = ['Profile Photo Present', 'Profile Photo Absent']
    sizes = [count_with_photo, count_without_photo]
    colors = ['#66b3ff', '#ff9999']
    explode = (0.1, 0)  # Slightly offset the first slice for emphasis
    
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%',
            shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Distribution of Channel Members by Profile Photo')
    plt.show()

# Run the client and execute the main coroutine within the client context
with client:
    client.loop.run_until_complete(main())
