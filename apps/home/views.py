# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import jwt
import time
import plotly.express as px
import random

METABASE_SITE_URL = "http://localhost:3000"
METABASE_SECRET_KEY = "7362a9de69737dd5ae8611a1fdd748ac23a9ad08d982f1a598f2cbcf2261ded3"

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    payload = {
    "resource": {"question": 1},
    "params": {
        
    },
    "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }

    x = [round(random.uniform(1, 20), 2) for _ in range(50)]
    y = [round(random.uniform(1, 20), 2) for _ in range(50)]
    fig = px.scatter(x=x, y=y)
    fig.update_layout(
        width=610,  # Set the width of the plot
        height=597,  # Set the height of the plot
    )

    fig.update_layout(
        title_text="Clubs Shot x xG Performance",  # Set the title text
        title_x=0.5,  # Set the title's horizontal position (0.5 is centered)
        title_font=dict(family='Roboto', size=24)
    )

    plot_html = fig.to_html(full_html=True)


    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

    iframeUrl = METABASE_SITE_URL + "/embed/question/" + token + "#bordered=true&titled=true"
    context['iframeUrl'] = iframeUrl
    context['plotlyframe'] = plot_html

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
