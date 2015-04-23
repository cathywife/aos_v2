# coding: utf-8
from __future__ import unicode_literals
import os
from optparse import OptionParser

from django.core.management.base import BaseCommand, CommandError
from host.models import Host, Service, CloudAndService

parser = OptionParser() 
cloudandservice_all = ''
status_desc_all = ''
service_desc_all = ''
host_type_all = ''
host_model_all = ''
host_image_all = ''
i = 1
d = 1

for cloudandservice in CloudAndService.objects.all():
    cloudandservice_all +=  "cloudandservice_id:%d-%s " % (i, cloudandservice)
    i += 1
#for service_desc in Service.objects.filter(id__in=Host.objects.values_list('service').distinct()).values_list('name', flat=True):
for service_desc in Service.objects.all():
    service_desc_all +=  "service_id:%d-%s " % (d, service_desc)
    d += 1
for host_type in Host.HOST_TYPE:
    host_type_all +=  "host_type_id:%d-%s " % (host_type[0], host_type[1])
for host_model in Host.HOST_MODEL:
    host_model_all +=  "host_model_id:%d-%s " % (host_model[0], host_model[1])
for host_image in Host.HOST_IMAGE:
    host_image_all +=  "host_image_id:%d-%s " % (host_image[0], host_image[1])
for status_desc in Host.HOST_STATUS:
    status_desc_all +=  "status_id:%d-%s " % (status_desc[0], status_desc[1])

class Command(BaseCommand):
    #option_list = BaseCommand.option_list + (

    def usage(self, subcommand):
        """
        Return a brief description of how to use this command, by
        default from the attribute ``self.help``.

        """
        #usage = 'python %%prog %s --name test123 --ip_in ip.list --idc 1 --service 1 --type 0 --status 0 --comment test-test %s' % (subcommand, self.args)
        usage = 'python %%prog %s --name test123 --ip_in ip.list --model 0  --image 0 --cloudandservice 1 --service 1 --type 0 --status 0 %s' % (subcommand, self.args)
        if self.help:
            return '%s\n\n%s' % (usage, self.help)
        else:
            return usage

    option_list = BaseCommand.option_list + (
#    option_list = (
        parser.add_option(str('-n'), '--name',   action='store', dest='name',  default=False, type='string', help='添加主机名'),
        parser.add_option(str('-i'), '--ip_in',  action='store', dest='iplist', default=False, type='string', help='一个ip.list文件(一行一个ip)'),
        parser.add_option(str('-o'), '--ip_out', action='store', dest='ip_out',default='', type='string', help='添加外网IP地址,默认为空'),
        parser.add_option(str('-m'), '--model', action='store', dest='model',default='', type='string', help=host_model_all),
        parser.add_option(str('-a'), '--image', action='store', dest='image',default='', type='string', help=host_image_all),
        parser.add_option(str('-d'), '--cloudandservice',    action='store', dest='cloudandservice',  default=False, type='string', help=cloudandservice_all),
        parser.add_option(str('-s'), '--service',  action='store', dest='service', default=False, type='string', help=service_desc_all),
        parser.add_option(str('-t'), '--type', action='store', dest='type',default=False, type='string', help=host_type_all),
        parser.add_option(str('-u'), '--status',  action='store', dest='status', default=False, type='string', help=status_desc_all),
        #parser.add_option(str('-c'), '--comment', action='store', dest='comment',default=False, type='string', help='添加备注信息'),
        )

    def handle(self, *args, **options):
        (options, args) = parser.parse_args() 
        file_path = os.path.abspath(options.iplist)
        ip_list = open(file_path)
        for ip in ip_list:
            #print ip,
            ip = ip.strip('\n')
            h = Host(name=options.name, ip_in=ip, ip_out=options.ip_out, model=options.model, image=options.image, cloudandservice_id=options.cloudandservice, service_id=options.service, type=options.type, status=options.status)
            #h = Host(name=options.name, ip_in=ip,  internetdatacenter_id=options.internetdatacenter, service_id=options.service, type=options.type, status=options.status)
            h.save()     
            #h.hostcomment_set.create(comment=options.comment)

