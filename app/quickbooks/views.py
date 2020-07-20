import json
import requests
import datetime
from flask import Flask,render_template, redirect, url_for, request, current_app, Blueprint, Response
from datetime import datetime
from flask.views import MethodView
from jinja2 import Markup
from flask_sqlalchemy import SQLAlchemy
from models.quickbooks_position import QuickbooksPosition
from models.quickbooks_form import QuickBooksForm
from services.db import DB as db
from hcg_utils.authentication.utils import current_user

QUIKBOOKS = Blueprint('quickbooks',__name__, template_folder='templates')

class FormQuickbook(MethodView):
    def get(self):
        return render_template(
            'quickbooks/quickbook-position.html'
        )

class SavePosition(MethodView):
    def post(self):
        form = QuickBooksForm(request.form)
        as_of_date = datetime.utcnow()
        submitter = current_user.identifier
        if not form.validate():
            render_template('quickbooks/error-page.html', exception='Please verify your data'), 400 
        """         
        else:
            wisetack_junior_position = form.wisetack_junior_position.data
            lighter_junior_position = form.lighter_junior_position.data
            form_period = form.period.data """
        position = QuickbooksPosition(
            submitter,
            as_of_date,
            period=form.period.data,
            wisetack_junior_position=form.wisetack_junior_position.data,
            lighter_junior_position=form.lighter_junior_position.data
        )
        try:
            db.session.add(position)
            db.session.commit()
        except Exception:
            current_app.logger.exception('Please verify your data')
            return render_template(
                'quickbooks/error-page.html',
                exception = 'Please verify your data',
            ) , 400
        return render_template(
            'quickbooks/success-page.html'
        )

QUIKBOOKS.add_url_rule('/', view_func=FormQuickbook.as_view('form_quickbook'))
QUIKBOOKS.add_url_rule('/save_position', view_func=SavePosition.as_view('save_position'))