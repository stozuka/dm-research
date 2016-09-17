#coding: utf-8
import requests
import keys
import xml.etree.ElementTree as ET

def yahoo_morpho_api(body):
    URL = "http://jlp.yahooapis.jp/MAService/V1/parse"
    params = {'appid': keys.YAHOO_APP_ID,
                'sentence': body,
                'results': 'ma'}
    r = requests.post(URL, params=params)
    return r.text

def parse_xml(morpho_xml_str):
    segmented_text = []
    root = ET.fromstring(morpho_xml_str)
    for surface in root.iter('{urn:yahoo:jp:jlp}surface'):
        segmented_text.append(surface.text)
    segmented_text = ' '.join(segmented_text)
    return segmented_text

if __name__ == '__main__':
    morpho_xml_str = yahoo_morpho_api(body="すもももももももものうち。")
    segmented_text = parse_xml(morpho_xml_str)
    print(segmented_text)
