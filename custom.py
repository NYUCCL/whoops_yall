# this file imports custom routes into the experiment server

from flask import Blueprint, render_template, request, jsonify, Response, abort, current_app, flash
from jinja2 import TemplateNotFound
from functools import wraps
from sqlalchemy import or_, and_
from sqlalchemy.orm.exc import NoResultFound

from psiturk.psiturk_config import PsiturkConfig
from psiturk.experiment_errors import ExperimentError
from psiturk.user_utils import PsiTurkAuthorization, nocache

# # Database setup
from psiturk.db import db_session, init_db
from psiturk.models import Participant
from json import dumps, loads
from custom_models import LegitWorker
import datetime

# load the configuration options
config = PsiturkConfig()
config.load_config()
myauth = PsiTurkAuthorization(config)  # if you want to add a password protect route use this

# explore the Blueprint
custom_code = Blueprint('custom_code', __name__, template_folder='templates', static_folder='static')

###########################################################
#  serving warm, fresh, & sweet custom, user-provided routes
#  add them here
###########################################################

# Status codes
NOT_ACCEPTED = 0
ALLOCATED = 1
STARTED = 2
COMPLETED = 3
SUBMITTED = 4
CREDITED = 5
QUITEARLY = 6
BONUSED = 7

#----------------------------------------------
# example using HTTP authentication
#----------------------------------------------
@custom_code.route('/dashboard', methods=['GET','POST'])
@myauth.requires_auth
def dashboard():
    if 'mode' in request.form:
        if request.form['mode']=='add':
            if ('workerid' in request.form) and ('bonus' in request.form):
                if (LegitWorker.query.filter(LegitWorker.amt_worker_id == request.form['workerid']).count() == 0):
                    newworker = LegitWorker(workerid=request.form['workerid'])
                    newworker.set_bonus(float(request.form['bonus']))
                    db_session.add(newworker)
                    db_session.commit()
                else:
                    flash('That worker has already been added!', 'error')
        elif request.form['mode']=='delete':
            if ('index' in request.form):
                current_app.logger.info('deleting')
                try:
                    lw=LegitWorker.query.filter(LegitWorker.index == int(request.form['index'])).one()
                    db_session.delete(lw)
                    db_session.commit()
                except:
                    flash(u'Sorry, was unable to delete that worker.  Perhaps they were already deleted!', 'error')
        elif request.form['mode']=='refresh':
            failed_workers = []
            workers = LegitWorker.query.all()
            for lw in workers:
                try:
                    user = Participant.query.filter(Participant.workerid == lw.amt_worker_id).one()
                    if user.status == BONUSED:
                        try:
                            lw.paid()
                            db_session.add(lw)
                            db_session.commit()
                        except Exception as ex:
                            current_app.logger.error('Could not update worker %s to paid status: %s',
                                                lw.amt_worker_id,
                                                ex)
                            failed_workers.append(w.amt_worker_id)  
                except NoResultFound:
                    pass # hasn't submitted yet... 
                if len(failed_workers) > 0:
                    display_str = u'Could not update the following workers:'
                    for w in failed_workers:
                        display_str += '\n%s' % (w)
                    flash(display_str, 'error')
    try:
        workers = LegitWorker.query.all()
        return render_template('dashboard.html', workers = workers)
    except TemplateNotFound:
        abort(404)

#----------------------------------------------
# verify secret code
#----------------------------------------------
@custom_code.route('/check_secret_code', methods=['POST'])
def check_secret_code():
    current_app.logger.info(request.form['workerid'])
    current_app.logger.info(request.form['code'])
    uniqueId = request.form['uniqueid']
    try:
        worker = LegitWorker.query.filter(and_(LegitWorker.amt_worker_id ==request.form['workerid'], \
                                    LegitWorker.completion_code == request.form['code'], \
                                    LegitWorker.status=='owed')).one()
    except:
        abort(406)
    worker.submitted()
    db_session.add(worker)
    db_session.commit()

    try:
        user = Participant.query.\
                filter(Participant.uniqueid == uniqueId).one()
        user.bonus = worker.bonus
        user.status = COMPLETED
        user.endhit = datetime.datetime.now()
        db_session.add(user)
        db_session.commit()
    except:
        abort(406)
    resp = {"bonus": user.bonus}
    return jsonify(**resp)



    
