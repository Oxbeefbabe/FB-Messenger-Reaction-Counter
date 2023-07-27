import json
import sys


def get_chat():
    chat = []
    for i in range(1, 10):
        with open(f"src/message_{i}.json") as file:
            chat.extend(list(map(get_msg_reactions, json.load(file)['messages'])))
    return list(filter(lambda x: 'reactions' in x.keys(), chat))


def get_participants():
    participants = []
    for i in range(1, 10):
        with open(f"src/message_{i}.json") as file:
            for msg in json.load(file)['messages']:
                if msg['sender_name'] not in participants:
                    participants.append(msg['sender_name'])
    return participants


def get_msg_reactions(msg):
    reaction_info = {'sender': msg['sender_name']}
    if 'reactions' in msg.keys():
        reactions = msg['reactions']
        for reaction in reactions:
            reaction['reaction'] = reaction['reaction'].encode('latin-1').decode('utf-8')
        reaction_info['reactions'] = msg['reactions']
    return reaction_info


def count_reactions_received(participant_list, chat_log):
    reaction_counts = {name: {} for name in participant_list}
    for msg in chat_log:
        for reaction in msg['reactions']:
            if reaction['reaction'] in reaction_counts[msg['sender']].keys():
                reaction_counts[msg['sender']][reaction['reaction']] = \
                    reaction_counts[msg['sender']][reaction['reaction']] + 1
            else:
                reaction_counts[msg['sender']][reaction['reaction']] = 1
    return reaction_counts


def get_reactions_received():
    participants = get_participants()
    chat = get_chat()
    reactions = count_reactions_received(participants, chat)
    return reactions


def print_reaction_details():
    reactions = get_reactions_received()
    for user in reactions:
        print(user)
        if reactions[user].keys():
            for reaction in reactions[user]:

                print(f"\t{reaction}: {reactions[user][reaction]} time{'s' if reactions[user][reaction] > 1 else ''}")
        else:
            print("\tGot no reactions in the chat history")


def print_reaction_counts():
    reactions = get_reactions_received()
    reaction_counts = {}
    for user in reactions:
        reaction_counts[user] = sum(reactions[user].values())
    reaction_counts = sorted(reaction_counts.items(), key=lambda x:x[1], reverse=True)
    for user, total in reaction_counts:
        print(f"{user} has received {total} reactions")


def add_page_num(msg, page_num):
    msg["page"] = page_num
    return msg


def find_user(user):
    chat = []
    for i in range(1, 10):
        with open(f"src/message_{i}.json") as file:
            chat.extend(list(map(lambda x: add_page_num(x, i), json.load(file)['messages'])))
    chat = list(filter(lambda x: 'sender_name' in x.keys(), chat))
    for msg in chat:
        if 'sender_name' in msg.keys() and msg['sender_name'] == user:
            print(msg)


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        print_reaction_counts()
    elif args[1] == "details":
        print_reaction_details()
