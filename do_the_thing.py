import sys
import json

if __name__ == '__main__':
    #args = sys.argv[1:]
    issue_json = json.loads(sys.argv[1])
    #print(issue_json)
    
    title = issue_json['title']
    body = issue_json['body']
    author_role = issue_json['author_association'] #"author_association": "OWNER",
    
    if author_role != 'OWNER':
        exit()
    
    prompt = f"issue title: {title}\nissue description: {body}"
    print("<prompt>")
    print(prompt)
    print("</prompt>)
