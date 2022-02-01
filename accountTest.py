import unittest
from flask import Flask, render_template, request, url_for, redirect
from app import app
from model import db, Account

class AccountTestCases(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        app.config["SERVER_NAME"] = "stefan.se"
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []  # This is the magic
        app.config['TESTING'] = True



    def test_när_inte_går_att_ta_ut_eller(self):
        test_client = app.test_client()
        url = '/insätning'
        with test_client:
            response = test_client.post(url, data={ "från":"12", "val":"withdraw", "belopp":"11122" })
            assert response.status_code == 302




    def test_när_gå_att_sätta_in_eller(self):
        test_client = app.test_client()
        url = '/insätning'
        with test_client:
            response = test_client.post(url, data={"från":"12", "val":"deposit", "belopp":"11122"  })
            assert response.status_code == 302

   
   
    def test_när_överföra_mer_pengar_än_det_finns_på_kontot_Det_ska_inte_heller(self):
        test_client = app.test_client()
        url = '/överföring'
        with test_client:
            response = test_client.post(url, data={ "från":"12", "till":"13", "belopp":"11122" })
            assert response.status_code == 302



    def test_när_inte_går_att_ta_ut_negativa_belopp(self):
        test_client = app.test_client()
        url = '/insätning'
        with test_client:
            response = test_client.post(url, data={"från":"12", "val":"withdraw", "belopp":"11122"  })
            assert response.status_code == 302




if __name__ == "__main__":
    unittest.main()
