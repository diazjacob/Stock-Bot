# Stock Bot
 I was in the market for a new graphics card in late 2021, but stock has been *horrible*. My solution was to create this stock bot to lurk websites.
 
I didn't want to rely on random Twitter or Instagram accounts to get stock updates, so I started researching the process of lurking through websites and using Python to make network requests and parse HTML/JSON. Aside from common Python networking libraries, the core libraries I used/learned were [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and [Twillow](https://www.twilio.com/docs)

Whether it's reading directly from the website HTML, or snooping around API calls, this stock bot can do it. This bot was created in a couple hours one night after being frustrated at scalper's prices. 
 
 I created this stock bot and initalized it to:
 
 - Check Memory Express stock for all 3000 series graphics cards by crawling through the HTML code on request. Doing enough checks to be informed, but not doing too many as to become timed out by their servers.
 - Check Best Buy stock for all 3000 series graphics cards by accessing the API call the page would normally request "under the hood" to get stock updates upon page load. Again only checking every little while.
 - Bring all data together to create a report on the current status of stock
 - If stock appears, immediatley send a text message to my mobile phone telling me what is available, where to get it, and a link to the store page.

## Did it work?

Yes! I retired this stock bot quicker than I thought I would. After having this stock bot run as a background process for around 20 days, I got a text message at 2pm notifying me of 12 3060 graphics cards available at Memory Express. I happend to be availble and so I ran over and snagged one, sucsess!

## What now?

In the future I'd like to make this bot much more flexible, right now it is quite dependent on many different URI string literals, and it's created to conform to the structure of the data that card seller's in Winnipeg use for their sites.
