# Metadata_processor

In this repo, I describe the metadata structure and preprocessing methods

### Defination of the metadata structure

meta_data_struct = {
	"schedule_of_all_films": {
		id: str,
		"run_no": int
	}
	"film_grant_details":{
		"WEG": str,
		"grantor":str,
		"ref_no":str,
	}
	"request": {
		"requested_by":str,
		"date":str,
	}
	"page":int,
	"title":str,
	"distribution_right":{
		"expire": str,
		"re_grant_by": str,
		"variable": bool,
		"cutting": bool,
		"selling":bool,
		"forces": bool,
		"ships":bool,
		"aircraft":bool
	},
	"underlying_right":{
		"remake_cinema": str,
		"remake_tv":str,
		"live":str
	},
	"file_length":{
		"35MM": str,
		"16MM":str
	},
	"running_time": str,
	"production_year": int,
	"tradeshow_date": str,
	"UK_release_date": str,
	"BW_color": str,
	"UK_censor":str,
	"content": [str],
	"author": [str],
	"producer": [str],
	"artist": [str],
	"director":[str],
}

### Image to text

I used Tesseract python interface -- tesserocr, where I set the segmentation argument to "single_block". This will let the reader read the text from left to right line by line. 

### Text Processing

1. Generality 

Since there is only one sample for me to create the text processing algorithm. I tried to make it as general as possible. For example, rather than matching the exact word, I used similar matching method "difflib.get_close_matches", in case that the image to text process will cause some typo of some words.  This method can be applied to any number of files, from 1 to 100000. 

2. Scalability 

I tried to implement the metadata enrity following the idea of object-oriented-programming, where I created several classes to form the final big class. This can be easily modified and scaled in the future. 

3. comp
