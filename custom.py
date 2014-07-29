# this file imports custom routes into the experiment server

from flask import Blueprint, render_template, request, jsonify, Response, abort, current_app
from jinja2 import TemplateNotFound
from functools import wraps
from sqlalchemy import or_

from psiturk.psiturk_config import PsiturkConfig
from psiturk.experiment_errors import ExperimentError
from psiturk.user_utils import PsiTurkAuthorization, nocache, print_to_log

# # Database setup
from psiturk.db import db_session, init_db
from psiturk.models import Participant
from json import dumps, loads
from custom_models import LegitWorker

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

#----------------------------------------------
# example using HTTP authentication
#----------------------------------------------
@custom_code.route('/dashboard', methods=['GET','POST'])
@myauth.requires_auth
def dashboard():
    if 'mode' in request.form:
        if request.form['mode']=='add':
            if ('workerid' in request.form) and ('bonus' in request.form):
                newworker = LegitWorker(workerid=request.form['workerid'])
                newworker.set_bonus(float(request.form['bonus']))
                db_session.add(newworker)
                db_session.commit()
        elif request.form['mode']=='delete':
            if ('index' in request.form):
                print_to_log('deleting')
                lw=LegitWorker.query.filter(LegitWorker.index == int(request.form['index'])).one()
                db_session.delete(lw)
                db_session.commit()
    try:
        workers = LegitWorker.query.all()
        return render_template('dashboard.html', workers = workers)
    except TemplateNotFound:
        abort(404)


#----------------------------------------------
# example computing bonus
#----------------------------------------------
@custom_code.route('/compute_bonus', methods=['GET'])
def compute_bonus():
    # check that user provided the correct keys
    # errors will not be that gracefull here if being
    # accessed by the Javascrip client
    if not request.args.has_key('uniqueId'):
        raise ExperimentError('improper_inputs')  # i don't like returning HTML to JSON requests...  maybe should change this
    uniqueId = request.args['uniqueId']

    try:
        # lookup user in database
        user = Participant.query.\
               filter(Participant.uniqueid == uniqueId).\
               one()
        user_data = loads(user.datastring) # load datastring from JSON
        bonus = 0

        for record in user_data['data']: # for line in data file
            trial = record['trialdata']
            if trial['phase']=='TEST':
                if trial['hit']==True:
                    bonus += 0.02
        user.bonus = bonus
        db_session.add(user)
        db_session.commit()
        resp = {"bonusComputed": "success"}
        return jsonify(**resp)
    except:
        abort(404)  # again, bad to display HTML, but...

    
