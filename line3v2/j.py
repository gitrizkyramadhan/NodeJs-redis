from datetime import datetime
import random, string
code = 'askmdncjndjvxjsovjsgchxzsknsnzvbk' + datetime.now().strftime('%Y%m%d%H%M%S') + 'bangjoni'

data = 'njsnjfndjfbvjdvnxnckdnvjdvnjdnvs'
print len(data)
# strs = 'abcdefghijklmnopqrstuvwxyz0123456789'
strs = '9876543210zyxwvutsrqponmlkjihgfedcba'
#use a string like this, instead of ord()
def shifttext(shift):
    inp = strs
    data = []
    for i in inp:                     #iterate over the text not some list
        if i.strip() and i in strs:                 # if the char is not a space ""
            data.append(strs[(strs.index(i) + shift) % 26])
        else:
            data.append(i)           #if space the simply append it to data
    output = ''.join(data)
    print output
    return output

# def genToken(digits):
#
#     return ''.join(random.choice(string.lowercase) for i in range(digits))

def getKeyUrl(msisdn):

    time = datetime.now().strftime('%Y%m%d%H%M%S')
    code = 'fbm' + msisdn  + str(time) + 'bangjoni'
    return code

key = getKeyUrl('njsnjfndjfbvjdvnxnckdnvjdvnjdnvs')

print key
print key[:3]
print key[3:35]
print key[35:48]



