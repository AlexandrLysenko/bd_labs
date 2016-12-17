from lxml import html
from lxml import etree as ET

data = ET.Element('data')

main_page = html.parse('http://uartlib.org/')

print(main_page)

links = main_page.xpath('//a[contains(@href, "uartlib.org")]/@href')[0:20]
print(links)


def task1():
    for link in links:
        main_page = ET.SubElement(data, "main_page", url=link)
        p = html.parse(link)
        texts = p.xpath('//*[not(self::script) and not(self::style)][text()]')
        for text in texts:
            ET.SubElement(main_page, "fragment", type="text").text = text.text

        imgs = p.xpath('//img/@src')

        for img in imgs:
            ET.SubElement(main_page, "fragment", type="image").text = img
    tree = ET.ElementTree(data)
    tree.write("task1.xml", pretty_print=True, encoding="UTF-8")




def task2():
    stats = {}

    tree = ET.parse('task1.xml')
    data = tree.getroot()

    def selectMidStats(stats):
        mid_text = 0
        for stat in stats:
            mid_text += stats[stat]['text']

        print mid_text / len(stats)

    for page in data:
        stat = {}
        stat['text'] = page.xpath('count(fragment[@type="text"])')
        stat['img'] = page.xpath('count(fragment[@type="image"])')

        stats[page.attrib['url']] = stat

    selectMidStats(stats)


def task3():
    root = ET.Element('data')
    page = html.parse('http://www.hozmart.com.ua')
    category_list = page.xpath(
        '//ul[@class="reset"]/li[contains(a/@href, "28-otdykh-i-turizm")]/div/ul[@class="inner"]/li/ul/li/a/@href')
    product_list = []

    for category in category_list:
        category_page = html.parse(category)
        product_list.extend(category_page.xpath('//ul[@id="product_list"]/li/div[@class="center_block"]/h3/a/@href'))
        if len(product_list) >= 20: break
    product_list = product_list[0:20]

    for link in product_list:

        prod_xml = ET.SubElement(root, 'product')

        product = html.parse(link)

        title = product.xpath('//div[@id="primary_block"]/h1').pop().text
        title_xml = ET.SubElement(prod_xml, 'title')
        title_xml.text = title

        image = product.xpath(
            '//div[@id="primary_block"]/div[@id="pb-right-column"]/div[@id="image-block"]/span/img/@src').pop()
        img_xml = ET.SubElement(prod_xml, 'image')
        img_xml.text = image

        price = product.xpath('//div[@id="primary_block"]/div[@class="pb-center-column"]/div[@class="price"]/p/span')

        if len(price) != 0:
            price = price.pop().text
        else:
            price = 'no price'

        price_xml = ET.SubElement(prod_xml, 'price')
        price_xml.text = price

        path = '//div[@id="primary_block"]/div[@id="pb-left-column"]/div[@id="short_description_block"]/div/table/tbody/tr'
        desc_table = product.xpath(path)

        description = ""

        if len(desc_table) == 0:
            description = 'no description'
        else:
            desc1 = product.xpath(path + '/td/strong')
            desc2 = product.xpath(path + '/td')

            i = 0

            for d in desc1:
                if desc1[i].text == None:
                    description += ''
                else:
                    description += desc1[i].text
                description += '\t'
                if desc2[2 * i + 1].text == None:
                    description += ''
                else:
                    description += desc2[2 * i + 1].text
                description += ';\n'
                i += 1

        decs_xml = ET.SubElement(prod_xml, 'description')
        decs_xml.text = description

    tree = ET.ElementTree(root)
    tree.write("task3.xml", pretty_print=True, encoding="UTF-8")



def task4():
    tree = ET.parse("task3.xml")
    xslt_root = ET.XML('''<?xml version="1.0" encoding="WINDOWS-1251"?>
    <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:template match="/">
            <html xmlns="http://www.w3.org/1999/xhtml">
                <table border="1">
                    <xsl:for-each select="data/product">
                        <tr bgcolor="#F5F5F5">
                            <td>
                                <img>
                                    <xsl:attribute name="src">
                                        <xsl:value-of select="image"/>
                                    </xsl:attribute>
                                </img>
                            </td>
                            <td align="left">
                                <strong>
                                    <xsl:value-of select="title"/>
                                </strong>
                                <br />
                                <xsl:value-of select="description"/>
                            </td>
                            <td>
                                <xsl:value-of select="price"/>
                            </td>
                        </tr>
                    </xsl:for-each>
                </table>
            </html>
        </xsl:template>
    </xsl:stylesheet>''')

    transform = ET.XSLT(xslt_root)

    my_file = open("task4.xhtml", 'w')
    my_file.write(ET.tostring(transform(tree)))
    my_file.close()

task1()
task2()
task3()
task4()







