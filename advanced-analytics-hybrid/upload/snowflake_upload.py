import snowflake.connector as sf

# Variables - to be modified, where needed!
user = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'
account = 'YOUR_ACCOUNT'
warehouse='YOUR_WAREHOUSE'
database = 'YOUR_DB'
schema = 'ATOMIC'
staging_table = 'SAMPLE_EVENTS_STAGED'
target_table ='SAMPLE_EVENTS'
csv_file = './sample_events.csv'

# Connection details - to be modified, where needed!
conn=sf.connect(user=user, password=password, account=account)

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()

try:
        # creating schema
        sql = "USE DATABASE " + database
        execute_query(conn, sql)
        sql = "CREATE SCHEMA IF NOT EXISTS " + schema
        execute_query(conn, sql)
        print('Schema created')

        # creating staging table
        execute_query(conn, sql)
        sql = "CREATE OR REPLACE TABLE " + database + "." + schema + "." + staging_table + """ (
                        APP_ID VARCHAR(255),
                        PLATFORM VARCHAR(255),
                        ETL_TSTAMP TIMESTAMP_NTZ(9),
                        COLLECTOR_TSTAMP TIMESTAMP_NTZ(9) NOT NULL,
                        DVCE_CREATED_TSTAMP TIMESTAMP_NTZ(9),
                        EVENT VARCHAR(128),
                        EVENT_ID VARCHAR(36) NOT NULL,
                        TXN_ID NUMBER(38,0),
                        NAME_TRACKER VARCHAR(128),
                        V_TRACKER VARCHAR(100),
                        V_COLLECTOR VARCHAR(100) NOT NULL,
                        V_ETL VARCHAR(100) NOT NULL,
                        USER_ID VARCHAR(255),
                        USER_IPADDRESS VARCHAR(128),
                        USER_FINGERPRINT VARCHAR(128),
                        DOMAIN_USERID VARCHAR(128),
                        DOMAIN_SESSIONIDX NUMBER(38,0),
                        NETWORK_USERID VARCHAR(128),
                        GEO_COUNTRY VARCHAR(2),
                        GEO_REGION VARCHAR(3),
                        GEO_CITY VARCHAR(75),
                        GEO_ZIPCODE VARCHAR(15),
                        GEO_LATITUDE FLOAT,
                        GEO_LONGITUDE FLOAT,
                        GEO_REGION_NAME VARCHAR(100),
                        IP_ISP VARCHAR(100),
                        IP_ORGANIZATION VARCHAR(128),
                        IP_DOMAIN VARCHAR(128),
                        IP_NETSPEED VARCHAR(100),
                        PAGE_URL VARCHAR(4096),
                        PAGE_TITLE VARCHAR(2000),
                        PAGE_REFERRER VARCHAR(4096),
                        PAGE_URLSCHEME VARCHAR(16),
                        PAGE_URLHOST VARCHAR(255),
                        PAGE_URLPORT NUMBER(38,0),
                        PAGE_URLPATH VARCHAR(3000),
                        PAGE_URLQUERY VARCHAR(6000),
                        PAGE_URLFRAGMENT VARCHAR(3000),
                        REFR_URLSCHEME VARCHAR(16),
                        REFR_URLHOST VARCHAR(255),
                        REFR_URLPORT NUMBER(38,0),
                        REFR_URLPATH VARCHAR(6000),
                        REFR_URLQUERY VARCHAR(6000),
                        REFR_URLFRAGMENT VARCHAR(3000),
                        REFR_MEDIUM VARCHAR(25),
                        REFR_SOURCE VARCHAR(50),
                        REFR_TERM VARCHAR(255),
                        MKT_MEDIUM VARCHAR(255),
                        MKT_SOURCE VARCHAR(255),
                        MKT_TERM VARCHAR(255),
                        MKT_CONTENT VARCHAR(500),
                        MKT_CAMPAIGN VARCHAR(255),
                        SE_CATEGORY VARCHAR(1000),
                        SE_ACTION VARCHAR(1000),
                        SE_LABEL VARCHAR(4096),
                        SE_PROPERTY VARCHAR(1000),
                        SE_VALUE FLOAT,
                        TR_ORDERID VARCHAR(255),
                        TR_AFFILIATION VARCHAR(255),
                        TR_TOTAL NUMBER(18,2),
                        TR_TAX NUMBER(18,2),
                        TR_SHIPPING NUMBER(18,2),
                        TR_CITY VARCHAR(255),
                        TR_STATE VARCHAR(255),
                        TR_COUNTRY VARCHAR(255),
                        TI_ORDERID VARCHAR(255),
                        TI_SKU VARCHAR(255),
                        TI_NAME VARCHAR(255),
                        TI_CATEGORY VARCHAR(255),
                        TI_PRICE NUMBER(18,2),
                        TI_QUANTITY NUMBER(38,0),
                        PP_XOFFSET_MIN NUMBER(38,0),
                        PP_XOFFSET_MAX NUMBER(38,0),
                        PP_YOFFSET_MIN NUMBER(38,0),
                        PP_YOFFSET_MAX NUMBER(38,0),
                        USERAGENT VARCHAR(1000),
                        BR_NAME VARCHAR(50),
                        BR_FAMILY VARCHAR(50),
                        BR_VERSION VARCHAR(50),
                        BR_TYPE VARCHAR(50),
                        BR_RENDERENGINE VARCHAR(50),
                        BR_LANG VARCHAR(255),
                        BR_FEATURES_PDF BOOLEAN,
                        BR_FEATURES_FLASH BOOLEAN,
                        BR_FEATURES_JAVA BOOLEAN,
                        BR_FEATURES_DIRECTOR BOOLEAN,
                        BR_FEATURES_QUICKTIME BOOLEAN,
                        BR_FEATURES_REALPLAYER BOOLEAN,
                        BR_FEATURES_WINDOWSMEDIA BOOLEAN,
                        BR_FEATURES_GEARS BOOLEAN,
                        BR_FEATURES_SILVERLIGHT BOOLEAN,
                        BR_COOKIES BOOLEAN,
                        BR_COLORDEPTH VARCHAR(12),
                        BR_VIEWWIDTH NUMBER(38,0),
                        BR_VIEWHEIGHT NUMBER(38,0),
                        OS_NAME VARCHAR(50),
                        OS_FAMILY VARCHAR(50),
                        OS_MANUFACTURER VARCHAR(50),
                        OS_TIMEZONE VARCHAR(255),
                        DVCE_TYPE VARCHAR(50),
                        DVCE_ISMOBILE BOOLEAN,
                        DVCE_SCREENWIDTH NUMBER(38,0),
                        DVCE_SCREENHEIGHT NUMBER(38,0),
                        DOC_CHARSET VARCHAR(128),
                        DOC_WIDTH NUMBER(38,0),
                        DOC_HEIGHT NUMBER(38,0),
                        TR_CURRENCY VARCHAR(3),
                        TR_TOTAL_BASE NUMBER(18,2),
                        TR_TAX_BASE NUMBER(18,2),
                        TR_SHIPPING_BASE NUMBER(18,2),
                        TI_CURRENCY VARCHAR(3),
                        TI_PRICE_BASE NUMBER(18,2),
                        BASE_CURRENCY VARCHAR(3),
                        GEO_TIMEZONE VARCHAR(64),
                        MKT_CLICKID VARCHAR(128),
                        MKT_NETWORK VARCHAR(64),
                        ETL_TAGS VARCHAR(500),
                        DVCE_SENT_TSTAMP TIMESTAMP_NTZ(9),
                        REFR_DOMAIN_USERID VARCHAR(128),
                        REFR_DVCE_TSTAMP TIMESTAMP_NTZ(9),
                        DOMAIN_SESSIONID VARCHAR(128),
                        DERIVED_TSTAMP TIMESTAMP_NTZ(9),
                        EVENT_VENDOR VARCHAR(1000),
                        EVENT_NAME VARCHAR(1000),
                        EVENT_FORMAT VARCHAR(128),
                        EVENT_VERSION VARCHAR(128),
                        EVENT_FINGERPRINT VARCHAR(128),
                        TRUE_TSTAMP TIMESTAMP_NTZ(9),
                        LOAD_TSTAMP TIMESTAMP_NTZ(9),
                        CONTEXTS_COM_SNOWPLOWANALYTICS_MOBILE_SCREEN_1 VARCHAR,
                        CONTEXTS_COM_SNOWPLOWANALYTICS_SNOWPLOW_CLIENT_SESSION_1 VARCHAR,
                        CONTEXTS_COM_SNOWPLOWANALYTICS_SNOWPLOW_GEOLOCATION_CONTEXT_1 VARCHAR,
                        CONTEXTS_COM_SNOWPLOWANALYTICS_SNOWPLOW_MOBILE_CONTEXT_1 VARCHAR,
                        CONTEXTS_COM_SNOWPLOWANALYTICS_MOBILE_APPLICATION_1 VARCHAR,
                        UNSTRUCT_EVENT_COM_SNOWPLOWANALYTICS_MOBILE_SCREEN_VIEW_1 VARCHAR,
                        constraint EVENT_ID_PK primary key (EVENT_ID)
                    );"""
        execute_query(conn, sql)
        print('Staging table '+ database + "." + schema + "." + staging_table +' is created')

        # staging
        sql = "USE SCHEMA " + schema
        execute_query(conn, sql)
        sql = 'DROP STAGE IF EXISTS DATA_STAGE'
        execute_query(conn, sql)
        print('Stage dropped, if applicable')

        sql = 'CREATE STAGE DATA_STAGE FILE_FORMAT = (TYPE = "CSV" FIELD_DELIMITER = "," SKIP_HEADER = 1)'
        execute_query(conn, sql)
        print('Stage created')

        # uploading
        sql = "PUT file://" + csv_file + " @DATA_STAGE AUTO_COMPRESS=true"
        execute_query(conn, sql)
        print('File put to stage')

        sql = "USE WAREHOUSE " + warehouse
        execute_query(conn, sql)
        sql = "COPY INTO " + database + "." + schema + "." + staging_table + " FROM @DATA_STAGE/sample_events.csv.gz FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '\"' ) ON_ERROR = 'ABORT_STATEMENT' "
        execute_query(conn, sql)
        print('Data loaded into staging table')

        # create target table
        sql = 'CREATE OR REPLACE TABLE ' + database + '.' + schema + "." + target_table + """ AS (
                    SELECT
                        APP_ID,
                        PLATFORM,
                        ETL_TSTAMP,
                        COLLECTOR_TSTAMP,
                        DVCE_CREATED_TSTAMP,
                        EVENT,
                        EVENT_ID,
                        TXN_ID,
                        NAME_TRACKER,
                        V_TRACKER,
                        V_COLLECTOR,
                        V_ETL,
                        USER_ID,
                        USER_IPADDRESS,
                        USER_FINGERPRINT,
                        DOMAIN_USERID,
                        DOMAIN_SESSIONIDX,
                        NETWORK_USERID,
                        GEO_COUNTRY,
                        GEO_REGION,
                        GEO_CITY,
                        GEO_ZIPCODE,
                        GEO_LATITUDE,
                        GEO_LONGITUDE,
                        GEO_REGION_NAME,
                        IP_ISP,
                        IP_ORGANIZATION,
                        IP_DOMAIN,
                        IP_NETSPEED,
                        PAGE_URL,
                        PAGE_TITLE,
                        PAGE_REFERRER,
                        PAGE_URLSCHEME,
                        PAGE_URLHOST,
                        PAGE_URLPORT,
                        PAGE_URLPATH,
                        PAGE_URLQUERY,
                        PAGE_URLFRAGMENT,
                        REFR_URLSCHEME,
                        REFR_URLHOST,
                        REFR_URLPORT,
                        REFR_URLPATH,
                        REFR_URLQUERY,
                        REFR_URLFRAGMENT,
                        REFR_MEDIUM,
                        REFR_SOURCE,
                        REFR_TERM,
                        MKT_MEDIUM,
                        MKT_SOURCE,
                        MKT_TERM,
                        MKT_CONTENT,
                        MKT_CAMPAIGN,
                        SE_CATEGORY,
                        SE_ACTION,
                        SE_LABEL,
                        SE_PROPERTY,
                        SE_VALUE,
                        TR_ORDERID,
                        TR_AFFILIATION,
                        TR_TOTAL,
                        TR_TAX,
                        TR_SHIPPING,
                        TR_CITY,
                        TR_STATE,
                        TR_COUNTRY,
                        TI_ORDERID,
                        TI_SKU,
                        TI_NAME,
                        TI_CATEGORY,
                        TI_PRICE,
                        TI_QUANTITY,
                        PP_XOFFSET_MIN,
                        PP_XOFFSET_MAX,
                        PP_YOFFSET_MIN,
                        PP_YOFFSET_MAX,
                        REPLACE(USERAGENT, '\"', '') as USERAGENT,
                        BR_NAME,
                        BR_FAMILY,
                        BR_VERSION,
                        BR_TYPE,
                        BR_RENDERENGINE,
                        BR_LANG,
                        BR_FEATURES_PDF,
                        BR_FEATURES_FLASH,
                        BR_FEATURES_JAVA,
                        BR_FEATURES_DIRECTOR,
                        BR_FEATURES_QUICKTIME,
                        BR_FEATURES_REALPLAYER,
                        BR_FEATURES_WINDOWSMEDIA,
                        BR_FEATURES_GEARS,
                        BR_FEATURES_SILVERLIGHT,
                        BR_COOKIES,
                        BR_COLORDEPTH,
                        BR_VIEWWIDTH,
                        BR_VIEWHEIGHT,
                        OS_NAME,
                        OS_FAMILY,
                        OS_MANUFACTURER,
                        OS_TIMEZONE,
                        DVCE_TYPE,
                        DVCE_ISMOBILE,
                        DVCE_SCREENWIDTH,
                        DVCE_SCREENHEIGHT,
                        DOC_CHARSET,
                        DOC_WIDTH,
                        DOC_HEIGHT,
                        TR_CURRENCY,
                        TR_TOTAL_BASE,
                        TR_TAX_BASE,
                        TR_SHIPPING_BASE,
                        TI_CURRENCY,
                        TI_PRICE_BASE,
                        BASE_CURRENCY,
                        GEO_TIMEZONE,
                        MKT_CLICKID,
                        MKT_NETWORK,
                        ETL_TAGS,
                        DVCE_SENT_TSTAMP,
                        REFR_DOMAIN_USERID,
                        REFR_DVCE_TSTAMP,
                        DOMAIN_SESSIONID,
                        DERIVED_TSTAMP,
                        EVENT_VENDOR,
                        EVENT_NAME,
                        EVENT_FORMAT,
                        EVENT_VERSION,
                        EVENT_FINGERPRINT,
                        TRUE_TSTAMP,
                        LOAD_TSTAMP,
                        PARSE_JSON(CONTEXTS_COM_SNOWPLOWANALYTICS_MOBILE_SCREEN_1) as CONTEXTS_COM_SNOWPLOWANALYTICS_MOBILE_SCREEN_1,
                        PARSE_JSON(CONTEXTS_COM_SNOWPLOWANALYTICS_SNOWPLOW_CLIENT_SESSION_1) as CONTEXTS_COM_SNOWPLOWANALYTICS_SNOWPLOW_CLIENT_SESSION_1,
                        PARSE_JSON(CONTEXTS_COM_SNOWPLOWANALYTICS_SNOWPLOW_GEOLOCATION_CONTEXT_1) as CONTEXTS_COM_SNOWPLOWANALYTICS_SNOWPLOW_GEOLOCATION_CONTEXT_1,
                        PARSE_JSON(CONTEXTS_COM_SNOWPLOWANALYTICS_SNOWPLOW_MOBILE_CONTEXT_1) as CONTEXTS_COM_SNOWPLOWANALYTICS_SNOWPLOW_MOBILE_CONTEXT_1,
                        PARSE_JSON(CONTEXTS_COM_SNOWPLOWANALYTICS_MOBILE_APPLICATION_1) as CONTEXTS_COM_SNOWPLOWANALYTICS_MOBILE_APPLICATION_1,
                        PARSE_JSON(UNSTRUCT_EVENT_COM_SNOWPLOWANALYTICS_MOBILE_SCREEN_VIEW_1) as UNSTRUCT_EVENT_COM_SNOWPLOWANALYTICS_MOBILE_SCREEN_VIEW_1

                    FROM """ + schema + "." + staging_table + ')'
        execute_query(conn, sql)
        print('Target table: ' + database + "." +  schema + "." + target_table + ' is created')

        # Drop the **SAMPLE_EVENTS_BASE** table
        sql = 'DROP TABLE ' + database + "." +  schema + "." + staging_table
        execute_query(conn, sql)
        print('Staging table: ' + database + "." +  schema + "." + staging_table + ' is dropped')

except Exception as e:
    print(e)

finally:
    conn.close()
