import json
import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import requests
import pickle
import seaborn as sns
import networkx.algorithms as nx_alg
import scipy as sp
from scipy.stats import pearsonr
import pandas as pd


#g = Github("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")

#for repo in g.get_user().get_repos():
    #print(repo.name)
    #repo.edit(has_wiki=False)
    # to see all the available attributes and methods
    #print(dir(repo))

#for repo in g.get_user().get_repos():
#    CONTR = [repo.get_contributors()]
#    #print(repo.name, repo.get_contributors())
#    print(CONTR)

# setup owner name , access_token, and headers
#owner='igraph'

access_token='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'
# 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
#access_token='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'
#headers = {'Authorization':"Token "+access_token}
headers = {'Authorization': 'token ' + access_token,
           'Accept': 'application/vnd.github+json',
           'Accept': 'application/vnd.github.v3.star+json'
           }

USER_NAME = 'qier222'
REPO_NAME = 'YesPlayMusic'

'''

//printing all the contributors of the project

repos=[]
for page_num in range(10):
    try:
    # to find all the repos' names from each page
        url=f"https://api.github.com/users/{owner}/repos?page={page_num}"
        repo=requests.get(url,headers=headers).json()
        repos.append(repo)
    except:
        repos.append(None)


all_repo_names=[]
for page in repos:
    for repo in page:
        try:
            all_repo_names.append(repo['full_name'].split("/")[1])
        except:
            pass


#print(all_repo_names)

all_contributors=[] # create an empty coontainer

for repo_name in all_repo_names:
    url = f"https://api.github.com/repos/{owner}/{repo_name}/contributors"
# make the request and return the json
    contributors= requests.get(url,headers=headers).json()
    all_contributors.append(contributors)


#print(all_contributors[0])

names=[]
counts=[]
for repo in all_contributors:
    for contributor in repo:
        try:
            name=contributor['login']
            count=contributor['contributions']
            names.append(name)
            counts.append(count)
        except:
            None


#print(len(names))

# create a dataframe and store the contrbutors' names and their contribution counts
mydata=pd.DataFrame()
mydata['contributor_name']=names
mydata['counts']=counts
# Then obtain unique names with sum of their contribution counts
mydata=mydata.groupby('contributor_name')["counts"].sum().reset_index().sort_values(by='counts',ascending=False)
# drop None / missing values
mydata=mydata.dropna(axis=0).reset_index().drop(columns='index')
# get top 10 contributiors
#print(mydata.head(10)) # top 10 contributors

mydata.to_csv("my_data.csv")'''

#getting acces to the all issue list

name_owner = "igraph"
repo_project = "igraph"

# url command

#url = "https://api.github.com/repos/" + name + "/" + repo +"/issues?per_page=100&page=1"

#making request for open issues

def open_and_closed_issues(name, repo):

  url = "https://api.github.com/repos/" + name + "/" + repo +"/issues?per_page=100&page=1&state=open"
  print(url)
  res=requests.get(url,headers=headers)
  issues=res.json()

  while 'next' in res.links.keys():
    res=requests.get(res.links['next']['url'],headers=headers)
    issues.extend(res.json())

  print(len(issues))

#making request for closed issues

  url = "https://api.github.com/repos/" + name + "/" + repo +"/issues?per_page=100&page=1&state=closed"
  print(url)
  res2=requests.get(url, headers=headers)
  issues2=res2.json()

  while 'next' in res2.links.keys():
    res2=requests.get(res2.links['next']['url'],headers=headers)
    issues2.extend(res2.json())

  print(len(issues2))

  issues.extend(issues2) #adding open and closed issues together

  print(len(issues))

  issues_string = json.dumps(issues)
  json_object = json.loads(issues_string)
  json_formatted_str = json.dumps(json_object, indent=2) #transforming issues to the string

  #printing the file with open and closed issues

  issues_file_name = "Output_open_and_closed_issues_" + name + "_" + repo + ".txt"

  with open(issues_file_name, "w") as text_file:
    text_file.write(json_formatted_str)

def created_at(name, repo):

  url = "https://api.github.com/repos/" + name + "/" + repo
  print(url)
  res = requests.get(url, headers=headers)
  repo_info = res.json()

  date = str(repo_info['created_at'])

  print(date)

  created_at_array = [(n) for n in date.strip().split('-')]

  print(created_at_array[1])
  print(created_at_array[0])

def list_of_edges_for_each_month(name1, repo1):

  url = "https://api.github.com/repos/" + name1 + "/" + repo1
  #print(url)
  res = requests.get(url, headers=headers)
  repo_info = res.json()

  date = str(repo_info['created_at'])
  created_at_array = [(n) for n in date.strip().split('-')]
  month = int(created_at_array[1])
  year = int(created_at_array[0])

  issues_file_name1 = "Output_open_and_closed_issues_" + name1 + "_" + repo1 + ".txt"

  #labels_list_file_name = "biological_projects_networks/biological_networks_labes/labels_list_file_" + name1 + "_" + repo1 + "_chain_thread.txt"

  #labelslistfile = open(labels_list_file_name, 'w')

  #creating list of lists of comments

  with open(issues_file_name1) as json_file:
    data = json.load(json_file) #data is a list

  dates = []
  #list of creators of the issues, all issuers who started the issues in the ordered array
  ids_of_issuers = []

  for i in range(len(data)):
    date = str(data[i]['created_at'])
    created_at_array = [(n) for n in date.strip().split('-')]
    pair = [created_at_array[1], created_at_array[0]]
    array_data = [data[i]['user']['id'], pair]
    ids_of_issuers.append(array_data)
    #dates.append(pair)
    dates.append(date)
    #labelslistfile.write("%s %s\n" % (str(data[i]['user']['id']), str(data[i]['author_association'])))

  #list of commenters, commenters, who commented for every issuer in the list of issuers

  #edge_list_file_name = "physics_projects_networks\\physics_networks_chain_list\\edge_list_file_" + name1 + "_" + repo1 + "_chain_thread.txt"

  #myedgelistfile = open(edge_list_file_name, 'w')

  #commenters_file_name = "Comments_list_of_lists_with_date_pair_" + name1 + "_" + repo1 + ".txt"

  #myfile = open(commenters_file_name, 'w')

  # file to record the lables

  #labels_list_file_name = "biological_projects_networks\\biological_networks_first_portion_labes\\labels_list_file_" + name1 + "_" + repo1 + "_chain_thread.txt"

  #mylabelslistfile = open(labels_list_file_name, 'w')

  ids_of_commenters = []
  list_of_ids_of_commenters = []

  comments = []

  for k in range(len(data)):

    print(str(k))
    url = data[k]['comments_url']
    print(url)
    res = requests.get(url, headers=headers)
    comments = res.json()

    comments_string = json.dumps(comments)
    comments_json_object = json.loads(comments_string)
    comments_json_formatted_str = json.dumps(comments_json_object, indent=2)  # transforming issues to the string

    # printing the file with comments

    file_name = "Comments_for_issues_" + str(k) + ".txt"

    with open(file_name, "w") as text_file:
      text_file.write(comments_json_formatted_str)

    with open(file_name) as json_file:
      comments_list = json.load(json_file) #data is a list

    ids_of_commenters = []

    for j in range(len(comments_list)):
      date = str(comments_list[j]['created_at'])
      created_at_array = [(n) for n in date.strip().split('-')]
      pair = [created_at_array[1], created_at_array[0]]
      array_commenters = [comments_list[j]['user']['id'], pair]
      ids_of_commenters.append(array_commenters) # adding id of commenter to the list ids_of_commenters
      #dates.append(pair)
      dates.append(date)
      #labelslistfile.write("%s %s\n" % (str(comments_list[j]['user']['id']), str(comments_list[j]['author_association'])))

    #comments_list.clear()

    #for r in range(len(ids_of_commenters)):
    #  myedgelistfile.write("%s %s\n" % (str(ids_of_commenters[r]), str(ids_of_issuers[k])))

    #connecting every first commenter to the issuer

    #if (len(ids_of_commenters) >= 1):
      #myedgelistfile.write("%s %s\n" % (str(ids_of_commenters[0]), str(ids_of_issuers[k])))

    #for m in range(len(ids_of_commenters)):
    #  v = m
    #  for l in range(0,v):
    #    myedgelistfile.write("%s %s\n" % (str(ids_of_commenters[v]),str(ids_of_commenters[l])))

    #if(len(ids_of_commenters) >= 2):
      #for m in range(1, len(ids_of_commenters)):
        #myedgelistfile.write("%s %s\n" % (str(ids_of_commenters[m]),str(ids_of_commenters[m-1])))

    list_of_ids_of_commenters.append(ids_of_commenters) # adding ids_of_commenters to the list list_of_ids_of_commenters

    os.remove(file_name) # removing created file, to not store all the files in the directory

    # printing commenters lists

    #myfile.write("%s\n" % str(ids_of_issuers[k]))
    #myfile.write("%s\n" % str(list_of_ids_of_commenters[k]))

    # end for #

  #myfile.close()
  #myedgelistfile.close()
  #mylabelslistfile.close()
  #labelslistfile.close()

  print(len(ids_of_issuers))
  print(len(list_of_ids_of_commenters))

  #collecting the dates from all of the comments

  dates_single = []  # the list of dates without doubles

  for date_pair in dates:
    if date_pair not in dates_single:
      dates_single.append(date_pair) #single dates

  #for date_pair in dates_single:
    #print(date_pair)

  dates_single_list = list(dates_single)

  dates_single_list.sort() # we sorted the dates

  #print(dates_single_list)

  dates_month_year = []

  for date_element in dates_single_list:
    created_at_array = [(n) for n in date_element.strip().split('-')]
    pair = [created_at_array[1], created_at_array[0]]
    dates_month_year.append(pair)

  #dates_month_year_list = list(dates_month_year)

  dates_month_year_single = []

  for date_pair in dates_month_year:
    if date_pair not in dates_month_year_single:
      dates_month_year_single.append(date_pair) #single dates

  for date_pair in dates_month_year_single:
    print(date_pair)

  #print(type(dates_month_year_single[0]))

  edge_list_for_date = []

  for date_pair in dates_month_year_single:

    #print(date_pair)

    edge_list_for_current_date = []

    # file with the network for each date

    #DATE_PAIR_file_name = "biological_projects_networks/networks_for_the_date/EDGE_LIST_" + name1 + "_" + repo1 + "_" + date_pair[0] + "_" + date_pair[1] + ".txt"
    #datepairfile = open(DATE_PAIR_file_name, 'w')

    for l in range(len(ids_of_issuers)):  # for each issuer

      # for l issue

      issuer_node = ids_of_issuers[l][0]
      #print(issuer_node)
      issuer_date = ids_of_issuers[l][1]
      #print(issuer_date)

      #print("len(list_of_ids_of_commenters[l]) = " + str(len(list_of_ids_of_commenters[l])))

      if (issuer_date == date_pair):

        #print("tada!!!!")

        if (len(list_of_ids_of_commenters[l]) == 0):  # array of commenters
          continue

        if (len(list_of_ids_of_commenters[l]) >= 1):  # we have just one comment
          fist_comment = list_of_ids_of_commenters[l][0]

          comment_node = fist_comment[0]  # inside the comment element, 0 - node, 1 - date
          comment_date = fist_comment[1]

          if (comment_date == date_pair):
            #datepairfile.write("%s %s\n" % (str(comment_node), str(issuer_node)))
            pair = [comment_node, issuer_node]
            edge_list_for_current_date.append(pair)

        if (len(list_of_ids_of_commenters[l]) >= 2):  # we have 2 and more comments, starting form the 1 element

          for m in range(1, len(list_of_ids_of_commenters[l])):

            m_comment = list_of_ids_of_commenters[l][m]
            previous_m_comment = list_of_ids_of_commenters[l][m - 1]

            m_comment_node = m_comment[0]
            m_comment_date = m_comment[1]

            previous_m_comment_node = previous_m_comment[0]
            previous_m_comment_date = previous_m_comment[1]

            if ((m_comment_date == date_pair) & (previous_m_comment_date == date_pair)):
              #datepairfile.write("%s %s\n" % (str(m_comment_node), str(previous_m_comment_node)))
              pair = [m_comment_node, previous_m_comment_node]
              edge_list_for_current_date.append(pair)

      if (issuer_date != date_pair):

        if (len(list_of_ids_of_commenters[l]) == 0):  # array of commenters
          continue

        if (len(list_of_ids_of_commenters[l]) == 1):  # array of commenters
          continue

        if (len(list_of_ids_of_commenters[l]) >= 2):  # we have 2 and more comments, starting form the 1 element

          for m in range(1, len(list_of_ids_of_commenters[l])):

            m_comment = list_of_ids_of_commenters[l][m]
            previous_m_comment = list_of_ids_of_commenters[l][m - 1]

            m_comment_node = m_comment[0]
            m_comment_date = m_comment[1]

            previous_m_comment_node = previous_m_comment[0]
            previous_m_comment_date = previous_m_comment[1]

            if ((m_comment_date == date_pair) & (previous_m_comment_date == date_pair)):
              #datepairfile.write("%s %s\n" % (str(m_comment_node), str(previous_m_comment_node)))
              pair = [m_comment_node, previous_m_comment_node]
              edge_list_for_current_date.append(pair)

    edge_list_for_date.append(edge_list_for_current_date)

  #datepairfile.close()

  #print(len(edge_list_for_date))

  #for element in edge_list_for_date:
    #print(element)

  edge_list_for_date_repetitions = []

  for list_date in edge_list_for_date:

    list_date_self_loops = []

    for pair in list_date:  # now we are going inside of every pair of line_array
      x, y = pair[0], pair[1]
      if (x != y):
        list_date_self_loops.append([x, y])  # creating the list of edges without self-loops


    list_date_double_edges = []

    for pair in list_date_self_loops:  # now we are going inside of every pair of line_array
      if pair not in list_date_double_edges:
        list_date_double_edges.append(pair)

    edge_list_for_date_repetitions.append(list_date_double_edges)

  #print(len(edge_list_for_date_repetitions))

  #for element in edge_list_for_date_repetitions:
    #print(element)

  # creating the list with the history for each month

  edge_list_for_month_history = []

  edge_list_for_month_history.append(edge_list_for_date_repetitions[0])

  for i in range(1, len(edge_list_for_date_repetitions)):

    listk = []

    for j in range(0, i+1):
      for pair in edge_list_for_date_repetitions[j]:
        listk.append(pair)

    edge_list_for_month_history.append(listk)

  #for element in edge_list_for_month_history:
    #print(element)

  #list1 = [[[55, 60]], [[1, 2], [1, 2]], [[2, 3], [4, 5]], [[5, 6], [8, 9]], [], [[5, 6], [8, 9], [7, 5]], []]
  #list2 = []
  #list2.append(list1[0])

  #for i in range(1, len(list1)):
    #listk = []
    #for j in range(0, i+1):
      #for pair in list1[j]:
        #listk.append(pair)
      #for k in range(0, len(list1[j])):
        #listk.append(list1[j][k])
    #list2.append(listk)

  # for k in range(0, len(edge_list_for_date_repetitions[j])):
  #   listk.append(edge_list_for_date_repetitions[j][k])

  # deleting double edges in edge_list_for_month_history

  edge_list_for_month_history_repetitions = []

  for list_month_history in edge_list_for_month_history:

    list_month_history_double_edges = []

    for pair in list_month_history:  # now we are going inside of every pair of line_array
      if pair not in list_month_history_double_edges:
        list_month_history_double_edges.append(pair)

    edge_list_for_month_history_repetitions.append(list_month_history_double_edges)

  for element in edge_list_for_month_history_repetitions:
   print(element)

  lscc_nodes_for_month = []

  pickle.dump(edge_list_for_month_history_repetitions, open('./biological_projects_networks/edge_list_for_month_history_repetitions_{}_{}'.format(USER_NAME, REPO_NAME), 'wb'))
  edge_list_for_month_history_repetitions = pickle.load(open('./biological_projects_networks/edge_list_for_month_history_repetitions_{}_{}'.format(USER_NAME, REPO_NAME), 'rb'))

  for list_edges_for_month in edge_list_for_month_history_repetitions:

    print(len(list_edges_for_month))

    G = nx.DiGraph()

    for edge_pair in list_edges_for_month:
      x, y = edge_pair[0], edge_pair[1]
      G.add_edge(x, y)

    if (len(list_edges_for_month) == 0):
      lscc_nodes = 0
      lscc_nodes_for_month.append(lscc_nodes)

    if(len(list_edges_for_month) != 0):

      nodes = G.number_of_nodes()

      largest = max(nx.strongly_connected_components(G), key=len)

      lscc = list(largest)

      lscc_nodes_for_month.append((len(lscc)/nodes) * 100)
      #lscc_nodes_for_month.append(len(lscc))

    G.clear()

  # printing dates and lsccs to the file

  #dates_file_name = "biological_projects_networks/dates_and_lsccs/Dates_" + name1 + "_" + repo1 + ".txt"
  #datesfile = open(dates_file_name, 'w')

  #for element in dates_month_year_single:
    #month = element[0]
    #year = element[1]
    #datesfile.write("%s\n" % str(element))

  #datesfile.close()

  #lscc_vertices_dates_file_name = "biological_projects_networks/dates_and_lsccs/Dates_lscc_vertices_" + name1 + "_" + repo1 + ".txt"
  #dateslsccverticesfile = open(lscc_vertices_dates_file_name, 'w')

  #for element in lscc_nodes_for_month:
    #dateslsccverticesfile.write("%s\n" % str(element))

  #dateslsccverticesfile.close()

  # getting amount of stars for each date in dates_month_year_single[] - did not do it yet, for now we have LSCCs and the star history from the web site

  '''
  url = "https://api.github.com/repos/" + name1 + "/" + repo1 + "/stargazers?per_page=100&page=1"
  print(url)
  res = requests.get(url, headers=headers)
  stars = res.json()

  while 'next' in res.links.keys():
    res = requests.get(res.links['next']['url'], headers=headers)
    stars.extend(res.json())

  print(len(stars))

  issues_string = json.dumps(stars)
  json_object = json.loads(issues_string)
  json_formatted_str = json.dumps(json_object, indent=2)  # transforming issues to the string

  # printing the file with open and closed issues

  stars_file_name = "Stars_" + name1 + "_" + repo1 + ".txt"

  with open(stars_file_name, "w") as text_file:
    text_file.write(json_formatted_str)

  with open(stars_file_name) as json_file:
    stars_data = json.load(json_file)  # data is a list

  stars_dates = []

  for i in range(len(stars_data)):
    date = str(stars_data[i]['starred_at'])
    starred_at_array = [(n) for n in date.strip().split('-')]
    pair = [starred_at_array[1], starred_at_array[0]]
    stars_dates.append(pair)

  for element in stars_dates:
    print(element)

  #print(len(dates_month_year_single))

  stars_for_month = [] # amount of stars in each month

  for date_pair in dates_month_year_single:

    amount_of_stars = 0

    for element in stars_dates:
      if (date_pair == element):
        amount_of_stars = amount_of_stars + 1

    stars_for_month.append(amount_of_stars)

  #print(len(stars_for_month))

  #for element in stars_for_month:
    #print(element)

  stars_for_month_history = []

  stars_for_month_history.append(stars_for_month[0])

  for i in range(1, len(stars_for_month)):

    sum_elements = 0

    for j in range(0, i + 1):
      sum_elements = sum_elements + stars_for_month[j]

    stars_for_month_history.append(sum_elements)


  #print(len(stars_for_month_history))

  #for element in stars_for_month_history:
    #print(element)
    
  '''

  # plotting dates and lsccs sizes together


  dates_together = []

  for element in dates_month_year_single:
    dates_together.append(element[0] + "-" + element[1])

  sample_timeseries_data = {

    'Date': dates_together,
    'LSCC': lscc_nodes_for_month,
    #'Stars': stars_for_month_history

  }

  dataframe = pd.DataFrame(sample_timeseries_data, columns=['Date', 'LSCC'])

  dataframe["Date"] = dataframe["Date"].astype("datetime64[ns]")

  dataframe = dataframe.set_index("Date")
  #dataframe.to_csv('df_{}_{}.csv'.format(USER_NAME, REPO_NAME))
  plt.style.use("fivethirtyeight")

  plt.figure(figsize=(12, 10))

  plt.xlabel("Date")
  plt.ylabel("LSCC, fraction")
  plt.title("Size the LSCC over time")

  plt.plot(dataframe["LSCC"])
  #plt.plot(dataframe["Stars"])

  plt.savefig("./biological_projects_networks/LSCC_over_time/Date_LSCC_fractioin_{}_{}.png".format(USER_NAME, REPO_NAME))

  plt.show()

  print("End of function!")

def print_LSCC_IN_OUT():

  vertices_file = "biological_projects_networks/LSCC_IN_OUT_percentage/ordered_3.txt"

  vertices_array = []

  with open(vertices_file) as f:
    for line in f:
      vertices_array.append(int(line))

  LSCC_file = "biological_projects_networks/LSCC_IN_OUT_percentage/V_LSCC_3.txt"

  LSCC_array = []

  with open(LSCC_file) as f:
    for line in f:
      LSCC_array.append(float(line))

  OUT_file = "biological_projects_networks/LSCC_IN_OUT_percentage/V_OUT_3.txt"

  OUT_array = []

  with open(OUT_file) as f:
    for line in f:
      OUT_array.append(float(line))

  IN_file = "biological_projects_networks/LSCC_IN_OUT_percentage/V_IN_3.txt"

  IN_array = []

  with open(IN_file) as f:
      for line in f:
          IN_array.append(float(line))

  df = pd.DataFrame(list(zip(vertices_array, LSCC_array, OUT_array, IN_array)),
                    index=vertices_array,
                    columns=['vertices', 'LSCC', 'OUT', 'IN'])

  df.plot(x='vertices', kind='bar', stacked=True,
          title='bow-tie structure, #biology')

  plt.savefig(
    "./biological_projects_networks/LSCC_IN_OUT_percentage/LSCC_IN_OUT_3_stacked_bar_biology.png")

  plt.show()

  '''
  plt.style.use("fivethirtyeight")

  plt.figure(figsize=(12, 10))

  #plt.semilogx()
  #plt.semilogy()

  plt.xlabel("100 most popular projects")
  plt.ylabel("LSCC, OUT, IN")
  plt.title("Fraction of the LSCC, OUT and IN")

  plt.plot.bar(x=vertices_array, stacked=True)

  #plt.plot(df["LSCC"])
  #plt.plot(df["OUT"])
  #plt.plot(df["IN"])

  plt.savefig(
    "./biological_projects_networks/LSCC_IN_OUT_percentage/LSCC_IN_OUT_100.png")

  plt.show()
  
  '''

  '''

  sample_timeseries_data = {

    'Vertices': vertices_array,
    'LSCC': LSCC_array,
    'OUT': OUT_array,
    'IN': IN_array,

  }

  dataframe = pd.DataFrame(sample_timeseries_data, columns=['Vertices', 'LSCC', 'OUT', 'IN'])

  #dataframe["Vertices"] = dataframe["Vertices"].astype("datetime64[ns]")

  dataframe = dataframe.set_index("Vertices")
  # dataframe.to_csv('df_{}_{}.csv'.format(USER_NAME, REPO_NAME))
  plt.style.use("fivethirtyeight")

  plt.figure(figsize=(12, 10))

  plt.xlabel("Vertices")
  plt.ylabel("LSCC, fraction")
  plt.title("Size the LSCC over time")

  plt.plot(dataframe["LSCC"])
  # plt.plot(dataframe["Stars"])

  plt.savefig(
    "./biological_projects_networks/LSCC_IN_OUT/LSCC_IN_OUT.png")

  plt.show()
  
  '''

def star_history(name, repo):

  url = "https://api.github.com/repos/" + name + "/" + repo + "/stargazers?per_page=100&page=1"
  print(url)
  res = requests.get(url, headers=headers)
  stars = res.json()

  while 'next' in res.links.keys():
    res = requests.get(res.links['next']['url'], headers=headers)
    stars.extend(res.json())

  print(len(stars))

  issues_string = json.dumps(stars)
  json_object = json.loads(issues_string)
  json_formatted_str = json.dumps(json_object, indent=2)  # transforming issues to the string

  # printing the file with open and closed issues

  stars_file_name = "Stars_" + name + "_" + repo + ".txt"

  with open(stars_file_name, "w") as text_file:
    text_file.write(json_formatted_str)

  with open(stars_file_name) as json_file:
    stars_data = json.load(json_file)  # data is a list

  stars_dates = []

  for i in range(len(stars_data)):
    date = str(stars_data[i]['starred_at'])
    starred_at_array = [(n) for n in date.strip().split('-')]
    pair = [starred_at_array[1], starred_at_array[0]]
    stars_dates.append(pair)



  print(len(stars_dates))


  # getting the values for the star history

  '''

  stars_line_array = []
  dates_stars = []
  amount_stars = []

  star_history_file_name = "biological_projects_networks/star_history/star_history.txt"

  with open(star_history_file_name) as f:
    for line in f:
      stars_line_array.append([(n) for n in line.strip().split(' ')])  # line_array has all our edges

  for element in stars_line_array:
    month = element[1]
    year = element[3]
    stars = element[8]
    stars_array = [(n) for n in stars.strip().split(',')]
    dates_stars.append([month, year])
    amount_stars.append(stars_array[1])

  for element in dates_stars:

    month = element[0]

    if (month == 'Jan'):
      element[0] = '01'
    if (month == 'Feb'):
      element[0] = '02'
    if (month == 'Mar'):
      element[0] = '03'
    if (month == 'Apr'):
      element[0] = '04'
    if (month == 'May'):
      element[0] = '05'
    if (month == 'Jun'):
      element[0] = '06'
    if (month == 'Jul'):
      element[0] = '07'
    if (month == 'Aug'):
      element[0] = '08'
    if (month == 'Sep'):
      element[0] = '09'
    if (month == 'Oct'):
      element[0] = '10'
    if (month == 'Nov'):
      element[0] = '11'
    if (month == 'Dec'):
      element[0] = '12'

  dates_stars_together = []

  for element in dates_stars:
    dates_stars_together.append(element[0] + "-" + element[1])

  sample_timeseries_data = {

    'Date': dates_stars_together,
    'Stars': amount_stars

  }
  
  '''

  '''
  min_date = dataframe['Date'].min()
  dataframe['n_days_past_inception'] = dataframe['Date'].apply(lambda b: (pd.to_datetime(b) - pd.to_datetime(min_date)).days)
  curr_stars = 0
  curr_day = 1
  derivatives = []
  for days, n_stars, date in zip(dataframe['n_days_past_inception'].tolist(), dataframe['Stars'].tolist(), dataframe['Date'].tolist()):
    derivatives.append({'date': pd.to_datetime(date).strftime('%Y%m'), 'star_gain': (int(n_stars) - curr_stars) / (days - curr_day)})
    curr_stars = int(n_stars)
    curr_day = days

  df_star = pd.DataFrame.from_records(derivatives)
  df_lscc = pd.read_csv('df_{}_{}.csv'.format(USER_NAME, REPO_NAME))
  df_lscc['month_year'] = df_lscc['Date'].apply(lambda b: pd.to_datetime(b).strftime('%Y%m'))
  df_merge = pd.merge(df_lscc, df_star, left_on='month_year', right_on='date')
  print(df_merge.head(5))
  plt.scatter(df_merge['star_gain'], df_merge['LSCC'])
  plt.show()
  from sklearn.linear_model import LinearRegression
  reg = LinearRegression().fit(np.array(df_merge['LSCC'].tolist()).reshape(-1,1), df_merge['star_gain'])
  print(reg)
  print(reg.score(np.array(df_merge['LSCC'].tolist()).reshape(-1,1), df_merge['star_gain']))
  print(reg.coef_)
  print(reg.intercept_)
  
  '''

  '''

  dataframe = pd.DataFrame(sample_timeseries_data, columns=['Date', 'Stars'])

  dataframe["Date"] = dataframe["Date"].astype("datetime64[ns]")

  dataframe = dataframe.set_index("Date")

  plt.style.use("fivethirtyeight")

  plt.figure(figsize=(12, 10))

  plt.xlabel("Date")
  plt.ylabel("Stars")
  plt.title("Amount of stars over time")

  plt.plot(dataframe["Stars"])

  plt.savefig("./biological_projects_networks/stars_over_time/Date_stars_{}_{}.png".format(USER_NAME, REPO_NAME))

  plt.show()
  
  '''

def drawing_network_properties_from_arrays(x_array, y_array):  # , y_name2, y_name3, y_name4

  x = []

  for element in x_array:
    x.append((element))  # line_array has all our edges

  y1 = []

  for element2 in y_array:
    y1.append(int(element2))  # line_array has all our edges

  print(len(x))
  print(len(y1))

  fig = plt.figure()
  ax1 = fig.add_subplot(111)

  ax1.scatter(x, y1, s=8, c='blue', marker="8", label='vertices, LSCC')
  # ax1.scatter(x, y2, s=8, c='r', marker="o", label='commits')
  # ax1.scatter(x, y3, s=8, c='g', marker="D", label='forks')
  # ax1.scatter(x, y4, s=8, c='dodgerblue', marker="h", label='contributors')
  plt.legend(loc='upper right')

  # plt.semilogx()
  # plt.semilogy()
  plt.savefig("./biological_projects_networks/dates_and_lsccs/picture.png")

  plt.show()

def list_of_edges(name1, repo1):

  print(name1 + " " + repo1)

  issues_file_name1 = "Output_open_and_closed_issues_" + name1 + "_" + repo1 + ".txt"

  labels_list_file_name = "biological_projects_networks/thematics_communities_list_of_labels/labels_list_file_" + name1 + "_" + repo1 + "_chain_thread.txt"

  labelslistfile = open(labels_list_file_name, 'w')

  #creating list of lists of comments

  with open(issues_file_name1) as json_file:
    data = json.load(json_file) #data is a list

  #list of creators of the issues, all issuers who started the issues in the ordered array
  ids_of_issuers = []

  for i in range(len(data)):
    ids_of_issuers.append(data[i]['user']['id'])
    labelslistfile.write("%s %s\n" % (str(data[i]['user']['id']), str(data[i]['author_association'])))

  #list of commenters, commenters, who commented for every issuer in the list of issuers

  edge_list_file_name = "biological_projects_networks/thematics_communities_list_of_edges/edge_list_file_" + name1 + "_" + repo1 + "_chain_thread.txt"

  myedgelistfile = open(edge_list_file_name, 'w')

  #commenters_file_name = "Comments_list_of_lists_" + name1 + "_" + repo1 + ".txt"

  #myfile = open(commenters_file_name, 'w')

  # file to record the lables

  #labels_list_file_name = "biological_projects_networks/thematics_communities_list_of_labels/labels_list_file_" + name1 + "_" + repo1 + "_chain_thread.txt"

  #mylabelslistfile = open(labels_list_file_name, 'w')

  ids_of_commenters = []
  list_of_ids_of_commenters = []

  #G = nx.DiGraph() # creating a directed graph object with 0 edges and nodes

  for k in range(len(data)):

    print(str(k))
    url = data[k]['comments_url']
    print(url)
    res = requests.get(url, headers=headers)
    comments = res.json()

    comments_string = json.dumps(comments)
    comments_json_object = json.loads(comments_string)
    comments_json_formatted_str = json.dumps(comments_json_object, indent=2)  # transforming issues to the string

    # printing the file with comments

    file_name = "Comments_for_issues_" + str(k) + ".txt"

    with open(file_name, "w") as text_file:
      text_file.write(comments_json_formatted_str)

    with open(file_name) as json_file:
      comments_list = json.load(json_file) #data is a list

    ids_of_commenters.clear()

    for j in range(len(comments_list)):
      ids_of_commenters.append(comments_list[j]['user']['id']) # adding id of commenter to the list ids_of_commenters
      labelslistfile.write("%s %s\n" % (str(comments_list[j]['user']['id']), str(comments_list[j]['author_association'])))

    #comments_list.clear()

    #for r in range(len(ids_of_commenters)):
    #  myedgelistfile.write("%s %s\n" % (str(ids_of_commenters[r]), str(ids_of_issuers[k])))

    #connecting every first commenter to the issuer

    if (len(ids_of_commenters) >= 1):
      myedgelistfile.write("%s %s\n" % (str(ids_of_commenters[0]), str(ids_of_issuers[k])))
      #G.add_edge(ids_of_commenters[0],ids_of_issuers[k])

    #for m in range(len(ids_of_commenters)):
    #  v = m
    #  for l in range(0,v):
    #    myedgelistfile.write("%s %s\n" % (str(ids_of_commenters[v]),str(ids_of_commenters[l])))

    if(len(ids_of_commenters) >= 2):
      for m in range(1, len(ids_of_commenters)):
        myedgelistfile.write("%s %s\n" % (str(ids_of_commenters[m]),str(ids_of_commenters[m-1])))
        #G.add_edge(ids_of_commenters[m],ids_of_commenters[m-1])

    list_of_ids_of_commenters.append(ids_of_commenters) # adding ids_of_commenters to the list list_of_ids_of_commenters

    os.remove(file_name) # removing created file, to not store all the files in the directory

    # printing commenters lists

    #myfile.write("%s\n" % str(ids_of_issuers[k]))
    #myfile.write("%s\n" % str(list_of_ids_of_commenters[k]))

    # end for #

  #myfile.close()
  myedgelistfile.close()

  #mylabelslistfile.close()

  labelslistfile.close()

  print("End of function!")

def deleting_edges(name2, repo2):

  edge_list_original_file_name = "biological_projects_networks/thematics_communities_list_of_edges/edge_list_file_" + name2 + "_" + repo2 + "_chain_thread.txt"

  edge_list = "biological_projects_networks/thematics_communities_list_of_edges_single/edge_list_file_" + name2 + "_" + repo2 + ".txt"

  edgelist = open(edge_list, 'w')

  labels_list_original_file_name = "biological_projects_networks/thematics_communities_list_of_labels/labels_list_file_" + name2 + "_" + repo2 + "_chain_thread.txt"

  labels_list = "biological_projects_networks/thematics_communities_list_of_labels_single/labels_list_file_" + name2 + "_" + repo2 + ".txt"

  labelslist = open(labels_list, 'w')

  line_array = []
  line_array_without_self_loops = []

  with open(edge_list_original_file_name) as f:
    for line in f:
      line_array.append([int(n) for n in line.strip().split(' ')])  # line_array has all our edges

  for pair in line_array:  # now we are going inside of every pair of line_array
    x, y = pair[0], pair[1]
    if (x != y):
      line_array_without_self_loops.append([x, y])  # creating the list of edges without self-loops

  # line_array_without_self_loops - array of edges wihout self-loops

  line_array_without_double_edges = []  # the list of edges without double edges

  for pair2 in line_array_without_self_loops:  # now we are going inside of every pair of line_array
    if pair2 not in line_array_without_double_edges:
      line_array_without_double_edges.append(pair2)

  list_nodes = []

  for pair3 in line_array_without_double_edges:  # now we are going inside of every pair of line_array
    x1, y1 = pair3[0], pair3[1]
    edgelist.write("%s %s\n" % (str(x1), str(y1)))
    if x1 not in list_nodes:
      list_nodes.append(x1)
    if y1 not in list_nodes:
      list_nodes.append(y1)

  print(len(list_nodes))
  print(len(line_array_without_double_edges))

  #file.write("%s\n" % str(len(list_nodes)))

  # print(line_array_without_double_edges)
  edgelist.close()


  line_array_labels = []

  with open(labels_list_original_file_name) as f:
    for line in f:
      line_array_labels.append([(n) for n in line.strip().split(' ')])  # line_array has all our edges

  line_array_labels_without_double_edges = []  # the list of edges without double edges

  for pair in line_array_labels:  # now we are going inside of every pair of line_array
    if pair not in line_array_labels_without_double_edges:
      line_array_labels_without_double_edges.append(pair)

  for pair in line_array_labels_without_double_edges:  # now we are going inside of every pair of line_array
    x1, y1 = pair[0], pair[1]
    labelslist.write("%s %s\n" % (str(x1), str(y1)))

  print(len(line_array_labels_without_double_edges))

  labelslist.close()

  print("End of deleting_edges function!")

def drawing_graphs(name3, repo3):

  edge_list_file = "edge_list_file_" + name3 + "_" + repo3 + ".txt"

  G = nx.DiGraph() # creating a directed graph object with 0 edges and nodes

  line_array = []

  with open(edge_list_file) as f:
    for line in f:
      line_array.append([int(n) for n in line.strip().split(';')])  # line_array has all our edges

  for pair in line_array:  # now we are going inside of every pair of line_array
    x, y = pair[0], pair[1]
    G.add_edge(x, y)

  po = nx.kamada_kawai_layout(G)
  fi, ax = plt.subplots(1, dpi=200, figsize=(4, 4))

  nx.draw_networkx(G, pos=po, arrows=True, node_size=5, node_color = 'black',with_labels=False, width=0.5, edge_color='black', alpha=0.8)

  #nx.draw_networkx_edges(G, pos=po, width=0.5, edge_color='blue', alpha=0.8, arrows=True)
  #nx.draw_networkx_nodes(G, pos=po, node_size=5, node_color='black')

  ax.set_title(name3 + '_' + repo3 + ' network')
  plt.savefig('./' + name3 + '_' + repo3 + '_test.pdf')
  plt.show()

  print("End of drawing_graphs function!")

def statistics_of_the_projects(name4, repo4, file):

  print(name4 + " " + repo4)

  '''

  url = "https://api.github.com/repos/" + name4 + "/" + repo4 + "/issues?per_page=100&page=1&state=open"
  print(url)
  res = requests.get(url, headers=headers)
  issues = res.json()

  while 'next' in res.links.keys():
    res = requests.get(res.links['next']['url'], headers=headers)
    issues.extend(res.json())

  #print(len(issues))

  # making request for closed issues

  url = "https://api.github.com/repos/" + name4 + "/" + repo4 + "/issues?per_page=100&page=1&state=closed"
  print(url)
  res2 = requests.get(url, headers=headers)
  issues2 = res2.json()

  while 'next' in res2.links.keys():
    res2 = requests.get(res2.links['next']['url'], headers=headers)
    issues2.extend(res2.json())

  #print(len(issues2))

  issues.extend(issues2)  # adding open and closed issues together

  #print(len(issues))

  file.write("%s\n" % str(len(issues)))
  
  '''



  url = "https://api.github.com/repos/" + name4 + "/" + repo4 +"/commits?per_page=100&page=1"
  print(url)
  res=requests.get(url,headers=headers)
  commits=res.json()

  while 'next' in res.links.keys():
    res=requests.get(res.links['next']['url'],headers=headers)
    commits.extend(res.json())

  #print(len(commits))

  file.write("%s\n" % str(len(commits)))
  


  '''
  
  url = "https://api.github.com/repos/" + name4 + "/" + repo4 + "/forks?per_page=100&page=1"
  print(url)
  res = requests.get(url, headers=headers)
  forks = res.json()

  while 'next' in res.links.keys():
    res = requests.get(res.links['next']['url'], headers=headers)
    forks.extend(res.json())

  #print(len(forks))

  file.write("%s\n" % str(len(forks)))
  
  '''


  '''

  url = "https://api.github.com/repos/" + name4 + "/" + repo4 + "/stargazers?per_page=100&page=1"
  print(url)
  res = requests.get(url, headers=headers)
  stars = res.json()

  while 'next' in res.links.keys():
    res = requests.get(res.links['next']['url'], headers=headers)
    stars.extend(res.json())

  print(len(stars))

  file.write("%s\n" % str(len(stars)))

  '''

  '''

  url = "https://api.github.com/repos/" + name4 + "/" + repo4 + "/contributors?per_page=100&page=1"
  # url = "https://api.github.com/repos/" + name4 + "/" + repo4 + "/contributors?per_page=100&page=1&anon=true"
  print(url)
  res = requests.get(url, headers=headers)
  contributors = res.json()

  while 'next' in res.links.keys():
    res = requests.get(res.links['next']['url'], headers=headers)
    contributors.extend(res.json())

  #print(len(contributors))

  file.write("%s\n" % str(len(contributors)))
  
  '''

  '''

  url = "https://api.github.com/search/issues?q=repo:" + name4 + "/" + repo4 + "+type:pr+is:merged"
  #url = "https://api.github.com/repos/"  + name4 + "/" + repo4 + "pulls?per_page=100&page=1"
  #+is:pr+is:merged
  #url = "https://api.github.com/api/v3/search/issues?q=repo:"  + name4 + "/" + repo4 + "+is:merged?per_page=100&page=1"
  print(url)
  res = requests.get(url, headers=headers)
  merged_pr = res.json()["total_count"]

  #print(merged_pr) #ta-da!!!!

  file.write("%s\n" % str(merged_pr))

  '''

  print("End of statistics_of_the_projects function!")

def network_properties(name5, repo5, file):

  #metrics_file = "LSCCs_" + name5 + "_" + repo5 + ".txt"

  #metricsfile = open(metrics_file, 'w')

  edge_list_file = "biological_projects_networks\\biological_projects_edge_list\\edge_list_file_" + name5 + "_" + repo5 + ".csv"

  label_list_file = "biological_projects_networks\\biological_networks_issuers_labes\\labels_issuers_list_file_" + name5 + "_" + repo5 + ".txt"

  G = nx.DiGraph() # creating a directed graph object with 0 edges and nodes

  line_array = []

  with open(edge_list_file) as f:
    for line in f:
      line_array.append([int(n) for n in line.strip().split(';')])  # line_array has all our edges

  for pair in line_array:  # now we are going inside of every pair of line_array
    x, y = pair[0], pair[1]
    G.add_edge(x, y)

  n = G.number_of_nodes() # number of nodes
  m = G.number_of_edges() # number of edges

  if(len(line_array) != 0):

    labels_line_array = []

    with open(label_list_file) as f2:
      for line2 in f2:
        labels_line_array.append([(n) for n in line2.strip().split(' ')])  # line_array has all our edges

    labels_line_array_without_double_edges = []  # the list of edges without double edges

    for pair2 in labels_line_array:  # now we are going inside of every pair of line_array
      if pair2 not in labels_line_array_without_double_edges:
        labels_line_array_without_double_edges.append(pair2)

    #for pair3 in labels_line_array_without_double_edges:
    #print(pair3)

    #contr = 0

    list_nodes_issuers = []

    for pair3 in labels_line_array_without_double_edges:
      node = pair3[0]
      list_nodes_issuers.append(node)

  #for i in range(len(list_nodes_issuers)):
    #print(list_nodes_issuers[i])

    largest = max(nx.strongly_connected_components(G), key=len)

    lscc = list(largest)

  #print(len(lscc))
  #print(len(list_nodes_issuers))

    count = 0

    for j in range(len(list_nodes_issuers)):
      for i in range(len(lscc)):
        if (int(list_nodes_issuers[j]) == int(lscc[i])):
          count = count + 1
          break

    #print(count)
    #print((count / len(list_nodes_issuers)) * 100)
    file.write("%s\n" % str((count/len(lscc)) * 100))

  else:
    file.write("%s\n" % str(0))

  '''

  labels_lscc = []

  for i in range(len(lscc)):
    v_lscc = lscc[i]
    for pair in labels_line_array:
      if(int(v_lscc) == int(pair[0])):
        labels_lscc.append(pair[1])
        break

  contr_lscc = 0
  owner = 0
  collab = 0
  member = 0

  for j in range(len(labels_lscc)):
    if(labels_lscc[j] == 'CONTRIBUTOR'):
      contr_lscc = contr_lscc + 1
    #if (labels_lscc[j] == 'OWNER'):
      #owner = owner + 1
    #if (labels_lscc[j] == 'COLLABORATOR'):
      #collab = collab + 1
    #if (labels_lscc[j] == 'MEMBER'):
      #member = member + 1

  print(contr_lscc)
  print((contr_lscc/contr)*100)

  '''



  #average_clustering = nx.average_clustering(G)

  '''

  centrality = nx.harmonic_centrality(G)

  centralities = [val for (node, val) in centrality.items()]

  sum_centralities = 0

  for i in range(len(centralities)):
    sum_centralities = sum_centralities + centralities[i]

  av_centralities = sum_centralities / len(centralities)
  
  '''

  '''

  in_degrees = [val for (node, val) in G.in_degree()]

  for i in range(len(in_degrees)):
    metrics_file.write("%s\n" % str(in_degrees[i]))


  metrics_file.close()

  '''

  '''
  out_degrees = [val for (node, val) in G.out_degree()]

  # degrees = [val for (node, val) in G.degree()]

  sum_out_degree = 0

  for i in range(len(out_degrees)):
    sum_out_degree = sum_out_degree + out_degrees[i]

  av_out_degree = sum_out_degree / len(out_degrees)
  '''

  #degree_assortativity_coefficient_in_in = nx.degree_assortativity_coefficient(G,'in','in')
  #degree_assortativity_coefficient_in_out = nx.degree_assortativity_coefficient(G, 'in', 'out')
  #degree_assortativity_coefficient_out_in = nx.degree_assortativity_coefficient(G, 'out', 'in')
  #degree_assortativity_coefficient_out_out = nx.degree_assortativity_coefficient(G, 'out', 'out')

  #reciprocity = nx.reciprocity(G)


  #G_LSCC = G.subgraph(max(nx.strongly_connected_components(G), key=len)) # subgraph that corresponds to the LSCC

  #degree_assortativity_coefficient = nx.degree_assortativity_coefficient(G)



  #LSCC_m = len(list(G_LSCC.edges))

  #average_clustering = nx.average_clustering(G_LSCC)

  #clustering_coefficient  = nx.clustering(G_LSCC)

  #av_shortest_path_length = nx.average_shortest_path_length(G_LSCC)

  #d = nx.diameter(G_LSCC)



  #sorted_degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)

  #b = nx.is_strongly_connected(G)

  #largest = max(nx.strongly_connected_components(G), key=len)

  #SCCs = sorted(nx.strongly_connected_components(G), key=len, reverse=True)

  #SCCs = nx.strongly_connected_components(G)



  #cc = nx.average_clustering(G)
  #d = nx.diameter(G)

  #part = nx_alg.best_partition(G)
  #mod = nx_alg.modularity(part, G)

  #pc = nx.degree_pearson_correlation_coefficient(G)

  #asp = nx.average_shortest_path_length(G)

  print("End of network_properties function!")

def small_network_properties():

  G = nx.DiGraph() # creating a directed graph object with 0 edges and nodes

  G.add_edge(0, 1)
  G.add_edge(1, 2)
  G.add_edge(2, 3)
  G.add_edge(3, 2)
  G.add_edge(2, 0)
  G.add_edge(0, 4)
  G.add_edge(4, 5)


  n = G.number_of_nodes()
  m = G.number_of_edges()

  print(str(n))
  print(str(m))


  out_degrees = [val for (node, val) in G.out_degree()]

  #degrees = [val for (node, val) in G.degree()]

  sum_out_degree = 0

  for i in range(len(out_degrees)):
    sum_out_degree = sum_out_degree + out_degrees[i]


  av_out_degree = sum_out_degree / len(out_degrees)

  print(av_out_degree)

  #reciprocity = nx.reciprocity(G)

  #largest = max(nx.strongly_connected_components(G), key=len)

  #LSCC = G.subgraph(max(nx.strongly_connected_components(G), key=len))

  #LSCC_edges = list(LSCC.edges)

  #aspl = nx.average_shortest_path_length(G)

  #largest = max(nx.strongly_connected_components(G), key=len)

  #scc = sorted(nx.strongly_connected_components(G), key=len, reverse=True)

  #sorted_degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)

  #print(largest)

  #print(LSCC_edges)

  #print(len(LSCC_edges))




  #cc = nx.average_clustering(G)
  #d = nx.diameter(G)

  #part = nx_alg.best_partition(G)
  #mod = nx_alg.modularity(part, G)

  #pc = nx.degree_pearson_correlation_coefficient(G)

  #asp = nx.average_shortest_path_length(G)

  print("End of small_network_properties function!")

def drawing_network_properties(name, repo): # , y_name2, y_name3, y_name4

  x_name = "biological_projects_networks/dates_and_lsccs/Dates_" + name + "_" + repo

  y_name1 = "biological_projects_networks/dates_and_lsccs/Dates_lscc_vertices_"  + name + "_" + repo

  x = []

  x_file = x_name + ".txt"

  with open(x_file) as f1:
    for number1 in f1:
      x.append((number1))  # line_array has all our edges


  y1 = []

  y_file1 = y_name1 + ".txt"

  with open(y_file1) as f2:
    for number2 in f2:
      y1.append(int(number2))  # line_array has all our edges

  '''

  y2 = []

  y_file2 = y_name2 + ".txt"

  with open(y_file2) as f3:
    for number3 in f3:
      y2.append(int(number3))  # line_array has all our edges

  y3 = []

  y_file3 = y_name3 + ".txt"

  with open(y_file3) as f4:
    for number4 in f4:
      y3.append(int(number4))  # line_array has all our edges

  y4 = []

  y_file4 = y_name4 + ".txt"

  with open(y_file4) as f5:
    for number5 in f5:
      y4.append(int(number5))  # line_array has all our edges
      
  '''

  #plt.xlabel("Indegree")
  #plt.ylabel("Frequency")
  #plt.scatter(x, y, c="blue", s=10) # "blue" - vertex-related property, "red" - edge-related propoerty
  #plt.semilogx()
  #plt.semilogy()

  fig = plt.figure()
  ax1 = fig.add_subplot(111)

  #ax1.plot(x, y1)

  ax1.scatter(x, y1, s=8, c='blue', marker="8", label='vertices, LSCC')
  #ax1.scatter(x, y2, s=8, c='r', marker="o", label='commits')
  #ax1.scatter(x, y3, s=8, c='g', marker="D", label='forks')
  #ax1.scatter(x, y4, s=8, c='dodgerblue', marker="h", label='contributors')
  plt.legend(loc='upper right')

  #plt.semilogx()
  #plt.semilogy()
  plt.savefig("./biological_projects_networks/dates_and_lsccs/dates_vertices_" + name + "_" + repo + "_LSCC.png")

  plt.show()


  #now we have list of issuers and list of lists of commenters, now we have to build an edge list!
  #now we have list of issuers and list of lists of commenters, now we have to build an edge list!
  #creating an edge list!!!!
  #creating an edge list!!!!

  #creating an edge list!!!!

  # the "rule of thumb" for the edge list for social network is every new node i is connecting to every node before him
  # so in the chane n1 -> n2 -> n3 -> n4, n2 will be connected to n1, n3 will be connected to nodes n1 and n2 and so on.
  # ids_of_issuers - is the list with all issuers for every issue, the authors of the issues
  # list_of_ids_of_commenters[] - is the list of lists of the commenters for every issue
  # first step: every commenter in list_of_ids_of_commenters[] will be connected to the issuer

  #edge_list_file_name = "edge_list5.txt"

  #edge_list_file = open(edge_list_file_name, 'w')

  #for n in range(0, len(list_of_ids_of_commenters)):
     # print("%s\n" % str(list_of_ids_of_commenters[n]))

      #edge_list_file.write("%s %s\n" % (str(list_of_ids_of_commenters[n][m]), str(ids_of_issuers[n])))
      #print("%s %s\n" % (str(list_of_ids_of_commenters[n][m]), str(ids_of_issuers[n])))

  #for p in range(len(list_of_ids_of_commenters)):
  #    for q in range(len(list_of_ids_of_commenters[p])):
  #      k = q
  #      for l in range(0, k):
  #        edge_list_file.write("%s %s\n" % (str(list_of_ids_of_commenters[p][k]), str(list_of_ids_of_commenters[p][l])))
          #print("%s %s\n" % (str(list_of_ids_of_commenters[n][m]), str(ids_of_issuers[n])))

  #edge_list_file.close()

  #"cleaning" the edge list

def correlation_coefficient(x_name, y_name1):

  x = []

  x_file = x_name + ".txt"

  with open(x_file) as f1:
    for number1 in f1:
      x.append(int(number1))  # line_array has all our edges

  print(len(x))

  y1 = []

  y_file1 = y_name1 + ".txt"

  with open(y_file1) as f2:
    for number2 in f2:
      y1.append(int(number2))  # line_array has all our edges

  print(len(y1))

  p = pearsonr(x, y1)

  #t = stats.ttest_ind(x, y1)

  #p = stats.linregress(x, y1)

  print(p)
  #print(t)

  #help(pearsonr)

def labels_in_LSCC(name, repo, file):

  #N_main = 0
  #current_lable_main = 0
  #SCCs_ID_main = []
  #seen_main = []

  def dfs_iterative(v, G):

    OUT_labels = []





  edge_list_file = "biological_projects_networks/biological_projects_edge_list/edge_list_file_" + name + "_" + repo + ".csv"

  label_list_file = "biological_projects_networks/biological_projects_labels/labels_list_file_" + name + "_" + repo + "_chain_thread.txt"

  G = nx.DiGraph()  # creating a directed graph object with 0 edges and nodes

  line_array = []

  with open(edge_list_file) as f:
    for line in f:
      line_array.append([int(n) for n in line.strip().split(';')])  # line_array has all our edges

  for pair in line_array:  # now we are going inside of every pair of line_array
    x, y = pair[0], pair[1]
    G.add_edge(x, y)

  n = G.number_of_nodes()  # number of nodes
  m = G.number_of_edges()  # number of edges

  if (len(line_array) != 0):

    labels_line_array = []

    with open(label_list_file) as f2:
      for line2 in f2:
        labels_line_array.append([(n) for n in line2.strip().split(' ')])  # line_array has all our edges

    labels_line_array_without_double_edges = []  # the list of the labels without double edges

    for pair2 in labels_line_array:  # now we are going inside of every pair of line_array
      if pair2 not in labels_line_array_without_double_edges:
        labels_line_array_without_double_edges.append(pair2)

    #print(len(labels_line_array_without_double_edges))

    largest = max(nx.strongly_connected_components(G), key=len) # vertices in the LSCC

    lscc = list(largest)

    SCCs_ID_main = [0] * n
    seen_main = [False] * n

    #current_lable_main = 1

    visited = set()

    for i in range(len(lscc)):
      dfs_iterative(lscc[i], G, visited)





    labels_LSCC = []

    for pair3 in labels_line_array_without_double_edges:
      node = int(pair3[0])
      label = str(pair3[1])
      if(node in lscc):
        labels_LSCC.append(label)

    #print(len(lscc))
    #print(len(labels_LSCC))

    members = 0
    contributors = 0
    collaborators = 0
    owners = 0
    nones = 0

    #total = 0

    for i in range(len(labels_LSCC)):
      #if(labels_LSCC[i] == 'MEMBER'):
        #members = members + 1
      #if (labels_LSCC[i] == 'CONTRIBUTOR'):
        #contributors = contributors + 1
      #if (labels_LSCC[i] == 'COLLABORATOR'):
        #collaborators = collaborators + 1
      if (labels_LSCC[i] == 'OWNER'):
        owners = owners + 1
      #if (labels_LSCC[i] == 'NONE'):
        #nones = nones + 1

    #total = members + contributors + collaborators + owners + nones

    #file.write("%s\n" % str((members/len(lscc)) * 100))

    file.write("%s\n" % str(owners))

  else:
    file.write("%s\n" % str(0))
    #print("no vertices in the network!")

#def LSCC_structure(name, repo, file):


'''

projects_file = "Repositories_list_ordered_for_the_topic_biology_temp.txt"

properties_file = "metrics_biological_projects/owners_in_LSCC.txt"

propertieslist = open(properties_file, 'w')

#edges_list = "biological_projects_networks\\edges_list\\edges_list.txt"

#edgeslist = open(edges_list, 'w')


#vertices_list = "biological_projects_networks\\vertices_list\\vertices_list.txt"

#verticeslist = open(vertices_list, 'w')

#LSCCs_list = "biological_projects_networks\\LSCCs_list\\LSCCs__issuers_list.txt"

#lsccslist = open(LSCCs_list, 'w')


line_projects = []

with open(projects_file) as f:
  for line in f:
    line_projects.append([str(n) for n in line.strip().split('/')])  # line_array has all our edges

for pair in line_projects:  # now we are going inside of every pair of line_array
  x, y = pair[0], pair[1]
  print(str(x) + " " + str(y))
  labels_in_LSCC(str(x), str(y), propertieslist)

#propertieslist.close()

#verticeslist.close()

#edgeslist.close()

propertieslist.close()
  
print("End of the list of the projects!")

'''

'''

properties_file = "metrics_biological_projects\\ordered_forks_numbers_of_projects.txt"

propertieslist = open(properties_file, 'w')

for i in range(999):
  propertieslist.write("%s\n" % str(i))

propertieslist.close()

'''

'''

projects_file = "Repositories_list_ordered_for_the_topic_mathematcis_temp.txt"

#projects_file_first_portion = "biological_projects_first_portion.txt"

# properties_file = "metrics_biological_projects\\amount_of_merged_pull_requests.txt"

# propertieslist = open(properties_file, 'a')

# edges_list = "biological_projects_networks\\edges_list\\edges_list_" + name2 + "_" + repo2 + ".txt"

# edgeslist = open(edges_list, 'w')


# vertices_list = "biological_projects_networks\\vertices_list\\vertices_list.txt"

# verticeslist = open(vertices_list, 'w')


line_projects = []

projects_array = []

with open(projects_file) as f:
  for line in f:
    line_projects.append([str(n) for n in line.strip().split('/')])  # line_array has all our edges

for pair in line_projects:  # now we are going inside of every pair of line_array
  x, y = pair[0], pair[1]
  print(str(x) + " " + str(y))
  open_and_closed_issues(str(x), str(y))

# propertieslist.close()

# verticeslist.close()

print("End of the list of the projects!")

'''

#print_LSCC_IN_OUT()

#open_and_closed_issues(USER_NAME, REPO_NAME)

#list_of_edges_for_each_month(USER_NAME, REPO_NAME)

#star_history(USER_NAME, REPO_NAME)

list_of_edges(USER_NAME, REPO_NAME)

#deleting_edges(USER_NAME, REPO_NAME)

#drawing_graphs("rich-iannone", "DiagrammeR")

#statistics_of_the_projects("petgraph","petgraph")

#network_properties("ossu", "computer-science")

#small_network_properties()

#namen = "sindresorhus"
#repos = "awesome"

#drawing_network_properties("kblin", "ncbi-genome-download")

# , "metrics_biological_projects\\amount_of_commits", "metrics_biological_projects\\amount_of_forks", "metrics_biological_projects\\amount_of_contributors"

#correlation_coefficient("metrics_biological_projects/amount_of_stars_2", "metrics_biological_projects/V_LSCC_2")

#created_at("deepchem", "deepchem")







#first step:

#list = [3, 5, 2]

#lst = [[1, 3], [4, 5], [7, 2, 4]]

#for n in range(len(list)):
#  for m in range(len(lst[n])):
#    #print("%s %s\n" % (str(n), str(m)))
#    print("%s %s\n" % (str(lst[n][m]), str(list[n]))) # building the link from commenters to issuers

#second step:

#for n in range(len(lst)):

#for m in range(len(lst)):
#  k = m
#  #print("k = %s\n" % str(lst[k]))
#  for l in range(0,k):
    #print("%s %s\n" % (str(lst[n][m]), str(lst[n][m-1]))) # building the link from commenters to issuers
#    print("%s %s\n" % (str(lst[k]),str(lst[l])))

#x = range(1, 2)
#for n in x:
#  print(n)

# double edges and self loops

# collecting the data for biological projects



'''

topic = 'biology'

repositories_file_name = "Repositories_for_the_topic_ordered_forks_" + topic + ".txt"

repositories = dict

url = "https://api.github.com/search/repositories?q=topic:biology&per_page=100&page=1&sort=forks&order=desc" #&sort=stars&order=desc
print(url)
res=requests.get(url,headers=headers)
repositories = res.json() # dictionary

#print(type(repositories))
#print(type(repositories["items"]))

while 'next' in res.links.keys():
  res = requests.get(res.links['next']['url'], headers=headers)
  repositories["items"].extend(res.json()["items"])

#print(i)
print(len(repositories["items"]))

repositories_string = json.dumps(repositories)
json_object = json.loads(repositories_string)
json_formatted_str = json.dumps(json_object, indent=2) #transforming issues to the string

#printing the file with open and closed issues

with open(repositories_file_name, "w") as text_file:
  text_file.write(json_formatted_str)
  
'''
  
'''

repositories_list_file_name = "Repositories_list_ordered_forks_for_the_topic_" + topic + ".txt"

repositorieslistfile = open(repositories_list_file_name, 'w')

with open(repositories_file_name) as json_file:
    data = json.load(json_file) #data is a list

names_of_repositories = []

for j in range(len(data["items"])):
  names_of_repositories.append(data["items"][j]["full_name"]) # adding id of commenter to the list ids_of_commenters

for i in range(len(names_of_repositories)):
  repositorieslistfile.write("%s\n" % str(names_of_repositories[i]))

repositorieslistfile.close()

print(len(names_of_repositories))
print(names_of_repositories[2])

'''

'''

repos_string = json.dumps(repos)
json_object = json.loads(repos_string)
json_formatted_str = json.dumps(json_object, indent=2) #transforming issues to the string

#printing the file with open and closed issues

repos_file_name = "repos_" +  topic + ".txt"

with open(repos_file_name, "w") as text_file:
  text_file.write(json_formatted_str)


with open(repos_file_name) as json_file:
  data = json.load(json_file) #data is a list
+
names_of_repos = []

print(data["items"][29])



'''

#for i in range(len(data["items"])):
#  names_of_repos.append(data["items"][i]["full_name"])

#print(len(names_of_repos))

#names_of_repos = []

#for i in data:
#  names_of_repos.append(data['items'][i]['full_name'])

#for i in range(len(data)):
  #names_of_repos.append(data['items'][i]['full_name'])

#print(len(names_of_repos))

#print(data['items'][0]['full_name'])

'''

line_array1 = []

with open(edge_list_file_name1) as f1:
  for line1 in f1:
    line_array1.append([int(l) for l in line1.strip().split(' ')]) #line_array has all our edges

for pair1 in line_array1: # now we are going inside of every pair of line_array
  x,y = pair1[0],pair1[1]
  if(x != y):
  
'''
