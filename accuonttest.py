import unittest
from flask import Flask, render_template, request, url_for, redirect
from app import app
from model import db, Account

class AccountTestCases(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        app.config["SERVER_NAME"] = "Hej.se"
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []  # This is the magic
        app.config['TESTING'] = True



    def test_när_inte_går_att_ta_ut_än_perngar_som_finns_på_kontot(self):
        test_client = app.test_client()
        url = '/insätning'
        with test_client:
            response = test_client.post(url, data={ "från":"1", "val":"withdraw", "belopp":"16000" })
            assert response.status_code == 302




    def test_när_gå_att_sätta_in_perngar_på_konto(self):
        test_client = app.test_client()
        url = '/insätning'
        with test_client:
            response = test_client.post(url, data={"från":"1", "val":"deposit", "belopp":"16000"  })
            assert response.status_code == 302




    def test_när_går_att_ta_ut_pengar_på_kontot(self):
        test_client = app.test_client()
        url = '/insätning'
        with test_client:
            response = test_client.post(url, data={"från":"1", "val":"deposit", "belopp":"5"  })
            assert response.status_code == 302



   
   
    def test_när_överföra_mer_pengar_än_det_finns_på_kontot(self):
        test_client = app.test_client()
        url = '/överföring'
        with test_client:
            response = test_client.post(url, data={ "från":"1", "till":"13", "belopp":"14000" })
            assert response.status_code == 302



   


    def test_när_inte_går_att_ta_ut_negativa_belopp(self):
        test_client = app.test_client()
        url = '/insätning'
        with test_client:
            response = test_client.post(url, data={"från":"1", "val":"withdraw", "belopp":"-5"  })
            assert response.status_code == 302


if __name__ == "__main__":
    unittest.main()
