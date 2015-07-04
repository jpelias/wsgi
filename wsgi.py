#!/usr/bin/python2.7
# -*- coding: utf8 -*-
import os
import StringIO
import json
import logging
import random
import urllib
import urllib2
import webapp2

import multipart
# for sending images pip install -I pillow

from PIL import Image

from TwitterAPI import TwitterAPI


virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
    
#ip = os.environ['OPENSHIFT_PYTHON_IP']
#port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
#host_name = os.environ['OPENSHIFT_GEAR_DNS']


#from PIL import Image

TOKEN = '109206957:...............................'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

# ================================

#class EnableStatus(ndb.Model):
#    # key name: str(chat_id)
#    enabled = ndb.BooleanProperty(indexed=False, default=False)
    

#def setEnabled(chat_id, yes):
#    es = EnableStatus.get_or_insert(str(chat_id))
#    es.enabled = yes
#    es.put()

#def getEnabled(chat_id):
#    es = EnableStatus.get_by_id(str(chat_id))
#    if es:
#        return es.enabled
#    return False


# ================================

# Twitter Connection Info 
access_token_key = '3331408493-qnpZcbgjjru8lvCjog'
access_token_secret = 'XyrxQEm2JL5pMBStnnUFJwx2nmsNj5u8V'
consumer_key = '7YBPrscvYVeGg'
consumer_secret = 'sMO1vDysa7Ae14gOZnw'
#
#access_token_key = '33393442k0YYYhHU1BBQuhrCcf3g'
#access_token_secret = 'IJpVqWdWbpEM45Zpq8sPxPV163SAXB'
#consumer_key = '3rJOl1ODzm93FACdg'
#consumer_secret = '5jPoQs4xJqhvgNJM4awaE8'


api = TwitterAPI(consumer_key,consumer_secret,access_token_key,access_token_secret)


def UltimoTweet():

    r = api.request('statuses/user_timeline', {'screen_name ':'BTCicker' })

    #for item in r.get_iterator():
    #print ">", item
    #    if 'text' in item:
    #        print item['text']
    #print r.__dict__

    item = r.get_iterator()
    last_t = next(item)
    return  last_t['text']



def PillaJson(url):
	
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(url,headers=hdr)
	page = ""
	data = ""
	try:
		page = urllib2.urlopen(req)
		data = json.loads(page.read())
		
	except urllib2.HTTPError as e:
	
		print 'Error code: ', e.code
 
	
		
	return data


# ================================

def GetTickerData():

	lasteur_btc = ""
	lastusd_btc = "" 
	_coindesk = ""
	_btce = ""
	_kraken = "" 
	_btchina = "" 
	_okcoin = "" 
	_bitfix = "" 

	url="https://btc-e.com/api/3/ticker/btc_eur"
	data = PillaJson(url)
	if not (data == "") :
		lasteur_btc = str(round(data['btc_eur']['last'],2))


	url="https://api.bitfinex.com/v1/pubticker/btcusd"
	data = PillaJson(url)
		   
	#last = str(round(data['last_price'],2)) Se les ocurre la genial idea de poner las cantidades como string XD
	last = data['last_price']

	_bitfix = "Bitfinex:  USD "+last +"\n" 


	url="https://api.kraken.com/0/public/Ticker?pair=XXBTZEUR"
	#Parece que a la gente de Kraken no les gusta que python carge sus datos , porque con php no me pasaba				
	data = PillaJson(url)
	# Formatea una cadena a dos decimales. con Split('.') y luego last = '%s.%s%%' % (la[0], la[1][:2])
	la = data['result']['XXBTZEUR']['c'][0].split('.')
	last = '%s.%s' % (la[0], la[1][:2])
	_kraken = "Kraken: EUR "+ last +"\n" 


	url="https://data.btcchina.com/data/ticker?market=btccny"
	data = PillaJson(url)

	last = data['ticker']['last']
	_btchina = "BTC China: CNY "+last +"\n" 

	url="https://www.okcoin.com/api/ticker.do?ok=1"
	data = PillaJson(url)

	last = data['ticker']['last']
	_okcoin = "OKCoin:    USD "+ last +"\n" 
		
	url="https://api.coindesk.com/v1/bpi/currentprice.json"
	data = PillaJson(url)

	last_usd = str(round(data['bpi']['USD']['rate_float'],2))
	last_eur = str(round(data['bpi']['EUR']['rate_float'],2))
	#last_gbp = str(round(data->bpi->GBP->rate_float,2))
		
	_coindesk = "CDesk:  EUR "+ last_eur +" USD "+ last_usd + "\n"  
		
	url="https://btc-e.com/api/3/ticker/btc_usd"
	data = PillaJson(url)
	if not (data == "") :
		
		lastusd_btc = str(round(data['btc_usd']['last'],2))

	_btce = "BTC-e :   EUR "+lasteur_btc +"  USD "+lastusd_btc+"\n" 

	message = _coindesk + _btce + _kraken + _btchina + _okcoin + _bitfix  

	return message

# ================================
class HomeHandler(webapp2.RequestHandler):
	
    def get(self):
        # self.response.write('The Matrix has you.')
		self.response.out.write("""
			  <html>
				  <body onload=d=Date.now,t=d(s=0)><p style="float:left" onclick="(e=d(++s)-t)<15e3?style.margin=e%300+' 0 0 '+e*7%300:alert(s)">X</p></body>
				</html>""")
				
class MeHandler(webapp2.RequestHandler):
    def get(self):
        
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
	
    def post(self):
        
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

       
        
        if not text:
            logging.info('no text')
            return

        def reply(msg=None, img=None):
		    
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'reply_to_message_id': "" ,  #str(message_id), Eco del mensaje recibido
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)


        if text.startswith('/'):
            if text == '/start':
                reply('Bot enabled')
                
            elif text == '/stop':
                reply('Bot disabled')
                
               
            elif text == '/help':
                reply('Cotizacion Bitcoin "/ticker" ')
                
               
                
            elif text == '/falla':
				
				message = GetTickerData()			
								
				reply (message)
                
                
                
            elif text == '/tiempo':
                
				url="https://api.accuweather.com/currentconditions/v1/90399?apikey=.............................&details=true&language=es"
				hdr = {'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Mobile/7D11'}  
								
				req = urllib2.Request(url,headers=hdr)  
					
				page = ""
				data = ""
				
				try:
					page = urllib2.urlopen(req)
					data = json.loads(page.read())

				except urllib2.HTTPError as e:

					print 'Error code: ', e.code
				
				
				 
				RelativeHumidity = str(data[0]['RelativeHumidity']) 
				WeatherText = str(data[0]['WeatherText'])
				Temperature = str(data[0]['Temperature']['Metric']['Value'])
				Pressure = str(data[0]['Pressure']['Metric']['Value'])
				WindS = str(data[0]['Wind']['Speed']['Metric']['Value'])
				WindD = str(data[0]['Wind']['Direction']['Degrees'])
				WindD2 = str(data[0]['Wind']['Direction']['Localized'])
				UVIndexText = str(data[0]['UVIndexText'])
				PressureTendency = str(data[0]['PressureTendency']['LocalizedText'])
				message = WeatherText + "  "+Temperature+ u"ºC"+"  Humedad: "+RelativeHumidity+"%   PA: "+Pressure+" mb\n"
				message = message +"Viento: "+WindS+" km/h "+WindD+ u"º"+WindD2+" Indice_UV: " +UVIndexText + u"\nPresión: "+PressureTendency				
				reply(message)
                
            elif text == '/ticker':    
                
                message = UltimoTweet()
                reply(message)               
                
                
                
            elif text == '/image':
                img = Image.new('RGB', (512, 512))
                base = random.randint(0, 16777216)
                pixels = [base+i*j for i in range(512) for j in range(512)]  # generate sample image
                img.putdata(pixels)
                output = StringIO.StringIO()
                img.save(output, 'JPEG')
                reply(img=output.getvalue())
            else:
                reply('What command?')







       
application = webapp2.WSGIApplication([

    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
    ('/', HomeHandler),
], debug=True)
