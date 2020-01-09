import os

def challenge_lookup(challenge_id, data_path = "~/workspace/prework-gitpod/data/challenges.json"):
    
    with open(data_path, "r") as read_file:
        data = json.load(read_file)
    
    match = list(filter(lambda person: person['id'] == challenge_id, data))

    return match[0]

def file_builder(challenge):
    for file_type in ["html", "css", "js"]:
        
        prefix = {
            "html": "index",
            "css": "styles",
            "js": "app"
        }

        filename = f'{prefix[file_type]}.{file_type}'
        
        try:
            os.remove(filename)
        except OSError:
            pass
        
        content = list(filter(lambda content: content['type'] == file_type, challenge['files']))[0]
        
        with open(filename, 'w+') as file:
            file.write(eval(content['content']))
        
file_builder(challenge_lookup("5c4768c3b5bf0ae884977a32"))
