import markdown, hashlib, os, re
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
        checksum = getChecksum(content)
        
        oldPost = DB.getPostIdFromFilename(filename)
        
        if len(oldPost) == 0:
            DB.addPost(filename, title, checksum, markdownToHtml(content))
        else:
            oldPost = oldPost[0]

            if oldPost[1] != checksum:
                print(f"updating: {oldPost[0]}")

                DB.updatePost(oldPost[0], title, checksum, markdownToHtml(content))

def getTitleFromMarkdown(markdown):
    return re.search('<!--(.*)-->', markdown).group()
