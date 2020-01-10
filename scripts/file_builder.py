import os, json, re

def challenge_lookup(challenge_id, data_path = "~/workspace/prework-gitpod/data/challenges.json"):
    
    with open(data_path, "r") as read_file:
        data = json.load(read_file)
    
    match = list(filter(lambda person: person['id'] == challenge_id, data))

    return match[0]

def file_builder(challenge):

    directory = 'prework/' + re.sub('[^A-Za-z0-9]+', '', challenge['title']) + '/'

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + 'README.md', 'w+') as readme:
        readme.write(challenge['instructions'])

    

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
         
if __name__ == "__main__":
	challenge_id = os.environ['CHALLENGE_ID']
	file_builder(challenge_lookup(challenge_id))
    # file_builder(challenge_lookup("5c4768c3b5bf0ae8849779dd", data_path="data/challenges.json"))
