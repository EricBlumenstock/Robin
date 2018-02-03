from Robinhood.Robinhood import Robinhood

rh = Robinhood()
RESET = '\u001b[0m'
BOLD = '\u001b[1m'
UNDERLINE = '\u001b[4m'
RED = '\u001b[1;31;40m'
REDBG = '\u001b[7;31;40m'
GREEN = '\u001b[1;32;40m'
GREENBG = '\u001b[7;32;40m'
WHITEBG = '\u001b[7;33;40m'
def color_print(color, item : str):
    print(color + item + RESET)

width = 43
header = str('\u2502' + ' {:^7} \u2502'*4).format(' Symbol', 'Price', 'Ask', 'Bid').center(width)
color_print(WHITEBG, header)

stocks =  [rh.quote_data('TQQQ'), rh.quote_data('UDOW')]
for i in stocks:
    print(str('\u2502 {:^7} \u2502' + ' {:^7.2f} \u2502'*3).format(i['symbol'], float(i['last_trade_price']) ,float(i['ask_price']), float(i['bid_price'])).center(width))
#Yesterday's mean moving avg
#Today's mean moving avg so far
#Tick history
#Tick summary amount for history
#Color numbers green/red according to whether number went higher or lower compared to last, white if same
#Mark extreme gain/losses
#Sentiment
print('\u2501'*width)

def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')
