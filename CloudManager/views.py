from django.http import HttpResponse
from euca import Euca
import CloudKingdom.settings as conf

driver = Euca(conf.EC2_ACCESS_KEY, conf.EC2_SECRET_KEY, conf.EC2_HOST, conf.EC2_PORT)

def index(request):

	print driver.conn.list_images()

	return HttpResponse("hello")
