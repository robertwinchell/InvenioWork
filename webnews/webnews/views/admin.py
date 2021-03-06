# -*- coding: utf-8 -*-

"""webnews Flask Blueprint"""
from flask import Flask
from flask.ext.login import login_required
from flask import request, url_for, g, Markup, redirect, flash,Blueprint,render_template
from flask.ext import menu
from ..models import  NwsToolTip,NwsSTORY,NwsTAG
from flask.ext.menu import register_menu
from invenio.ext.principal import permission_required
from sqlalchemy.exc import IntegrityError
from werkzeug.debug import DebuggedApplication
from invenio.ext.sqlalchemy import db

from ..encoder import Encode,Decode
from .. import config



blueprint = Blueprint('webnews.admin', __name__, template_folder='../templates',static_folder='../static' )

# For Object Insert
@blueprint.route(config.CFG_WEBNEWS_ADMIN_INSERT, methods=['GET', 'POST'])
@login_required
@permission_required(config.CFG_WEBNEWS_WEBACCESSACTION)
#@register_menu(blueprint, 'main.admin.Insert',config.CFG_WEBNEWS_ADMIN_MENU_INSERT)
def Insert():
    if request.method == 'POST':
        try:
            if request.form.get('_action',None)==config.CFG_WEBNEWS_ADMIN_ACTION_NEWS:
                new_story = NwsSTORY(title=str(request.form.get('txtTitle',None)),
                                     body=str(request.form.get('txtBody_news',None)),
                                     document_status=str(request.form.get('st_document_status',None)),
                                     remote_ip=str(request.form.get('remote_ip',None)),
                                     email=str(request.form.get('email',None)),
                                     nickname=str(request.form.get('nickname',None)),
                                     uid=int(request.form.get('uid',None)))
                db.session.add(new_story)
                db.session.commit()
                flash(config.CFG_WEBNEWS_SUCCESS_RECORD_ADDED)
                alert=config.CFG_WEBNEWS_SUCCESS_ALERT
                return  redirect(config.CFG_WEBNEWS_ADMIN_UPDATE+'/?id='+str(Encode(new_story.id)))
            elif request.form.get('_action',None)==config.CFG_WEBNEWS_ADMIN_ACTION_TOOLTIP:
                new_tooltip = NwsToolTip(body=str(request.form.get('txtBody_tooltip',None)),
                                         target_element=str(request.form.get('txttarget_element',None)),
                                         target_page=str(request.form.get('txttarget_page',None)),
                                         id_story=int(Decode(request.form.get('_newsID',Encode(0)))))
                db.session.add(new_tooltip)
                db.session.commit()
                flash(config.CFG_WEBNEWS_SUCCESS_RECORD_ADDED)
                alert=config.CFG_WEBNEWS_SUCCESS_ALERT

            elif request.form.get('_action',None)==config.CFG_WEBNEWS_ADMIN_ACTION_TAG:
                print(request.form.get('_newsID',0))
                new_tag = NwsTAG(tag=str(request.form.get('txttag',None)),
                                 id_story=int(Decode(request.form.get('_newsID',Encode(0)))))
                db.session.add(new_tag)
                db.session.commit()
                flash(config.CFG_WEBNEWS_SUCCESS_RECORD_ADDED)
                alert=config.CFG_WEBNEWS_SUCCESS_ALERT
            id=int(Decode(request.form.get('_newsID',Encode(0))))
            #result = NwsSTORY.query.get(id)
            return  redirect(config.CFG_WEBNEWS_ADMIN_UPDATE+'/?id='+str(Encode(id)))
            #return  render_template('admin/update.html',EncodeStr=Encode, searchResult=result ,display_forms=['normal','none','none'])   # [news,tooltip,tag]
        except IntegrityError, e:
            return e
    else:
        try:
            formAct = request.args.get('formAct', Encode(None))
            id=Decode(request.args.get('id', Encode(0)))
            if Decode(formAct)=='1':
                return render_template('admin/insert.html' ,EncodeStr=Encode,display_forms=['none','normal','none'],id=id)   # [news,tooltip,tag]
            elif Decode(formAct)=='2':
                return render_template('admin/insert.html' ,EncodeStr=Encode,display_forms=['none','none','normal'],id=id)   # [news,tooltip,tag]
            else:
                return render_template('admin/insert.html' ,EncodeStr=Encode,display_forms=['normal','none','none'])   # [news,tooltip,tag]
        except IntegrityError, e:
                flash('Error')
                alert=config.CFG_WEBNEWS_ERROR_ALERT

# For Object Update
@blueprint.route(config.CFG_WEBNEWS_ADMIN_UPDATE, methods=['GET', 'POST'])
@login_required
@permission_required(config.CFG_WEBNEWS_WEBACCESSACTION)
def Update():

    stid=0
    if request.method == 'POST':
        try:
            id = int(Decode(request.form.get('_newsID',Encode(0))))
            if request.form.get('_action',None)==config.CFG_WEBNEWS_ADMIN_ACTION_NEWS:
                new_story=NwsSTORY.query.get(id)
                new_story.title=str(request.form.get('story_txtTitle',None))
                new_story.body=str(request.form.get('story_txtBody',None))
                new_story.document_status=str(request.form.get('story_docStatus',None))
                db.session.commit()
                return  redirect(config.CFG_WEBNEWS_ADMIN_EDIT)
            if request.form.get('_action',None)==config.CFG_WEBNEWS_ADMIN_ACTION_TOOLTIP:
                tooltipid = int(Decode(request.form.get('_tooltipID',Encode(0))))
                new_tooltip=NwsToolTip.query.get(tooltipid)
                new_tooltip.body=str(request.form.get('txtBody_tooltip',None))
                new_tooltip.target_element=str(request.form.get('txttarget_element',None))
                new_tooltip.target_page=str(request.form.get('txttarget_page',None))
                db.session.commit()
                id=new_tooltip.id_story

            elif request.form.get('_action',None)==config.CFG_WEBNEWS_ADMIN_ACTION_TAG:
                tagid =  int(Decode(request.form.get('_tagID',Encode(0))))
                new_tag=NwsTAG.query.get(tagid)
                new_tag.tag=str(request.form.get('txttag',None))
                db.session.commit()
                flash(config.CFG_WEBNEWS_SUCCESS_RECORD_ADDED)
                alert=config.CFG_WEBNEWS_SUCCESS_ALERT
                id=new_tag.id_story
            return  redirect(config.CFG_WEBNEWS_ADMIN_UPDATE+'/?id='+str(Encode(id)))
        except IntegrityError, e:
            flash('Error')
            alert=config.CFG_WEBNEWS_ERROR_ALERT


    else:
        try:
            formAct = Decode(request.args.get('formAct', Encode(None)))
            id=int(Decode(request.args.get('id', Encode(0))))
            if formAct=='1':
                result = NwsToolTip.query.get(id)
                return render_template('admin/update.html',EncodeStr=Encode, searchResult=result,display_forms=['none','normal','none'],id=id)   # [news,tooltip,tag]
            elif formAct=='2':
                result = NwsTAG.query.get(id)
                return render_template('admin/update.html',EncodeStr=Encode, searchResult=result ,display_forms=['none','none','normal'],id=id)   # [news,tooltip,tag]
            else:
                result = NwsSTORY.query.get(id)
                return render_template('admin/update.html',EncodeStr=Encode, searchResult=result ,display_forms=['normal','none','none'])   # [news,tooltip,tag]
        except IntegrityError, e:
                flash('Error')
                alert=config.CFG_WEBNEWS_ERROR_ALERT

#For Object Edit
@blueprint.route(config.CFG_WEBNEWS_ADMIN_EDIT, methods=['GET', 'POST'])
@login_required
@permission_required(config.CFG_WEBNEWS_WEBACCESSACTION)
@register_menu(blueprint, 'main.admin.Edit',config.CFG_WEBNEWS_ADMIN_MENU_EDIT)
def EDIT():
    if request.method == 'POST':
         result = NwsSTORY.query.filter(NwsSTORY.title.contains(request.form['keywords']) | NwsSTORY.body.contains(request.form['keywords'])).all()
         return render_template('admin/Edit.html',searchResult=result,resultshow='block')
    result = NwsSTORY.query.order_by(NwsSTORY.id.desc()).limit(config.CFG_WEBNEWS_ADMIN_SHOWRECORDS).all()
    return render_template('admin/Edit.html',searchResult=result,resultshow='block',EncodeStr=Encode, str=str)


# For Object Delete
@blueprint.route(config.CFG_WEBNEWS_ADMIN_DELETE, methods=['GET', 'POST'])
@login_required
@permission_required(config.CFG_WEBNEWS_WEBACCESSACTION)
def DELETE():
    try:
        formAct = Decode(request.args.get('formAct', Encode(None)))
        id= int(Decode(request.args.get('id',Encode(0))))
        if formAct=='1':
            new_tooltip = NwsToolTip.query.get(id)
            db.session.delete(new_tooltip)
            db.session.commit()
            return redirect(request.referrer)
        elif formAct=='2':
            new_tag=NwsTAG.query.get(id)
            db.session.delete(new_tag)
            db.session.commit()
            return redirect(request.referrer)
        else:
            new_story=NwsSTORY.query.get(id)
            db.session.delete(new_story)
            db.session.commit()
            return redirect(config.CFG_WEBNEWS_ADMIN_EDIT)
    except IntegrityError, e:
        flash('Error')
        alert=config.CFG_WEBNEWS_ERROR_ALERT
