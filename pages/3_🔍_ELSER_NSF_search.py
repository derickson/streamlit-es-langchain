import streamlit as st

from datetime import datetime

from resources import get_es

st.set_page_config(layout="wide")


es = get_es()

# ######################
#     ______                           __  __  _            
#    / ____/___  _________ ___  ____ _/ /_/ /_(_)___  ____ _
#   / /_  / __ \/ ___/ __ `__ \/ __ `/ __/ __/ / __ \/ __ `/
#  / __/ / /_/ / /  / / / / / / /_/ / /_/ /_/ / / / / /_/ / 
# /_/    \____/_/  /_/ /_/ /_/\__,_/\__/\__/_/_/ /_/\__, /  
#                                                  /____/   
# ######################

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

def format_date_for_humans(date_str):
    # Parse the input string into a datetime object
    parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    # Format the datetime object into a human-readable format
    formatted_date = parsed_date.strftime("%B %d, %Y")
    return formatted_date


# ######################
#     ________           __  _     
#    / ____/ /___ ______/ /_(_)____
#   / __/ / / __ `/ ___/ __/ / ___/
#  / /___/ / /_/ (__  ) /_/ / /__  
# /_____/_/\__,_/____/\__/_/\___/  
# ######################

def countDocs():
    count = es.count(index="nsf_awards")["count"]
    st.session_state.docCount = count

def clearCount():
    if "docCount" in st.session_state:
        del st.session_state["docCount"]
    if "nsf_award_search" in st.session_state:
        del st.session_state["nsf_award_search"]
    if "incuded_panelists" in st.session_state:
        st.session_state.incuded_panelists = {}
    if "nsf_award_keyword_search" in st.session_state:
        del st.session_state.nsf_award_keyword_search

def runKeywordSearch(text_query):
    if(text_query and text_query!= ""):
        keyword_query = {
            "match": {
                "AbstractNarration": text_query
            }
        }
    else:
        keyword_query = {"match_all": {}}


    fields= [
        "AwardEffectiveDate",
        "Investigator_PI_FULL_NAME",
        "Institution_Name",
        "AbstractNarration",
        "AwardTitle"
      ]
    
    index = "nsf_awards_semantic"
    resp = es.search(index=index,
                     query=keyword_query,
                     fields=fields,
                     size=10,
                     source=False)
    st.session_state.nsf_award_keyword_search = resp

def runSearch(text_query):
    


    elser_query = {
      "text_expansion": {
        "AbstractNarration_ml.tokens": {
          "model_id": ".elser_model_1",
          "model_text": text_query
        }
      }
    }
    text_query = {
        "match": {
            "AbstractNarration": text_query
        }
    }
    sub_searches = {
        "sub_searches": [
            {"query": elser_query},
            {"query": text_query}
        ]
    }


    fields= [
        "AwardEffectiveDate",
        "Investigator_PI_FULL_NAME",
        "Institution_Name",
        "AbstractNarration",
        "AwardTitle"
      ]

    body = {
        "sub_searches": [
            {
                "query": text_query
            },
            {
                "query": elser_query
            }
        ],
        "rank": {
            "rrf": {
                "window_size": 50,
                "rank_constant": 20
            }
        },
        "fields" : fields,
        "_source": False,
        "size": 10
    }




    index = "nsf_awards_semantic"
    resp = es.perform_request("POST", f"/{index}/_search", headers={"content-type": "application/json", "accept": "application/json"}, body=body)

    # resp = es.search(index="nsf_awards_semantic",
    #                  query=elser_query,
    #                  fields=fields,
    #                  size=10,
    #                  source=False)
    
    st.session_state.nsf_award_search = resp


"### 🚧 Elasticsearch Prototype Workbench 🚧"
"Keyword vs Semantic Search"
st.markdown("Semantic search is ELSER + BM25 with reciprocal rank fusion. For a big chunk scientific search text, grab an abstract from <a href='https://arxiv.org/list/astro-ph/recent'>Arxiv</a>",unsafe_allow_html=True)

tab_keyword, tab_semantic  = st.tabs(["Keyword Search", "Semantic Search"])



# ######################
#  ___   _  _______  __   __  _     _  _______  ______    ______  
# |   | | ||       ||  | |  || | _ | ||       ||    _ |  |      | 
# |   |_| ||    ___||  |_|  || || || ||   _   ||   | ||  |  _    |
# |      _||   |___ |       ||       ||  | |  ||   |_||_ | | |   |
# |     |_ |    ___||_     _||       ||  |_|  ||    __  || |_|   |
# |    _  ||   |___   |   |  |   _   ||       ||   |  | ||       |
# |___| |_||_______|  |___|  |__| |__||_______||___|  |_||______| 
# ######################

with tab_keyword:
    "# Keyword Search for NSF Awards"
    col1, col2 = st.columns([6,1])
    with col1:
        keyword_search_box = st.text_area("Search Input", "")
    with col2:
        ""
        if st.button("🔙", type="secondary", key="resetKeyword"):
            clearCount()
        if st.button("🔎", type="secondary", key="searchKeyword"): 
            countDocs()
            runKeywordSearch(keyword_search_box)

    st.markdown("<hr/>", unsafe_allow_html=True)
    if "nsf_award_keyword_search" in st.session_state:
        "## Similar NSF Award PIs"
        # already_check_boxes = {}
        hits = st.session_state.nsf_award_keyword_search["hits"]["hits"]
        for hit in hits:
            score = hit["_score"]
            date = hit["fields"]["AwardEffectiveDate"][0]
            name = hit["fields"]["Investigator_PI_FULL_NAME"][0] if "Investigator_PI_FULL_NAME" in hit["fields"] else "<No PI on Award>"
            institution = hit["fields"]["Institution_Name"][0]
            abstract = hit["fields"]["AbstractNarration"][0]
            title = hit["fields"]["AwardTitle"][0]
            # col1, col2 = st.columns([3,1])
            # with col1:
            f"### {name}"
            # with col2:
            #     key = f"{name}"
            #     if key not in already_check_boxes:
            #         previous_val = getPanelistState(key)
            #         already_check_boxes[key] = st.toggle("Include in panel",value=previous_val,key=key, on_change=togglePanelist, args=(key, ))
            #     else:
            #         st.markdown("*author already listed above*")
            st.markdown(f"#### {title}")
            if score:
                st.markdown(f"Score: {score} <br/> {institution} <br/> {format_date_for_humans(date)}",unsafe_allow_html=True)
            else:
                st.markdown(f"{institution} <br/> {format_date_for_humans(date)}",unsafe_allow_html=True)
            with st.expander("See full abstract"):
                st.markdown(abstract,unsafe_allow_html=True)

# ######################
#  _______  _______  __   __  _______  __    _  _______  ___   _______ 
# |       ||       ||  |_|  ||   _   ||  |  | ||       ||   | |       |
# |  _____||    ___||       ||  |_|  ||   |_| ||_     _||   | |       |
# | |_____ |   |___ |       ||       ||       |  |   |  |   | |       |
# |_____  ||    ___||       ||       ||  _    |  |   |  |   | |      _|
#  _____| ||   |___ | ||_|| ||   _   || | |   |  |   |  |   | |     |_ 
# |_______||_______||_|   |_||__| |__||_|  |__|  |___|  |___| |_______|
# ######################

with tab_semantic:
    ### Inputs
    "# Semantic Search for NSF Awards"
    col1, col2 = st.columns([6,1])
    with col1:
        text_search_box = st.text_area("Abstract Text", "")
    with col2:
        ""
        if st.button("🔙", type="secondary"):
            clearCount()
        if st.button("🔎", type="primary", key="searchButton"): 
            countDocs()
            runSearch(text_search_box)
    


    ### Search Results

    
    def togglePanelist(key):
        if key in st.session_state.incuded_panelists:
            del st.session_state.incuded_panelists[key]
            # st.session_state.incuded_panelists[key] = not st.session_state.incuded_panelists[key]
        else:
            st.session_state.incuded_panelists[key] = True
    def getPanelistState(key):
        if key in st.session_state.incuded_panelists:
            return st.session_state.incuded_panelists[key]
        else:
            return False
    def initialize_and_describe_panel():
        if "incuded_panelists" not in st.session_state:
            st.session_state.incuded_panelists = {}
        else:
            "## Panelists"
            if len(st.session_state.incuded_panelists) == 0:
                st.markdown("*Panel is currently empty*")
            else:
                
                chicklet = "<div>"
                for key in st.session_state.incuded_panelists:
                    chicklet = chicklet + f"<span class='panelist'>{key}</span>"
                chicklet = chicklet + "</div>"
                st.markdown(chicklet,unsafe_allow_html=True)
    initialize_and_describe_panel()
    st.markdown("<hr/>", unsafe_allow_html=True)

    if "docCount" in st.session_state:
        st.markdown(f"Searching on {'{:,}'.format(st.session_state.docCount)} past awards:")



    if "nsf_award_search" in st.session_state:
        "## Similar NSF Award PIs"
        already_check_boxes = {}
        hits = st.session_state.nsf_award_search["hits"]["hits"]
        for hit in hits:
            score = hit["_score"]
            date = hit["fields"]["AwardEffectiveDate"][0]
            name = hit["fields"]["Investigator_PI_FULL_NAME"][0] if "Investigator_PI_FULL_NAME" in hit["fields"] else "<No PI on Award>"
            institution = hit["fields"]["Institution_Name"][0]
            abstract = hit["fields"]["AbstractNarration"][0]
            title = hit["fields"]["AwardTitle"][0]
            col1, col2 = st.columns([3,1])
            with col1:
                f"### {name}"
            with col2:
                key = f"{name}"
                if key not in already_check_boxes:
                    previous_val = getPanelistState(key)
                    already_check_boxes[key] = st.toggle("Include in panel",value=previous_val,key=key, on_change=togglePanelist, args=(key, ))
                else:
                    st.markdown("*author already listed above*")
            st.markdown(f"#### {title}")
            if score:
                st.markdown(f"Score: {score} <br/> {institution} <br/> {format_date_for_humans(date)}",unsafe_allow_html=True)
            else:
                st.markdown(f"{institution} <br/> {format_date_for_humans(date)}",unsafe_allow_html=True)
            with st.expander("See full abstract"):
                st.markdown(abstract,unsafe_allow_html=True)


