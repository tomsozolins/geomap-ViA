CREATE TABLE  "GEOMAP" 
   (	"ID" NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  NOT NULL ENABLE, 
	"HOST_TYPE" VARCHAR2(50), 
	"HOST_MODEL" VARCHAR2(50), 
	"HOSTID" NUMBER, 
	"VENDOR" VARCHAR2(50), 
	"LOCATION_LAT" NUMBER, 
	"LOCATION_LON" NUMBER, 
	"HOST_NAME" VARCHAR2(100), 
	 PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   )
/

CREATE TABLE  "GEOMAP_EVENTS" 
   (	"ID" NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  NOT NULL ENABLE, 
	"EVENT_TIMESTAMP" TIMESTAMP (6) WITH LOCAL TIME ZONE, 
	"USERNAME" VARCHAR2(50), 
	"EVENT_TYPE" VARCHAR2(50), 
	"EVENT_MESSAGE" VARCHAR2(50), 
	"HOSTID" NUMBER, 
	"LOCATION_LAT" NUMBER, 
	"LOCATION_LON" NUMBER, 
	 PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   )
/

CREATE OR REPLACE EDITIONABLE TRIGGER  "GEOMAP_T1_DELETE" 
AFTER
DELETE ON "GEOMAP"
FOR EACH ROW
BEGIN
INSERT INTO GEOMAP_EVENTS(EVENT_TIMESTAMP,USERNAME,EVENT_TYPE,EVENT_MESSAGE,HOSTID,LOCATION_LAT,LOCATION_LON)
VALUES(CURRENT_TIMESTAMP,V('APP_USER'),'DELETE','DELETED GEO POINT',:OLD.HOSTID,:OLD.LOCATION_LAT,:OLD.LOCATION_LON);
END;

/
ALTER TRIGGER  "GEOMAP_T1_DELETE" ENABLE
/

CREATE OR REPLACE EDITIONABLE TRIGGER  "GEOMAP_T2_INSERT" 
AFTER
INSERT ON "GEOMAP"
FOR EACH ROW
BEGIN
INSERT INTO GEOMAP_EVENTS(EVENT_TIMESTAMP,USERNAME,EVENT_TYPE,EVENT_MESSAGE,HOSTID,LOCATION_LAT,LOCATION_LON)
VALUES(CURRENT_TIMESTAMP, V('APP_USER'),'INSERT','CREATED GEO POINT',:NEW.HOSTID,:NEW.LOCATION_LAT,:NEW.LOCATION_LON);
END;

/
ALTER TRIGGER  "GEOMAP_T2_INSERT" ENABLE
/