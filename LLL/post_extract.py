import xml.etree.ElementTree as ET
import sqlite3
import datetime
import re

F = datetime.datetime.strftime
P = datetime.datetime.strptime

#Connect with the XML - Source name has been changed for clients privacy.
tree = ET.parse('XML_DB\LLL.WordPress.2023-08-05 posts.xml')
root = tree.getroot()

#creates DB 
con = sqlite3.connect('post_db_separate.db')
cur = sqlite3.Cursor(con)

#creates SQL Tables if one doesn't exists
with open('create_table.sql') as f:
    create_table =  f.read()
cur.executescript(create_table)

#Holds Data - whilst looping through xml
tw = {} # tw = to_write = Holds data to write, from XML extract
tl = [] # tl = tag_list = holds list of #tags

# Parse Date string 'pubDate'
def conv(x):
    date = P(x, '%a, %d %b %Y %H:%M:%S %z')
    return date

# Enumerate through the XML subset and convert data in to json / dictionary
def report(tw, tl):
    for count, child in enumerate(root[0]):
        if child.tag == 'item':
            tw['id'] = count

            for it in child:

                if it.tag.lower() == 'title':
                    tw['title'] = it.text

                if it.tag.lower() == '{http://purl.org/rss/1.0/modules/content/}encoded':
                    # Separate post by p Tag
                    tw['post_text'] = "  ".join(re.findall("<p>" +".*" + "</p>", str(it.text)))

                    # Remove Comments and Keep any other tags to be reviewed and re added to the post later. 
                    tw['post_extra'] = re.sub("<!--" +".*" + "-->", "" , re.sub("<p>" +".*" + "</p>", "" , str(it.text))).strip()

                if it.tag.lower() == '{http://wordpress.org/export/1.2/excerpt/}encoded':
                    tw['post_excerpt'] = it.text

                if it.tag.lower() == 'category':
                    tl.append(it.text)

                if it.tag.lower() == 'pubdate':
                    if it.text is not None:
                        tw['pub_date'] = F(conv(it.text), '%Y-%m-%d %H:%M:%S')
                    else: 
                        tw['pub_date'] = ""

                if it.tag.lower() == '{http://wordpress.org/export/1.2/}post_date':
                    tw['post_date'] = it.text

                if it.tag.lower() == '{http://wordpress.org/export/1.2/}post_modified':
                    tw['post_modified'] = it.text

                if 'category' in it.attrib.values():
                    tw['category'] = it.text

            # te = to execute = data to write
            te = (tw['title'], tw['post_text'], tw['post_extra'], tw['post_excerpt'], tw['category'], tw['pub_date'], tw['post_date'], tw['post_modified'], tw['id']) 
            
            
            cur.execute("INSERT INTO post (post_title, post_blog_post, post_blog_extra, post_excerpt, post_category, post_pub_date, post_create_date, post_mod_date, post_tag_id) VALUES (?,?,?,?,?,?,?,?,?)", te)
            for i in tl:
                cur.execute("INSERT INTO hash (hash_label, hash_post_id) VALUES (?, ?)", (i, tw['id']))
            con.commit()

            # clear the data on the Dictionary to start again.
            tw = {}
            tl = []

result = report(tw, tl)

# a = ""
# while a != 'n':
#     a = input("Next Record --------------------:")
#     if a != 'n':
#         next(result)
#         print("te")

            

con.close()