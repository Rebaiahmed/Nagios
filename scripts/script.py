import pynag.Model , all_services , pynag.Model.Service.objects.all

myhost = pynag.Model.Host.objects.get_by_shortname('host1')
#myhost.address = '127.0.0.1'
#myhost.save()
# See what the host definition looks like after change:
print myhost


print("*************")



for i in all_services:
	print i.host_name, i.service_description
