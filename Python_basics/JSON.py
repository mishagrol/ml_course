import json 
filename = 'user_setting.json'
player_1 = {
    'Name':'Donald Trump',
    'Score':345,
    'Award':['NY', 'Arizona', 'Minesota']
}
player_2 = {
    'Name':'Hillary Clinton ',
    'Score':325,
    'Award':['Texac', 'Alyaska', 'Messury']
}

myplayers = []
myplayers.append(player_1)
myplayers.append(player_2)

json.dump( )