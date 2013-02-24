from .models import *
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, render_to_response, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.gis.geos import Point
from vectorformats.Formats import Django, GeoJSON
from django.utils.safestring import SafeString
import simplejson


def index(request):
    geoj = GeoJSON.GeoJSON()
    djf = Django.Django(geodjango='geom', properties=['description'])
    issues = geoj.encode(djf.decode(Issue.objects.all()))
    return render_to_response('index.html', {'issues': SafeString(issues)}, RequestContext(request))

def all_issues(request):
    geoj = GeoJSON.GeoJSON()
    djf = Django.Django(geodjango='geom', properties=['description'])
    issues = geoj.encode(djf.decode(Issue.objects.filter(status='open')))
    print issues
    return render_to_response('mapview.html', {'issues': SafeString(issues)}, RequestContext(request))


def all_issues_ajax(request):
    issues= Issue.objects.filter(status='open')
    t_issues =[]
    for issue in issues:
        t_issue ={}
        #t_issue= dict((x.name, getattr(issue, x.name)) for x in issue._meta.fields)
        for field in issue._meta.fields:
            if field.name != 'geom' and field.name != 'after_img' and field.name !='before_img':
                t_issue[field.name]=str(getattr(issue, field.name))
        t_issue['lat']=issue.geom.get_x()
        t_issue['lng']=issue.geom.get_y()
        t_issues.append(t_issue)
    return render_to_response('mapview.html', {'issues': SafeString(simplejson.dumps(t_issues))}, RequestContext(request))

@csrf_exempt
def open_issue(request):
    if request.method == 'POST':
        status = 'open'

        data = simplejson.loads(request.raw_post_data)

        user = User.objects.get(pk=data['user_id'])
        category = Category.objects.get(pk=1) #data['category_id']
        location_type = LocationType.objects.get(pk=data['location_type_id'])

        description = data['description']
        #TODObefore_img = data['before_img']

        reported_to_311 = data['reported_to_311']
        longitude = data['longitude']
        latitude = data['latitude']

        pnt = Point(float(longitude), float(latitude))
        issue = Issue(status=status, opener=user, description=description, #before_img=before_img,
                      category=category, reported_to_311=reported_to_311, location_type=location_type,
                      geom=pnt)
        issue.save()

        report = IssueUser(issue=issue, user=user)
        report.save()

        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


@csrf_exempt
def close_issue(request):
    if request.method == 'POST':
        data = simplejson.loads(request.raw_post_data)
        status = 'closed'
        issue = Issue.objects.get(pk=data['issue_id'])
        issue.after_img = data['after_img']
        issue.status = status
        issue.closer = User.objects.get(pk=data['closer_id'])
        issue.cleaner = User.objects.get(pk=data['cleaner_id'])
        issue.save()
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


@csrf_exempt
def reup_issue(request):
    if request.method == 'POST':
        data = simplejson.loads(request.raw_post_data)
        issue = Issue.objects.get(pk=data['issue_id'])
        user = User.objects.get(pk=data['user_id'])

        report = IssueUser(issue=issue, user=user)
        report.save()
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


@csrf_exempt
def create_pledge(request):
    if request.method == 'POST':
        data = simplejson.loads(request.raw_post_data)
        user = User.objects.get(pk=data['user_id'])
        longitude = data['longitude']
        latitude = data['latitude']
        pnt = Point(longitude, latitude)

        pledge = Pledge(user=user, geom=pnt)
        pledge.save()
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')

@csrf_exempt
def claim_issue(request):
    if request.method == 'POST':
        data = simplejson.loads(request.raw_post_data)
        user = User.objects.get(pk=data['user_id'])
        issue = Issue.objects.get(pk=data['issue_id'])

        claim = Claim(user=user, issue=issue)
        claim.save()
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')