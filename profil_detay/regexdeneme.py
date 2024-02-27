from bs4 import BeautifulSoup
import re

def extract_edu_domains(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(text=True)
    matching_domains = []
    for element in elements:
        matches = re.findall(r'\b(\S*\.edu\S*)\b', element)
        matching_domains.extend(matches)
    return matching_domains

html_content = """
<div id="gsc_prf_i"><div id="gsc_prf_inw"><div id="gsc_prf_in">Osman Kilic</div></div><div class="gsc_prf_il">osman.kilic@marmara.edu.tr</div><div class="gsc_prf_il" id="gsc_prf_ivh">marmara.edu.tr üzerinde doğrulanmış e-posta adresine sahip</div><div class="gsc_prf_il" id="gsc_prf_int"><a class="gsc_prf_inta gs_ibl" href="/citations?view_op=search_authors&amp;hl=tr&amp;mauthors=label:elektrik_m%C3%BChendsili%C4%9Fi">elektrik mühendsiliği</a></div></div>
"""

edu_domains = extract_edu_domains(html_content)
for domain in edu_domains:
    print(domain)
