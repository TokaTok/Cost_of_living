# initialization

from slnm import gather 

lst = ["Dubai","Lisbon"]
case = "მინიმალური"
gather(lst)

# pip install -r requirements.txt   ---  install
# pip freeze > requirements.txt   ---  generate

import pandas as pd
places_data = {}
for place in lst:    
    df = pd.read_excel(f"{place}_data.xlsx")   
    df = df.rename(columns={"Unnamed: 0":"ინდექსი"})
    df = df.set_index("ინდექსი")
    df = df.ffill()
    df["რეალური საშუალო"] = round(df["მინიმალური"]+( df["მაქსიმალური"] - df["მინიმალური"] )  /2 , 2)  

    places_data[place] = df

# df = pd.concat(places_data.values(), axis=1,keys = places_data.keys())
df = pd.concat(places_data.values(), axis=1, keys = [lst[0],lst[1]])
df["difference"] = df[lst[1]][case] - df[lst[0]][case]






def is_True(num):
    if str(num)[0] == "-":
        return 'background-color: lime'
    
def is_False(num):
    if str(num)[0] != "-":
        return 'background-color: red'
df = df.style.applymap(is_True, subset=['difference'])
df = df.applymap(is_False, subset=['difference'])
df.to_excel("result.xlsx")