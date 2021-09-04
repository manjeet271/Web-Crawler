from ply.lex import lex
from ply.yacc import  yacc
import urllib.request
import urllib.error
import urllib.parse
import codecs,re

#GLOBAL DICTIONARY TO STORE MOVIE'S RECORD
result = {
        'MOVIE': '',
        'DIRECTOR':[],
        'WRITER':[],
        'PRODUCER':[],
        'LANGUAGE': '',
        'CAST': [],
        'STORYLINE': '',
        'BOXOFFICE': '',
        'RUNTIME': '',
        'GENRE': '',
        'PROVIDER': [],
        'LIKE': [],
        'URL': [],
        'CASTURL': [],
        'HIGH' : '',
        'LOW' : '',
        'BIRTHDAY': '',
        'OTHERMOVIE': [],
        'YEAR': []
        }

#TOKEN LIST
tokens = (
	'LMOVIE', 
    'BOXOFFICE',
	'LLANGUAGE',
    'LSTORY', 
	'RUNTIME',
    'CELEB',
    'LWRITER',
    'LPRODUCER',
    'LCAST',
    'RCAST',
    'GENRE',
    'LIKE',
    'PROVIDER',
    'URL',
    'PROFILE',
    'RATEDFILM',
    'BIRTHDAY',
    'OTHER',
    'YEAR',
    )

#TOKEN RULES:
def t_LMOVIE(t):
    r'<h1\sslot="title"\sclass="scoreboard__title"\sdata-qa="score-panel-movie-title">(.+)</h1>'
    #print(t)
    t.value = t.lexer.lexmatch.groups()[1]
    return t    


def t_BOXOFFICE(t):
    r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Box\sOffice\s\(Gross\sUSA\):</div>\n.*<div\sclass="meta-value"\sdata-qa="movie-info-item-value">(.+)</div>'
    grp = t.lexer.lexmatch.groups()
    #print(grp)
    t.value = grp[3]
    return t


def t_LLANGUAGE(t):
    r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Original\sLanguage:</div>\n.*<div\sclass="meta-value"\sdata-qa="movie-info-item-value">(.+)'
    grp = t.lexer.lexmatch.groups()
    #print(grp)
    t.value = grp[5]
    return t


def t_RUNTIME(t):
    r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Runtime:</div>\n.*\n.*\n(.*)'
    grp = t.lexer.lexmatch.groups()
    #print(grp)
    t.value = grp[7].strip(' ')
    return t

def t_LSTORY(t):
    r'<div\sid="movieSynopsis"\sclass="movie_synopsis\sclamp\sclamp-6\sjs-clamp"\sstyle="clear:both"\sdata-qa="movie-info-synopsis">\n(.*)'
    grp = t.lexer.lexmatch.groups()
    #print(grp)
    #print(grp[11].strip(' '))
    t.value = grp[9].strip(' ')
    return t


def t_LWRITER(t):
    r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Writer:</div>\n.*'
    return t

def t_CELEB(t):
    r'.*<a\shref=".*/celebrity/.*">(.*)</a>,?'
    grp = t.lexer.lexmatch.groups()
    t.value = grp[12]
    return t

def t_LPRODUCER(t):
    r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Producer:</div>\n.*'
    return t

def t_LCAST(t):
    r'<a\shref="\s.*/celebrity/.*\s"\sclass="unstyled\sarticleLink"\sdata-qa="cast-crew-item-link">\n.*\n.*<span\stitle="(.*)">'
    grp = t.lexer.lexmatch.groups()
    t.value = grp[15]
    return t

def t_RCAST(t):
    r'<span\sclass="characters\ssubtle\ssmaller"\stitle=".*">\n.*\n.*<br/?>\n.*\n([A-Za-z,\n\s]+)*'
    grp = t.lexer.lexmatch.groups()
    x = grp[17].split(',')
    rcast = []
    for i in range(len(x)):
        x[i] = x[i].replace('\n','')
        x[i] = x[i].strip(' ')
        rcast.append(x[i])
    t.value = rcast
    return t

def t_GENRE(t):
    r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Genre:</div>\n.*\n.*([a-z,\n\s]+)*'
    grp = t.lexer.lexmatch.groups()
    x = grp[19].split(',')
    genre = []
    for i in range(len(x)):
        x[i] = x[i].replace('\n','')
        x[i] = x[i].strip(' ')
        genre.append(x[i])
    t.value = genre
    return t

def t_LIKE(t):
    r'<span\sslot="title"\sclass="recommendations-panel__poster-title">(.*)</span>'
    grp = t.lexer.lexmatch.groups()
    t.value = grp[21]
    return t

def t_PROVIDER(t):
    r'<a\sclass="unstyled\sarticleLink"\shref=".*services=.*"\sdata-qa="dvd-streaming-link">(.*)</a>'
    grp = t.lexer.lexmatch.groups()
    t.value = grp[23]
    return t

def t_URL(t):
    r'<a\shref="(.*)"\sclass="recommendations-panel__poster-link">'
    grp = t.lexer.lexmatch.groups()
    t.value = grp[25]
    return t

def t_PROFILE(t):
    r'<a\shref="(.*)"\sdata-qa="cast-crew-item-img-link">'
    grp = t.lexer.lexmatch.groups()
    t.value = grp[27]
    return t

def t_RATEDFILM(t):
    r'<a\sclass="celebrity-bio__link"\shref=".*".*>.*\n(.*)'
    grp = t.lexer.lexmatch.groups()
    t.value = grp[29].strip(' ')
    return t

def t_BIRTHDAY(t):
    r'<p\sclass="celebrity-bio__item"\sdata-qa="celebrity-bio-bday">.*\n.*\n(.*)'
    grp = t.lexer.lexmatch.groups()
    t.value = grp[31].strip(' ')
    return t

def t_OTHER(t):
    r'<td\sclass="celebrity-filmography__title">.*\n.*\n.*<a\shref="/m/.*">(.*)</a>'       
    grp = t.lexer.lexmatch.groups()
    t.value = grp[33]
    return t

def t_YEAR(t):
    r'<td\sclass="celebrity-filmography__year">(.*)</td>'
    grp = t.lexer.lexmatch.groups()
    t.value = grp[35]
    return t

# Error handling rule
def t_error(t):
    t.lexer.skip(1)


# PARSING RULES:
def p_start(p):
	'''start : start provider
            | start moviename
            | start like 
            | start storyline 
            | start genre 
            | start language 
            | start director 
            | start producer 
            | start writer 
            | start box 
            | start runtime 
            | start cast 
            | start url
            | start casturl
            | start rated
            | start bday
            | start other
            | end
			 '''
	pass

def p_provider(p):
    '''provider : provider provid
                | provid '''
    pass

def p_provid(p):
    'provid : PROVIDER'
    result['PROVIDER'].append(p[1])
    pass
    
def p_moviename(p):
    'moviename : LMOVIE'
    result['MOVIE'] = p[1]
    pass

def p_like(p):
    '''like : like rlike
            | rlike'''
    pass

def p_rlike(p):
    'rlike : LIKE'
    result['LIKE'].append(p[1])
    pass

def p_storyline(p):
    'storyline : LSTORY'  
    result['STORYLINE'] = p[1]
    pass

def p_genre(p):
    'genre : GENRE'
    result['GENRE'] = p[1]

def p_language(p):
    'language : LLANGUAGE'
    result['LANGUAGE'] = p[1]
    pass

def p_director(p):
    '''director : director dir 
            | dir'''
    pass

def p_dir(p):
    'dir : CELEB'
    result['DIRECTOR'].append(p[1]) 

def p_producer(p):
    'producer : LPRODUCER rproducer'
    pass

def p_rproducer(p):
    '''rproducer : rproducer pceleb
               | pceleb '''
    pass

def p_pceleb(p):
    'pceleb : CELEB'
    result['PRODUCER'].append(p[1])
    pass

def p_writer(p):
    'writer : LWRITER rwriter'
    pass

def p_rwriter(p):
    '''rwriter : rwriter wceleb
               | wceleb '''
    pass

def p_wceleb(p):
    'wceleb : CELEB'
    result['WRITER'].append(p[1])
    pass

def p_box(p):
    'box : BOXOFFICE'
    result['BOXOFFICE'] = p[1]
    pass
    
def p_runtime(p):
    'runtime : RUNTIME' 
    result['RUNTIME'] = p[1] 
    pass

def p_cast(p):
    ''' cast : cast rcast
             | rcast '''
    pass

def p_rcast(p):
    'rcast : LCAST RCAST'
    result['CAST'].append((p[1],p[2]))

def p_url(p):
    '''url : url rurl
           | rurl '''
    pass

def p_rurl(p):
    'rurl : URL'
    result['URL'].append(p[1])

def p_casturl(p):
    '''casturl : casturl rcasturl
             | rcasturl'''
    pass

def p_rcasturl(p):
    'rcasturl : PROFILE'
    result['CASTURL'].append(p[1])

def p_rated(p):
    'rated : RATEDFILM RATEDFILM'
    result['HIGH'] = p[1]
    result['LOW'] = p[2]

def p_bday(p):
    'bday : BIRTHDAY'
    result['BIRTHDAY'] = p[1]

def p_other(p):
    '''other : other rother
            | rother'''
    pass

def p_rother(p):
    'rother : OTHER YEAR'
    result['OTHERMOVIE'].append(p[1])
    result['YEAR'].append(p[2])


def p_end(p):
    'end : '
    pass

         
def p_error(p):
    pass

c = -1 #GLOBAL VARIABLE IF c = -1 THEN USER INPUT OF GENRE AND MOVIE NAME
       #IF c = 0 THEN MOVIE WEBPAGE PARSING
       #IF c = 1 THEN CAST WEBPAGE PARSING
def main():
    #CLEARING DICTIONARY BEFORE EVERY RUN
    result['DIRECTOR'].clear()
    result['PRODUCER'].clear()
    result['WRITER'].clear()
    result['CAST'].clear()
    result['PROVIDER'].clear()
    result['LIKE'].clear()
    result['URL'].clear()
    result['CASTURL'].clear()

    global c
    if c==-1:
        #GENRE LINKS
        genre = {
        'Action & Adventure': "https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/",
        'Animation': "https://www.rottentomatoes.com/top/bestofrt/top_100_animation_movies/",
        'Drama': "https://www.rottentomatoes.com/top/bestofrt/top_100_drama_movies/",
        'Comedy': "https://www.rottentomatoes.com/top/bestofrt/top_100_comedy_movies/",
        'Mystery & Suspense': "https://www.rottentomatoes.com/top/bestofrt/top_100_mystery__suspense_movies/",
        'Horror': "https://www.rottentomatoes.com/top/bestofrt/top_100_horror_movies/",
        'Sci-Fi': "https://www.rottentomatoes.com/top/bestofrt/top_100_science_fiction__fantasy_movies/",
        'Documentary': "https://www.rottentomatoes.com/top/bestofrt/top_100_documentary_movies/",
        'Romance': "https://www.rottentomatoes.com/top/bestofrt/top_100_romance_movies/",
        'Classics': "https://www.rottentomatoes.com/top/bestofrt/top_100_classics_movies/"
        }
        
        #GENRE HTML PAGE DOWNLOAD
        for x in genre.keys():
            print("● %s" %(x))
        inp_genre = input('\nENTER ANY GENRE FROM THE ABOVE LIST:').strip(' ')
        
        while(1):
            try:
                response = urllib.request.urlopen(genre[inp_genre])
                break
            except:
                inp_genre = input('\nOOPS! YOU HAVE ENTERED A WRONG GENRE, ENTER AGAIN:').strip(' ')
                
        #MOVIE LIST
        print('\nLIST OF MOVIES OF GENRE %s ARE FOLLOWING:\n' %inp_genre)
        web_content = response.read()
        open(inp_genre+'.html', 'wb').write(web_content)

        list_lines = []
        dict_movie={}

        f = open(inp_genre+'.html', 'r')
        for x in f:
            list_lines.append(x)

        #EXTRACTING NAME OF MOVIES AND THEIR LINKS 
        l=0
        for l in range(len(list_lines)):
            p = re.findall('<a href="/m/.*" class="unstyled articleLink">',list_lines[l])
            if p:
                movie=""
                movielink=""
                x = list_lines[l].split('/')
                for c in x[2]:
                    if c=='"':
                        break
                    else:
                        movielink+=c
                q=list_lines[l+1][12:]
                for c in q:
                    if c=="<":
                        break
                    else:
                        movie+=c
                print("● %s" %(movie))
                dict_movie[movie] = movielink
                l+=2

        #MOVIE PAGE DOWNLOAD
        name = input("\nENTER ANY MOVIE NAME FROM THE ABOVE LIST:").strip(' ')
        while(1):
            try:
                movie_url = 'https://www.rottentomatoes.com/m/' + dict_movie[name]
                break
            except:
                name = input('\nOOPS! YOU HAVE ENTERED A WRONG MOVIE NAME, ENTER AGAIN:').strip(' ')

        r = urllib.request.urlopen(movie_url)
        open('movie_file'+'.html', 'wb').write(r.read())
        print("\nWEBPAGE FOR \'%s\' MOVIE HAS BEEN DOWNLOADED" %name)
        c = 0


    if c==0:
        fm = open("movie_file.html", "r")
    else:
        fm = open("cast_profile.html", "r")

    movieContent = fm.read() 
    lexer = lex()
    lexer.input(movieContent)
    parser = yacc()
    print('\nPLEASE WAIT! HTML FILE IS BEING PARSED')
    parser.parse(movieContent)

    #LOCAL DICTIONARY FOR STORING MOVIE RECORDS
    result1 = {
        'MOVIE': '',
        'DIRECTOR':[],
        'WRITER':[],
        'PRODUCER':[],
        'LANGUAGE': '',
        'CAST': [],
        'STORYLINE': '',
        'BOXOFFICE': '',
        'RUNTIME': '',
        'GENRE': '',
        'PROVIDER': [],
        'LIKE': [],
        'URL': [],
        'CASTURL': [],
        'HIGH' : '',
        'LOW' : '',
        'BIRTHDAY': '',
        'OTHERMOVIE': [],
        'YEAR': []
        }

    result1 = result.copy()
    result1['DIRECTOR'] = result['DIRECTOR'].copy()
    result1['PRODUCER'] = result['PRODUCER'].copy()
    result1['WRITER'] = result['WRITER'].copy()
    result1['CAST'] = result['CAST'].copy()
    result1['PROVIDER'] = result['PROVIDER'].copy()
    result1['LIKE'] = result['LIKE'].copy()
    result1['URL'] = result['URL'].copy()
    result1['CASTURL'] = result['CASTURL'].copy()
    result1['OTHERMOVIE'] = result['OTHERMOVIE'].copy()
    result1['YEAR'] = result['YEAR'].copy()

    
    if c == 0:
        #USER INPUT 
        print('\nENTER ANY FIELD FROM THE FOLLOWING LIST\n● Movie Name\n● Director\n● Writers\n● Producer\n● Original Language\n● Cast\n● Storyline\n● Box Office Collection\n● Runtime\n● YOU MIGHT ALSO LIKE\n● WHERE TO WATCH\n● Exit')
        e = 'N'
        while e != 'Y':
            choice = input('\nENTER YOUR CHOICE>').strip(' ')
            if choice.lower() == 'movie name':
                if result1['MOVIE'] == '':
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    print(result1['MOVIE'])

            elif choice.lower() == 'director':
                if len(result1['DIRECTOR']) == 0 :
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    for x in result1['DIRECTOR']:
                        print(x)
                    

            elif choice.lower() == 'writers':
                if len(result1['WRITER']) == 0:
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    for x in result1['WRITER']:
                        print(x)
                    

            elif choice.lower() == 'producer':
                if len(result1['PRODUCER']) == 0:
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    for x in result1['PRODUCER']:
                        print(x)
                    

            elif choice.lower() == 'original language':
                if result1['LANGUAGE'] == '':
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    print(result1['LANGUAGE'])
                    

            elif choice.lower() == 'cast':
                if len(result1['CAST']) == 0:
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    casturl_dict = {}
                    i=0
                    while i<len(result1['CAST']):
                        key = result1['CAST'][i][0]
                        value = result1['CASTURL'][i]
                        casturl_dict[key] = value
                        i+=1
                    print('CAST \t\t CHARACTER')
                    print('---- \t\t ---------')
                    for x in result1['CAST']:
                        print(x[0], '\t' ,x[1])
                    
                    cast_name = input('\nENTER NAME OF ANY ONE OF THE CAST MEMBER FROM THE ABOVE LIST:').strip(' ')
                    #DOWNLOADING CAST'S WEBPAGE
                    while(1):
                        try:
                            if 'https://www.rottentomatoes.com' not in casturl_dict[cast_name]:
                                new_url = 'https://www.rottentomatoes.com' + casturl_dict[cast_name]
                            else:
                                new_url = casturl_dict[cast_name]
                            break
                        except:
                            cast_name = input('\nOOPS! YOU HAVE ENTERED A WRONG CAST NAME, ENTER AGAIN:').strip(' ')
                    r = urllib.request.urlopen(new_url)
                    open('cast_profile'+'.html', 'wb').write(r.read())
                    print('\n\'%s\' PROFILE WEBPAGE HAS BEEN DOWNLOADED' %cast_name)
                    c = 1
                    #RECURSION
                    main()
                    print('\nYOU ARE NOW BACK TO THE \'%s\' MOVIE' %result1['MOVIE'])
                    print('\nENTER ANY FIELD FROM THE FOLLOWING LIST\n● Movie Name\n● Director\n● Writers\n● Producer\n● Original Language\n● Cast\n● Storyline\n● Box Office Collection\n● Runtime\n● YOU MIGHT ALSO LIKE\n● WHERE TO WATCH\n● Exit')



            elif choice.lower() == 'storyline':
                if result1['STORYLINE'] == '':
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    print(result1['STORYLINE'])
                    

            elif choice.lower() == 'box office collection':
                if result1['BOXOFFICE'] == '':
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    print(result1['BOXOFFICE'])
                    

            elif choice.lower() == 'runtime':
                if result1['RUNTIME'] == '':
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    print(result1['RUNTIME'])
                    
            elif choice.lower() == 'you might also like':
                if len(result1['LIKE']) == 0:
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    url_dict = {}
                    i=0
                    while i<len(result1['LIKE']):
                        key = result1['LIKE'][i]
                        value = result1['URL'][i]
                        url_dict[key] = value
                        print(key)
                        i+=1

                    
                    new_movie = input('\nENTER NAME OF MOVIE:').strip(' ')
                    while(1):
                        try:
                            if 'https://www.rottentomatoes.com' not in url_dict[new_movie]:
                                new_url = 'https://www.rottentomatoes.com' + url_dict[new_movie]
                            else:
                                new_url = url_dict[new_movie]
                            break
                        except:
                            new_movie = input('\nOOPS! YOU HAVE ENTERED A WRONG MOVIE NAME, ENTER AGAIN:').strip(' ')

                    r = urllib.request.urlopen(new_url)
                    open('movie_file'+'.html', 'wb').write(r.read())
                    print("\nWEBPAGE FOR \'%s\' MOVIE HAS BEEN DOWNLOADED" %new_movie)
                    c = 0  #TO PARSE NEW MOVIE'S WEBPAGE
                    main() #RECURSION 
                    print('\nYOU ARE NOW BACK TO THE \'%s\' MOVIE' %result1['MOVIE'])
                    print('\nENTER ANY FIELD FROM THE FOLLOWING LIST\n● Movie Name\n● Director\n● Writers\n● Producer\n● Original Language\n● Cast\n● Storyline\n● Box Office Collection\n● Runtime\n● YOU MIGHT ALSO LIKE\n● WHERE TO WATCH\n● Exit')

            elif choice.lower() == 'where to watch':
                if len(result1['PROVIDER']) == 0:
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    for x in result1['PROVIDER']:
                        print(x)
                    
            elif choice.lower() == 'exit':
                e = 'Y'
            else:
                print('WRONG CHOICE ENTER AGAIN')
    else:

        print('\n● Highest Rated film\n● Lowest Rated film\n● Birthday\n● His/Her other movies\n● Exit')
        e = 'N'
        while e != 'Y':
            choice = input('\nENTER YOUR CHOICE>').strip(' ')
            if choice.lower() == 'highest rated film':
                if result1['HIGH'] == '':
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    print(result1['HIGH'])

            elif choice.lower() == 'lowest rated film':
                if result1['LOW'] == '':
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    print(result1['LOW'])

            elif choice.lower() == 'birthday':
                if result1['BIRTHDAY'] == '':
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    print(result1['BIRTHDAY'])

            elif choice.lower() == 'his/her other movies':
                if len(result1['OTHERMOVIE']) == 0:
                    print('OOPS! THIS FIELD IS NOT PRESENT IN THE WEBPAGE')
                else:
                    flag = 0
                    year = input('ENTER YEAR:').strip(' ')
                    i=0
                    while i<len(result1['YEAR']):
                        if(int(year)<=int(result1['YEAR'][i])):
                            print(result1['OTHERMOVIE'][i])
                            flag = 1
                        i = i+1
                    if flag == 0:
                        print('THERE IS NO MOVIE RELEASED ON OR AFTER THIS YEAR')

            elif choice.lower() == 'exit':
                e = 'Y'
            else:
                print('WRONG CHOICE ENTER AGAIN')
    
if __name__ == '__main__':
	main()
    

