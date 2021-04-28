
from flask import jsonify, render_template, redirect, url_for, flash, request

from app.base import blueprint
import app.Modules.GetRouting as GetRouting
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, NewAccountForm
from app.base.models import User
from app.base.util import verify_pass
import app.Modules.connection as ConnectWith


device = None
username = None
password = None
netconf_port = None
netconf_session = None
success_login_form = None
route_session= None

@blueprint.route('/', methods=['POST', 'GET'])
def login():
    """Device authentication use Ncclient"""
    
    #Store variable globally for use later
    global success_login_form, username, password, netconf_port, device, netconf_session

    if request.form:
        # Set variable from form data. Set defaults if not entered in the login form
        if not request.form['netconfPort']:
            netconf_port = 830
        else:
            netconf_port = request.form['netconfPort']

        username = request.form['username']
        password = request.form['password']
        device = request.form['ipAddress']

        # Create NETCONF and netmiko session objects
        netconf_session = ConnectWith.create_netconf_connection(request.form['username'], request.form['password'],
                                                                request.form['ipAddress'], netconf_port)
      
        if netconf_session == 'error':
            return render_template('device_login.html', status="Login Failed")
        else:
            #Used to ensure user is authenticated prior to accessing any pages. If not 1 user is redirected to login page
            success_login_form = 1
            return redirect(url_for('base_blueprint.index'))
    else:
        return render_template('device_login.html', status=None)

@blueprint.route('/index', methods=['POST', 'GET'])
def index():
    """This page displays device interface"""

    global route_session

    if success_login_form is None:
        return redirect(url_for('base_blueprint.login'))
    elif request.form.get('getRibs'):
        #Get updated rib entries using the route_session object
        routing_information = route_session.get_routing_info(device, netconf_port, username, password)
        return jsonify({'data': render_template('updated_routes.html', routes=routing_information[1])})
    elif request.form.get('flappingRoutes'):
        #Access flapping_routes property using the route_session object
        return jsonify({'data': render_template('updated_flap_routes.html', diff_routes=route_session.flapping_routes)})
    else:
        #Create Routing object. Store variable globally
        route_session = GetRouting.Routing()
        #Using object call method to get current rib table
        routing_information = route_session.get_routing_info(device, netconf_port, username, password)
        return render_template('index.html', protocols=routing_information[0], routes=routing_information[1], diff_routes=[])

@blueprint.route('/logout')
def logout():
    """User logout"""
    
    #Clear login for variable
    success_login_form = None
    #Clear route_session object
    route_session = None

    return redirect(url_for('base_blueprint.login'))



