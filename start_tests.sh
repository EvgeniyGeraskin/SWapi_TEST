#!/usr/bin/env sh
pytest --alluredir=report_allure/ sw_test.py
allure serve report_allure/