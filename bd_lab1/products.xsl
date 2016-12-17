<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="xml" doctype-system
="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"
  doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" indent="yes" encoding="utf-8" />

<xsl:template match="/">
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/xhtml; charset=utf-8" />
            <title>Laba 1</title>
        </head>
        <body>
            <table>
                <tbody>
                    <xsl:for-each select="data/product">
                        <tr style="margin-bottom: 25px;">
                            <td style="border-bottom: 1px solid #ddd; padding: 15px;">
                                <img style="max-width: 250px"><xsl:attribute name="src"><xsl:value-of select='image' /></xsl:attribute></img>
                            </td>
                            <td style="border-bottom: 1px solid #ddd; padding: 15px;">
                                <h3><xsl:value-of select="title"/></h3>
                            </td>
                            <td style="border-bottom: 1px solid #ddd; padding: 15px;">
                                <span><xsl:value-of select="price"/></span>
                            </td>
                            <td style="border-bottom: 1px solid #ddd; padding: 15px;">
                                <p><xsl:value-of select="description"/></p>
                            </td>
                        </tr>
                    </xsl:for-each>
                </tbody>
            </table>
        </body>
    </html>
</xsl:template>

</xsl:stylesheet>