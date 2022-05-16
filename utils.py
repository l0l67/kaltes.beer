import markdown, hashlib, sys, os, re
import DB

def markdownToHtml(md):
    return markdown.markdown(md)

def getChecksum(content):
    return hashlib.md5(content.encode()).hexdigest()

PATH = 'posts/'
def checkForNewPosts():
    for file in os.listdir(PATH):
        if not file.startswith('.'):
            file = PATH + file
            updatePostIfChanged(file)

def updatePostIfChanged(filename):
    with open(filename) as f:
        content = str(f.read())
        title = getTitleFromMarkdown(content)
        postName = filename.replace('.md', '')
        checksum = getChecksum(content)
        
        oldPost = DB.getPostByPostName(postName)
        
        if len(oldPost) == 0:
            DB.addPost(postName, title, checksum, markdownToHtml(content))
            
            print(f"added new post: {title}")
        else:
            oldPost = oldPost[0]

            if oldPost[1] != checksum:
                DB.updatePost(oldPost[0], title, checksum, markdownToHtml(content))

                print(f"updated post: {title}")

def getTitleFromMarkdown(markdown):
    try:
        return re.search('<!-- (.*) -->', markdown).group(1)
    except AttributeError:
        print('No title found!')
        return 'No Title'
        


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'update':
            print('Updating...')
            checkForNewPosts()
    except IndexError:
        pass