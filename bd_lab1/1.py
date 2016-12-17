from lxml import etree as ET
from lxml import html as html

data = ET.Element("data")

page = html.parse('http://ru.golos.ua/')
print page

links = page.xpath('//a[contains(@href, "ru.golos.ua")]/@href')[0:20]
# print len(links)
# print links

for link in links:

    page = ET.SubElement(data, "page", url=link)

    p = html.parse(link)

    texts = p.xpath('//span/text()')
    print texts
    # for text in texts:
    #     ET.SubElement(page, "fragment", type="text").text = text.text

    imgs = p.xpath('//img/@src')

    for img in imgs:
        ET.SubElement(page, "fragment", type="image").text = img

tree = ET.ElementTree(data)
tree.write("tasf1.xml", pretty_print=True, encoding="UTF-8")