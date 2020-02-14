import os, json, re


def challenge_lookup(challenge_id, data_path = "/workspace/prework-gitpod/data/challenges.json"):
    """
    Given a challenge ID and a path to the JSON, return a python object with all of the challenge details
    challenge_id: string,
    data_path: string
    """

    with open(data_path, "r") as read_file:
        data = json.load(read_file)
    
    match = list(filter(lambda challenge: challenge['id'] == challenge_id, data))

    return match[0]


def file_builder(challenge):
    """
    Given a challenge object, build the neccesary files for the challenge inside of the workspace
    challenge: dictionary[title, instructions, tests, files, id, etc...]
    """
    directory = '/workspace/prework-gitpod/prework/' + re.sub('[^A-Za-z0-9 ]+', '', challenge['title']).replace(' ', '_').lower() + '/'

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + 'README.md', 'w+') as readme:
        readme.write(challenge['instructions'])

    with open(directory + 'test.js', 'w+') as tests:
        tests.write(challenge['tests'])

    for file_type in ["html", "css", "js"]:
        prefix = {
            "html": "index",
            "css": "styles",
            "js": "app"
        }

        filename = f'{directory}/{prefix[file_type]}.{file_type}'
        content = list(filter(lambda content: content['type'] == file_type, challenge['files']))[0]
        
        with open(filename, 'w+') as file:
            file.write(eval(content['content']))

# this executes only when the script is run from the terminal
if __name__ == "__main__":

    # try to grab the challenge ID from the environment variables
    try: 
        challenge_id = os.environ['CHALLENGE_ID']
    
    # if no env var exists, bump the user to the first challenge
    except:
        challenge_id = '5c4768c3b5bf0ae8849779d6'
    
    # build the files for the current challenge, pointing to the JSON file with all challenge data
    file_builder(
        challenge_lookup(
            challenge_id, 
            # data_path="data/challenges.json"
        )
    )