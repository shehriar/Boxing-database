from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#This function is only to format the results in a way that is more easily readable
def win_loss_formatting(result):
		if result == 'No':
			result = 'No Contest'
		if result == 'DrawSD':
			result = 'Draw (SD)'

		elif result == 'WinTKO':
			result = 'Win (TKO)'
		elif result == 'WinKO':
			result = 'Win (KO)'
		elif result == 'WinUD':
			result = 'Win (UD)'
		elif result == 'WinSD':
			result = 'Win (SD)'
		elif result == 'WinRTD':
			result = 'Win (RTD)'
		elif result == 'WinTD':
			result = 'Win (TD)'
		elif result == 'WinPTS':
			result = 'Win (PTS)'

		elif result == 'LossTKO':
			result = 'Loss (TKO)'
		elif result == 'LossKO':
			result = 'Loss (KO)'
		elif result == 'LossUD':
			result = 'Loss (UD)'
		elif result == 'LossSD':
			result = 'Loss (SD)'
		elif result == 'LossRTD':
			result = 'LossRTD'
		elif result == 'LossTD':
			result = 'Loss (TD)'
		elif result == 'LossPTS':
			result = 'Loss (PTS)'
		
		else:
			result = 'NA'
		return result

#Main boxing function that takes a name of a boxer and returns their stats
def boxing(name, opponentlist = []):
	name = name.split()
	if len(name) ==2:
		first_name = name[0]
		last_name = name[1]
		myurl = 'https://champinon.info/boxing/'+first_name+'-'+last_name
	elif len(name) == 3:
		first_name = name[0]
		last_name = name[2]
		middle_name = name[1]
		myurl = 'https://champinon.info/boxing/'+first_name+'-'+middle_name+'-'+last_name

	uClient = uReq(myurl)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html, "html.parser")

	win_loss_draw = page_soup.findAll('span',{'class':'fs-24'})
	wins = int(win_loss_draw[0].text)
	losses = int(win_loss_draw[1].text)
	draw = int(win_loss_draw[2].text)

	record = (wins, losses, draw)

	
	#print(record)
	#print('\n')

	tr = page_soup.findAll('tr')
	tr.pop(0)
	for i in range(wins+losses+draw):
		tr_text = tr[i].text
		tr_text = tr_text.split()
		date = tr_text[0]
		opponent = tr_text[1]+' '+tr_text[2]
		result = tr_text[3]

		#for formatting
		result = win_loss_formatting(result)
		if result == 'NA':
			result = (win_loss_formatting(tr_text[4]))
			opponent = tr_text[1]+' '+tr_text[2]+' '+tr_text[3]

		a = opponent + " " + result + " " + date
		opponentlist.append(a)
		#print('\n')
	final = []
	final.append(record)
	final.append(opponentlist)
	return final

    
def all_fighter_data(name, fighters_dict):
    firts_last_name = name.split()
    full_name = ''

    # The URL of the website consists of the website name followed by boxing, followed by the name of the boxer with "-" in between. The following code is just to make sure that the URL is correct
    
    for a in firts_last_name:
        full_name += a + '-'
    fn_lst = list(full_name)
    fn_lst.pop(-1)
    full_name = ''
    for n in fn_lst:
        full_name += n
    if "'" in full_name:
        full_name = full_name.replace("'", "")
    #All of the exceptions to the general rule the website have for their URLs
    if full_name == 'juan-estrada':
        myurl = 'https://champinon.info/boxing/juan-francisco-estrada/'
    elif full_name == 'roy-jones':
        myurl = 'https://champinon.info/boxing/roy-jones-jr'
    elif full_name == 'deejay-kriel':
        myurl = 'https://champinon.info/boxing/dee-jay-kriel'
    elif full_name == 'julio-cesar-martinez':
        myurl = 'https://champinon.info/boxing/julio-cesar-martinez-aguilar/'
    elif full_name == 'lucas-matthysse':
        myurl = 'https://champinon.info/boxing/lucas-martin-matthysse/'
    elif full_name == 'jose-carlos-ramirez':
        myurl = 'https://champinon.info/boxing/jose-ramirez/'
    elif full_name == 'gary-allen-russell-jr':
        myurl = 'https://champinon.info/boxing/gary-russell-jr/'
    else:
        myurl = 'https://champinon.info/boxing/' + full_name


    uClient = uReq(myurl)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")
#does similar work to the boxing() function, however this function is producing a dictionary with every boxer listed along with their records.
    #this can later be used to answer questions like which boxer has the most wins, etc.
    win_loss_draw = page_soup.findAll('span', {'class': 'fs-24'})
    wins = int(win_loss_draw[0].text)
    losses = int(win_loss_draw[1].text)
    draw = int(win_loss_draw[2].text)

    p = page_soup.findAll('p')

     #extracting the Knock-out percentage
    for y in p:
        y = (y.text).split()
        if len(y) >= 1:
            if y[0] == 'KOs:':
                KO_perc = y[1]
    KO_perc = KO_perc.replace('%', '')

    record_lst = [wins, losses, draw, int(KO_perc)]

    return record_lst


def highest_KO_perc(lst):
     #going through the data set that was made earlier and determining the boxer with the highest KO%.
    num_lst = []
    for j in lst:
        num_lst.append(lst[j][3])
    num_lst = mergeSort(num_lst)

    max = num_lst[-1]
    for i in lst:
        if lst[i][3] == max:
            return (i, max)

def most_draws(lst):

    # going through the data set that was made earlier and determining the boxer with the highest draws.
    num_lst = []
    for j in lst:
        num_lst.append(lst[j][2])
    num_lst = mergeSort(num_lst)

    max = num_lst[-1]
    for i in lst:
        if lst[i][2] == max:
            return (i, max)

def most_losses(lst):
    num_lst = []
    for j in lst:
        num_lst.append(lst[j][1])
    num_lst = mergeSort(num_lst)

    max = num_lst[-1]
    for i in lst:
        if lst[i][1] == max:
            return (i, max)

def most_wins(lst):
    num_lst = []
    for j in lst:
        num_lst.append(lst[j][0])
    num_lst = mergeSort(num_lst)

    max = num_lst[-1]
    for i in lst:
        if lst[i][0] == max:
            return (i, max)

def mergeSort(arr):
    if len(arr) > 1:

        # Finding the mid of the array
        mid = len(arr) // 2

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        # Sorting the first half
        mergeSort(L)

        # Sorting the second half
        mergeSort(R)

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr
#
def stats(options):
    #primarily works in order to provide stats such as most wins, most losses, etc.
    myurl = 'https://champinon.info/boxing'
    uClient = uReq(myurl)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    h3 = page_soup.findAll('h3')
    fighters_dict = {}
    fighter_data = {}
    #There are 4 additional irrelevant things at the end of the page hence the len(h3)-4
    #Goes through all of the fighters and adds their name as a key in the dictionary
    for i in range(len(h3) - 4):
        name = h3[i].text
        name = name.lower()
        fighters_dict[name] = []
    for j in fighters_dict:
        fighter_data[j] = all_fighter_data(j, fighters_dict)
    #options = int(input("Type 0 to find fighter with most wins, 1 for most losses,
        #                2 for most draws and 3 for highest KO %"))


    if options == 0:
        #print(most_wins(fighter_data))

        return most_wins(fighter_data)
    elif options == 1:
        #print(most_losses(fighter_data))
        return most_losses(fighter_data)
        
    elif options == 2:
        #print(most_draws(fighter_data))
        return most_draws(fighter_data)
    
    else:
        #print(highest_KO_perc(fighter_data))
        return highest_KO_perc(fighter_data)



########################################################################################

# URL for the NBA website
URL = "http://www.espn.com/nba/players"

#requests library is used to open the URL and then close is
Client = uReq(URL)
html = Client.read()
Client.close()

#It used a parser to go through the data of the website
soupp = soup(html, "lxml")

#used to find the specific html that has the information we need stored
containers = soupp.findAll("div", {"class":"mod-container mod-open-list mod-no-footer mod-teams-list-small"})

dataset = {}

#being used to create a dataset with all the regions and the teams from there along with the URLS that
#give more information about those teams

for i in containers:

    
    name = i.find('div', {"class": "mod-header stathead"})
    name = name.text

    dataset[name] = []
    
    link = i.findAll("div", {"style":"float:left;"})

    teams = i.find('div', {"class": "mod-content"})

    links_list = []
    
    for m in link:

        start = 'http://www.espn.com/nba'
        end = m.find('a')['href']

        end = end[4:]

        actual_link = start + end
        
        links_list.append(actual_link)

    dataset[name].append(links_list)
        
    
    for team in teams:
        
        team = team.text
        
        team = team[1:]
        
        team = team.split("\xa0")
        
        dataset[name].append( team )


updated_dataset = {}

for keys in dataset:

    updated_dataset[keys] = []

    for i in range(len(dataset[keys][0])):
        
        start_info = dataset[keys][1][i]

        end_info = dataset[keys][0][i]

        info = (start_info, end_info)

        updated_dataset[keys].append(info)

output = []

ultimate_dataset = {}
for key in updated_dataset:

    ultimate_dataset[key] = []

    teams_dataset = {}
    
    for team in updated_dataset[key]:

        thename = team[0]

        teams_dataset[thename] = []

        newURL = team[1]

        newClient = uReq(newURL)
        newhtml = newClient.read()
        newClient.close()

        thehtml = soup(newhtml, "lxml")


        textt = thehtml.findAll("tr", {"class": "Table__TR Table__TR--lg Table__even"})

        for i in textt:


            new = i.findAll("td", {"class": "Table__TD"})
            
            alist = []
            
            for j in new:
                alist.append(j.text)


            teams_dataset[thename].append(alist[1:])

        ultimate_dataset[key].append(teams_dataset)

print(ultimate_dataset)

import tkinter as tk

WIDTH = 800
HEIGHT = 800

def format_response(returned):
    try:
        final = returned
    except:
        final = 'Not a prompt, press help for more information'

    return final

regions = ultimate_dataset.keys()

def players(region, team):
    
    list_of_players = []
    
    for i in ultimate_dataset[region][0]:
        if i == team:
            for j in ultimate_dataset[region][0][i]:
                list_of_players.append(j[0])

    return list_of_players

def top_earning_ten_list(ultimate_dataset):
    earning_list = []
    
    for i in regions:
        for j in ultimate_dataset[i][0]:
            for k in ultimate_dataset[i][0][j]:
                if k[6] == '--':
                    pass

                else:
                    money = k[6]
                    money = money.replace('$', '')
                    money = money.replace(',', '')
                    
                    person_money = (k[0], int(money))
                    earning_list.append(person_money)

    return earning_list

#QuickSort

def quickSort(lst, low, high):
    if len(lst) == 1:
        return lst
    if low < high:
        pi = partition(lst, low, high)
        quickSort(lst, low, pi - 1)
        quickSort(lst, pi + 1, high)


def partition(lst, low, high):
    i = (low - 1)
    pivot = lst[high][1]

    for j in range(low, high):
        if lst[j][1] <= pivot:
            i = i + 1
            lst[i], lst[j] = lst[j], lst[i]

    lst[i + 1], lst[high] = lst[high], lst[i+1]
    return (i + 1)


#Top earning players

def most_earning_players(ultimate_dataset):
    
    a = top_earning_ten_list(ultimate_dataset)
    quickSort(a, 0, len(a)-1)

    b = a[::-1]
    return b[:11]
     
        
def test_function(entry):
    
    if entry == "helpNBA":
       speech = ["Here are the possible prompts:",
        "(1)All Regions:", "To find all regions of NBA",
        "(2)Region Teams: - :", "where - is the name of the region",
        "(3)Top Most Earning Players:", "To find out top 10 most earning players",
        "(4)Players-region-team:", "where region and team need to be replaced",'\n',
        "All entries are case sensitive,", "please be careful", '\n',
        "Made by Fatima Alvi and Shehriar Burney"]

       returned = ''
       for i in speech:
           returned += i + '\n'

       

    elif entry == 'All Regions':
        returned = ""
        for i in regions:
            returned += i + '\n'

    elif entry == 'Region Teams: Atlantic':
        team = ultimate_dataset['Atlantic'][0].keys()
        returned = ""
        for i in team:
            returned += i + '\n'

    elif entry == 'Region Teams: Pacific':
        team = ultimate_dataset['Pacific'][0].keys()
        returned = ""
        for i in team:
            returned += i + '\n'

    elif entry == 'Region Teams: Central':
        team = ultimate_dataset['Central'][0].keys()
        returned = ""
        for i in team:
            returned += i + '\n'

    elif entry == 'Region Teams: Southwest':
        team = ultimate_dataset['Southwest'][0].keys()
        returned = ""
        for i in team:
            returned += i + '\n'

    elif entry == 'Region Teams: Southeast':
        team = ultimate_dataset['Southeast'][0].keys()
        returned = ""
        for i in team:
            returned += i + '\n'
    
    elif entry == 'Region Teams: Northwest':
        team = ultimate_dataset['Northwest'][0].keys()
        returned = ""
        for i in team:
            returned += i + '\n'

    elif entry == 'Top Most Earning Players':
        output = most_earning_players(ultimate_dataset)
        returned = ""
        for a, b in output:
            returned += str(a) + " $" + str(b) + '\n'



    elif entry[:7] == 'Players':

        
        players1 = entry.split('-')
        
        region = players1[1]
        team = players1[2]
        
        allplayers = players(region, team)
        
        returned = ""
        for each in allplayers:
            returned += each + '\n'

    elif entry[:6] == "boxing":
        a = entry.split('-')
        c, d = boxing(a[1])

        returned = ""

        returned += str(c) + '\n'
        
        for i in d:
            returned += i + '\n'

    
    elif entry == 'Highest KO Percentage':
        a = stats(3)
        returned = ""
        for p in a:
            returned += str(p) + '\n'

    elif entry == 'Most wins':
        w = stats(0)
        returned = ""
        for g in w:
            returned += str(g) + '\n'

    elif entry == 'Most losses':
        m = stats(1)
        returned = ""
        for h in m:
            returned += str(h) + '\n'

    elif entry == 'Most draws':
        d = stats(2)
        returned = ""
        for l in d:
            returned += str(l) + '\n'
    

    else:
        returned = "press helpNBA or helpBoxer"
            
    #this is how the text is sent to be outputed on the lower frame
    label['text'] = format_response(returned)

#all tkinter functions happen after this   
root = tk.Tk()

#the title of the window formed
root.title('Athletepedia')

#the window that is being formed
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

#the upper frame on the window where the text is being input
frame = tk.Frame(root, bg = '#80c1ff', bd = 5)
frame.place(relx = 0.5, rely = 0.1, relwidth = 0.74, relheight = 0.1, anchor = 'n')

#this is the input
entry = tk.Entry(frame, font = ('Courier', 20))
entry.place(relwidth = 0.65, relheight = 1)

#the button is pressed when input is complete
button = tk.Button(frame, text = "Enter", font = ('Courier', 15), command=lambda:test_function(entry.get()))
button.place(relx = 0.7, relheight = 1, relwidth = 0.3)

#where the output is shown
lower_frame = tk.Frame(root, bg = '#80c1ff', bd = 10)
lower_frame.place(relx = 0.5, rely = 0.25, relwidth = 0.75, relheight = 0.7, anchor = 'n')


#the the input for the output
label = tk.Label(lower_frame, font = ('Courier', 15),anchor = 'nw', justify = 'left', bd = 4)
label.place(relwidth = 1, relheight = 1)

root.mainloop()
