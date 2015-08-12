# encoding: utf-8
import requests
import bs4
import time
import subprocess
import threading
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Monitor_lufax(object):

    def __init__(self, product):
        self.title = product.title
        self.url = product.url
        self.class_name = product.class_name
        self.logfile = product.logfile
        self.mail_list = ['#####@yeah.net', '####@yeah.net']

    def monitor(self):
        found = False
        start = None
        end = None
        while True:
            res = requests.get(self.url)
            result = bs4.BeautifulSoup(res.text)
            output = result.find_all('li', {"class": self.class_name})

            if output:
                if not found:
                    start = time.time()
                    with open(self.logfile, 'a') as f:
                        f.write('Found at {}\n'.format(time.ctime()))
                    found = True
                    body = result.select('ul.main-list')[0].getText().strip()
                    subprocess.Popen("echo '{0}' |mail -s 'Lufax product-{2} is open!' {1}".format(body, ' '.join(self.mail_list), self.title),
                                     shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif start:
                end = time.time()
                with open(self.logfile, 'a') as f:
                    f.write('It last {} second]\n\n'.format(int(end-start)))
                start = None
                end = None
            else:
                found = False
                #print '{} not found'.format(self.title)
            time.sleep(10)


class Product(object):
    def __init__(self, url, title, class_name):
        self.url = url
        self.class_name = class_name
        self.title = title
        self.logfile = '/root/.product-' + title


if __name__ == '__main__':
    piaoju = Product(url='http://list.lufax.com/list/piaoju?lufax_ref=http%3A%2F%2Fwww.lufax.com%2F', title='piaoju', class_name="product-list product-piaoju clearfix ")
    rensheng = Product(url='https://list.lufax.com/list/fuying?lufax_ref=https%3A%2F%2Flist.lufax.com%2Flist%2Ftouzi', title='rensheng', class_name='product-list clearfix ')
    monitor_piaoju = Monitor_lufax(piaoju)
    monitor_rensheng = Monitor_lufax(rensheng)
    threads = [threading.Thread(target=monitor_piaoju.monitor), threading.Thread(target=monitor_rensheng.monitor)]
    for t in threads:
        t.start()



