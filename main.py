import discord
import requests
from replit import db 

def getcryptoprice(crypto):
  URL ='https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
  r=requests.get(url= URL)
  data = r.json()

  for i in range(len(data)):
    db[data[i]['id']] = data[i]['current_price']

  if crypto in db.keys():
    return db[crypto]
  else:
    return None

def iscryptoSupported(crypto):
  if crypto in db.keys():
    return True
  else:
    return False

def checkPriceTrends(startPrice,endPrice,priceTargets):
    if startPrice < endPrice:
        return normal_alert(startPrice,endPrice)
    elif startPrice == endPrice:
        return []
    else:
        return reverse_alert(startPrice,endPrice,priceTargets)
        
def reverse_alert(startPrice,endPrice,priceTargets):
    db['noti'] = []
    priceTargets = priceTargets[::-1]
    for priceTarget in priceTargets:
        if endPrice <= priceTarget:
            db['noti'].append(priceTarget)
        else:
            continue
    return db['noti']
    
def normal_alert(startPrice,endPrice,priceTargets):
  db['noti']=[]
  for priceTarget in (priceTargets):
    if priceTarget <= endPrice:
      db['noti'].append(priceTarget)
      
    else:
      continue
  return db['noti']
    
def checkTwoListOrder(list1,list2):
  sorted_elemets_1 = [list1[index] <= list1[index+1] for 
  index in range(len(list1)-1)]  
  sorted_elemets_2 = [list2[index] <= list2[index+1] for 
  index in range(len(list2)-1)]  
  return all(sorted_elements_1) and all(sorted_elements_2)

async def detectPriceAlert(crypto,priceTargets):
  current_price = getcryptoprice(crypto)

  for i in range(len(SEQUENCE)):
    
    if db['hitPriceTarget'] not in range(min(current_price,db['hitPriceTarget']),max(current_price,db['hitPriceTarget'])+1) and min(priceTargets) <= current_price <= max(priceTargets):
      
      
      db['hitPriceTarget'] = 0
      
    else:
      #compute noti
      
      if len(checkPriceTrend(db['hitPriceTarget'],current_price,priceTargets))!=0:
        
        
        if db['noti']!= checkPriceTrend(db['hitPriceTarget'],current_price,priceTargets):
                #increasing in value:    
                if db['hitPriceTarget'] < current_price:
                  if checkTwoListOrder(normal_alert(db['hitPriceTarget'],current_price),db['noti']):
                    print(f'send increase noti for: {list(set(normal_alert(db["hitPriceTarget"],current_price)) - set(db["noti"]))}')
                else:    
                    print(f'send increase noti for: {list(set(normal_alert(db["hitPriceTarget"],current_price)))}')
                  
                  #decreasing in value:
                  
        elif db['hitPriceTarget'] >= current_price:    
          if checkTwoListOrder(reverse_alert(db['hitPriceTarget'],current_price,priceTargets),db["noti"]):
                        
                  print(f'send decrease noti for: {list(set(db["noti"]) - set(reverse_alert(db["hitPriceTarget"],current_price,priceTargets)))}')
          else:
            print(f'send decrease noti for: {list(set(reverse_alert(db["hitPriceTarget"],current_price,priceTargets)))}')
  else:
                pass
              
                if db['hitPriceTarget'] < current_price:  
                
                  db['noti'] = normal_alert(db['hitPriceTarget'],current_price)
                  db['hitPriceTarget'] = max(normal_alert(db['hitPriceTarget'],current_price))
                  
                  if db['hitPriceTarget'] > current_price:
                    
                    db['noti']= reverse_alert(db['hitPriceTarget'],current_price,priceTargets)
                    
                    db['hitPriceTarget'] = min(reverse_alert(db['hitPriceTarget'],current_price,priceTargets))
                    
                  else :
                    db['hitPriceTarget'] = 0
  

print(getcryptoprice('bitcoin'))

  


client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
  print(f'You are in as {client}')
  channel = discord.utils.get(client.get_all_channels(),name='general')
  

  db[db["hitPriceTarget"]] = 0
  db[db['noti']]=[]

  await client.get_channel(channel.id).send('cryptor is now online!')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('cryptor'):
    await message.channel.send('yeee_haw')

  if message.content.lower() in db.keys():
    await message.channel.send(f'At the moment {message.content} is at:{getcryptoprice(message.content.lower())} USD')

  if message.content.startswith('$list'):
    cryptoSupportedList = [key for key in db.keys()]
    await message.channel.send(cryptoSupportedList)

  if message.content.startswith('$support '):
    cryptoToBeChecked = message.content.split('$support',1)[1].lower()
    await message.channel.send(iscryptoSupported(cryptoToBeChecked))

  if message.content.startswith('howdy'):
    await message.channel.send('its always growing yo!')






BOT_TOKEN = 'MTA2ODA3NzQ3ODAyMDY1NzE2Mg.GMdkwt.5b2cZYsCI2gG58lGjH1GBdxxgt-TrkUvO2Jxvs'
client.run(BOT_TOKEN)
