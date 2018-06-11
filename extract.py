import json
import glob
from tesserocr import PyTessBaseAPI, PSM
import difflib 


def distribution_right(expire,re_grant_by, variable, cutting, selling,forces, ships, aircraft):
	return {
		"expire": expire,
		"re_grant_by": re_grant_by,
		"variable": variable,
		"cutting": cutting,
		"selling":selling,
		"forces": forces,
		"ships":ships,
		"aircraft":aircraft
	}
def underlying_right(remake_cinema,remake_tv, live):
	return{
		"remake_cinema": remake_cinema,
		"remake_tv":remake_tv,
		"live":live
	}	

def film_length(tfMM,osMM):
	return{
		"35MM": tfMM,
		"16MM":osMM
	}
def schedule_of_all_films(id, run_no):
	return {
		"id": id,
		"run_no": run_no,
	}
def request(date, requested_by):
	return{
		"date":date,
		"requested_by": requested_by,
	}
def film_grant_details(WEG, grantor, ref_no):
	return {
		"WEG": WEG,
		"grantor":grantor,
		"ref_no":ref_no,
	}
def row(schedule_of_all_films,request,page,film_grant_details,
	title, distribution_right, underlying_right,film_length,running_time,
	production_year, tradeshow_date, UK_release_date, BW_color, UK_censor,
	contents, authors, producers,artists,directors):
	return {
	"schedule_of_all_films": schedule_of_all_films,
	"film_grant_details":film_grant_details,
	"request": request,
	"page":page,
	"title":title,
	"distribution_right":distribution_right,
	"underlying_right":underlying_right,
	"film_length":film_length,
	"running_time": running_time,
	"production_year": production_year,
	"tradeshow_date": tradeshow_date,
	"UK_release_date":UK_release_date,
	"BW_color": BW_color,
	"UK_censor":UK_censor,
	"content": contents,
	"author": authors,
	"producer": producers,
	"artist": artists,
	"director":directors,
}

def find_index(word, texts):
	try:
		words = difflib.get_close_matches(word, texts)[0]
		return texts.index(words)
	except:
		print "can not find index"

def find_index_list(word, texts):
	index_list = []
	for match in difflib.get_close_matches(word, texts):
		index_list.extend( [i for i, x in enumerate(texts) if x == match ])
	return set(index_list)
	

def process_text(text):
	text = text.replace('\n', ' ')
	# text.replace('7V','TV')
	list_text = text.split(' ')

	# schedule_of_all_films
	id = list_text[0]
	run_no = list_text[3]
	soaf = schedule_of_all_films(id, run_no)

	# film_grant_details
	date_index = find_index("DATE", list_text)
	weg_index = find_index(u'W\u2018E.G.',list_text )
	grantor_index = find_index('GRANTOR', list_text)
	ref_no_index = find_index('REF', list_text)
	weg = ' '.join(list_text[weg_index+2: date_index])
	grantor = ' '.join(list_text[grantor_index +2: ref_no_index])
	ref_no = list_text[ref_no_index+2]
	fgd  = film_grant_details(weg,grantor,ref_no)

	# request
	page_index = find_index("PAGE", list_text)
	request_index = find_index("REQUESTED", list_text)
	date = list_text[date_index+2:page_index]
	details_index  = find_index("FILM", list_text[request_index:])
	request_by = ' '.join(list_text[request_index+2: request_index+details_index])
	req = request(date, request_by)

	page = list_text[page_index+1]
	title_index = find_index("TITLE", list_text)
	distr_index = find_index("DISTRIBUTION", list_text[title_index:])
	title = ' '.join(list_text[title_index+2: title_index+distr_index])

	#distribution rights
	expire_index = find_index('EXPIRE', list_text)
	RE_index = find_index("RE", list_text)
	variable_index = find_index("VARIABLE", list_text)
	cutting_index = find_index("CUTTING", list_text)
	selling_index = find_index("SELLING", list_text)
	forces_index = find_index("FORCES", list_text)
	ship_index = find_index("SHIPS", list_text)
	aircraft_index = find_index("AIRCRAFT", list_text)
	expire  = list_text[expire_index+2]
	RE = grantor
	variable = list_text[variable_index+2]
	cutting = list_text[cutting_index+2]
	selling = list_text[selling_index+2]
	forces = list_text[forces_index+2]
	ships = list_text[ship_index+2]
	aircraft = list_text[aircraft_index+2]
	dr = distribution_right(expire, RE, variable, cutting, selling, forces, ships, aircraft)

	#underlying rights
	remake_index = find_index("REMAKE", list_text)
	remake_cinema_index = find_index("CINEMA", list_text[remake_index:])
	remake_tv_index = find_index("TV", list_text[remake_index:])
	live_index = find_index("LIVE", list_text[remake_index:])
	remake_cinema = list_text[remake_index+remake_cinema_index+2]
	remake_tv = list_text[remake_index+remake_tv_index+2]
	live = list_text[remake_index+live_index+2]
	ur = underlying_right(remake_cinema, remake_tv, live)

	#film length
	length_index = find_index("LENGTH", list_text)
	tfmm_index = find_index("35MM", list_text[length_index:])
	osmm_index = find_index("16MM", list_text[length_index:])
	tfmm  = ''.join(list_text[length_index+tfmm_index+2: length_index+tfmm_index+4])
	osmm  = ''.join(list_text[length_index+osmm_index+2: length_index+osmm_index+4])
	fl = film_length(tfmm, osmm)

	product_year = list_text[find_index("PRODUCTION", list_text)+3]
	tradeshow_date =  list_text[find_index("TRADESHOW", list_text)+3]
	running_index = find_index("RUNNING", list_text)
	BW_color = list_text[find_index("COLOUR", list_text)+2]
	UK_censor = list_text[find_index("CENSOR", list_text)+2:running_index ]
	UK_release_date = list_text[find_index("RELEASE", list_text) +3]
	running_time = list_text[running_index +3: running_index+find_index("UK", list_text[running_index:])]

	content_indexs =  find_index_list("CONTENT", list_text)
	author_indexs = find_index_list("AUTHOR", list_text)
	artist_indexs = find_index_list("ARTIST", list_text)
	director_indexs = find_index_list("DIRECTOR-", list_text)
	producer_indexs = find_index_list("PRODUCER-", list_text)

	contents, authors, artists, directors, producers = [],[],[],[],[]
	contents = [list_text[idx+2] for idx in content_indexs]
	authors = [' '.join(list_text[idx+2: idx+4 ] )for idx in author_indexs]
	artists = [' '.join(list_text[idx+2: idx+4 ]) for idx in artist_indexs]
	directors = [' '.join(list_text[idx+1: idx+3 ]) for idx in director_indexs]
	producers = [  ' '.join(list_text[idx+1: idx+3 ]) for idx in producer_indexs]

	# build the final data entry
	one_entry = row(soaf, fgd, req, page, title, dr, ur,fl, 
			running_time, product_year, tradeshow_date, UK_release_date, BW_color, UK_censor,
			contents,authors,producers,artists,directors )

	return one_entry

if __name__== "__main__":
	images = glob.glob("*.jpg")
	outfile = open('output.txt', 'w+')
    
	with PyTessBaseAPI(psm=PSM.SINGLE_BLOCK) as api:
	    for img in images:
	        api.SetImageFile(img)
	        text = api.GetUTF8Text()
	        one_entry = process_text(text)
	        json.dump(one_entry, outfile)
        	




