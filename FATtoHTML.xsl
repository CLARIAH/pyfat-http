<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    xmlns:trix="http://www.w3.org/2004/03/trix/trix-1/"
    exclude-result-prefixes="xs math trix"
    version="3.0">
    
    <xsl:output method="html"/>
    
    <xsl:template match="text()"/>
    
    <xsl:variable name="t" select="/"/>
    <xsl:key name="t-subject" match="trix:triple" use="trix:uri[1]"/>
    <xsl:key name="t-predicate" match="trix:triple" use="trix:uri[2]"/>
    <xsl:key name="t-object" match="trix:triple" use="trix:uri[3]"/>
    
    <xsl:variable name="p-rdf-type" select="'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'"/>
    <xsl:variable name="c-fair-rubric" select="'http://www.clarin.eu/ns/rubric#AssessmentRubricResultSet'"/>
    <xsl:variable name="p-fair-completion" select="'https://w3id.org/fair_test_result#completion'"/>
    <xsl:variable name="p-prov-used" select="'http://www.w3.org/ns/prov#used'"/>
    <xsl:variable name="p-schema-url" select="'https://schema.org/url'"/>
    <xsl:variable name="p-prov-hadMember" select="'http://www.w3.org/ns/prov#hadMember'"/>
    <xsl:variable name="p-schema-identifier" select="'https://schema.org/identifier'"/>
    <xsl:variable name="p-schema-name" select="'https://schema.org/name'"/>
    <xsl:variable name="p-fair-status" select="'https://w3id.org/fair_test_result#status'"/>
    <xsl:variable name="p-fair-log" select="'https://w3id.org/fair_test_result#log'"/>
    
    <xsl:function name="trix:get-instance">
        <xsl:param name="class"/>
        <xsl:sequence select="key('t-object',$class,$t)[trix:uri[2]=$p-rdf-type]/trix:uri[1]"/>
    </xsl:function>
    
    <xsl:function name="trix:subject">
        <xsl:param name="subj"/>
        <xsl:sequence select="key('t-subject',$subj,$t)"/>
    </xsl:function>

    <xsl:function name="trix:get-property">
        <xsl:param name="subj"/>
        <xsl:param name="prop"/>
        <xsl:sequence select="key('t-subject',$subj,$t)[trix:uri[2]=$prop]/trix:*[3]"/>
    </xsl:function>

    <xsl:template match="trix:graph">
        <xsl:variable name="report" select="trix:get-instance($c-fair-rubric)"/>
        <xsl:variable name="assessed" select="replace(trix:get-property(trix:get-property($report,$p-prov-used),$p-schema-url),'^.*/(.*).xml','$1')"/>
        <html xsl:expand-text="yes">
            <head>
                <title>FAIR assessment report for [{$assessed}]</title>
            </head>
            <body>
                <h1>FAIR assessment report for [{$assessed}]</h1>
                <p>Score is <b>{trix:get-property($report,$p-fair-completion)}</b>, based on <i>{if (trix:get-property($report,$p-fair-log)='Test modality = all') then ('all') else ('any')}</i></p>
                <dl>
                    <xsl:for-each select="trix:get-property($report,$p-prov-hadMember)">
                        <dt>{trix:get-property(current(),$p-schema-identifier)}: {trix:get-property(current(),$p-schema-name)}</dt>
                        <dd>
                            <p>Score is <b>{trix:get-property(current(),$p-fair-completion)}</b>, based on <i>{if (trix:get-property(current(),$p-fair-log)='Test modality = all') then ('all') else ('any')}</i></p>
                            <dl>
                                <xsl:for-each select="trix:get-property(current(),$p-prov-hadMember)">
                                    <dt>{trix:get-property(current(),$p-schema-identifier)}: {trix:get-property(current(),$p-schema-name)}</dt>
                                    <dd>
                                        <p>Status is <b>{trix:get-property(current(),$p-fair-status)}</b></p>
                                    </dd>
                                </xsl:for-each>
                            </dl>
                        </dd>
                    </xsl:for-each>
                </dl>
            </body>
        </html>
    </xsl:template>
    
    
    
</xsl:stylesheet>