from django.shortcuts import render
from Forms.models import Forms, Fields, Values, Emails,SecondValues
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import CreateView, TemplateView
from validate_email import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage

from django.http import HttpResponseForbidden, HttpResponse
import threading
from threading import Thread
import sys
from project import settings
import json



class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, email_list):
        self.subject = subject
        self.email_list = email_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.email_list)
        msg.content_subtype = "html"
        msg.send()

def send_html_mail(subject, html_content, email_list):
    EmailThread(subject, html_content, email_list).start()


class FormsMetm(TemplateView):
    model = Fields
    template_name = 'index.html'
 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objects = Forms.objects.filter(pk=context['id']).first()
        context["objects"] = objects
        

        return context

  
    def post(self, request, *args, **kwargs):
        err_list = []
        context = dict()
        objects = Forms.objects.filter(pk=kwargs['id']).first()
        # print(objects,"FFFFFFFFFFFFFFFFFFFFFFFFFFf")
        context["objects"] = objects
        global email_value
        email_value = {}
        # print(self.request.POST[field])
        
        for field in self.request.POST:  
            if field == 'csrfmiddlewaretoken':
                continue
            else:
                print(self.request.POST[field],'AAAAAAAAAAAAAAAAAAAAAA')
                
                input_name = field.split("-")
                
                field_id = input_name[1]
                field_label = input_name[0]
                # print(field_label)
                fields = Fields.objects.filter(id=field_id).first().get_type()
                require = Fields.objects.filter(id=field_id ,requirement = True).first()
                # print(require,'ALALALALALAALALLAAL')
                
                
                main_field = Fields.objects.filter(label=field_label).first()

                is_valid = False
                if fields == '1':
                    a=request.POST.get(field, "")
                   
                  
                    if len(a) == 0 and require:
                        
                        err_list.append({field_label:'Bosh buraxmaq olmaz'})
                        context["err_list"] = err_list
                    
                
                if fields == '2':
                    nomre = request.POST.get(field, "")
                    
                   
                    if len(nomre) == 0 and require:
                      
                        err_list.append({field_label:'bosh buraxmaq olmaz'})
                        context["err_list"] = err_list

                    if not nomre.isdigit() and len(nomre)!=0:
                        err_list.append({field_label:'Duzgun nomre daxil edin'})
                        context["err_list"] = err_list


                if fields == '6' and require:
                    email = request.POST.get(field, "")
                    if len(email) == 0:
                        err_list.append({field_label:'bosh buraxmaq olmaz'})
                        context["err_list"] = err_list


                        is_valid = validate_email(email_address=email, check_regex=True, check_mx=True, from_address='my@from.addr.ess',
                                helo_host='localhost', smtp_timeout=10, dns_timeout=10, use_blacklist=True, debug=False)
                        if not is_valid:
                            err_list.append({field_label:'Duzgun email daxil edin'})
                            context["err_list"] = err_list

                email = request.POST.get(field, "")
                if fields == '6' and len(email)!=0:
                    email = request.POST.get(field, "")
                    is_valid = validate_email(email_address=email, check_regex=True, check_mx=True, from_address='my@from.addr.ess',
                            helo_host='localhost', smtp_timeout=10, dns_timeout=10, use_blacklist=True, debug=False)
                    if not is_valid:
                        err_list.append({field_label:'Duzgun email daxil edin'})
                        context["err_list"] = err_list

                
        if len(err_list) == 0:
                                
            form = SecondValues(forms=objects,
                              datas=json.dumps(self.request.POST))
            form.save()
            
            for field in self.request.POST:  
                if field == 'csrfmiddlewaretoken':
                    continue
                else:
                    dicti = {
                        field : self.request.POST[field]
                    }
                    email_value=dicti
            subject = 'Form datas'
            emails = Emails.objects.filter(forms__id=kwargs['id']).values_list('email', flat=True)
            context = {
                    'value_list':email_value,
                 }
            template_name = 'email.html'
            msg = render_to_string(template_name , context)
            template = msg
            send_html_mail(subject,template,emails) 
            return render(request, 'index2.html')
        return render(request, 'index.html',context)






