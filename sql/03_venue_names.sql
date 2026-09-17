    DROP VIEW IF EXISTS v_matches_venue;
CREATE VIEW v_matches_venue AS 
SELECT *,
        REPLACE(
            TRIM(
              SUBSTR(venue,1,
                CASE WHEN INSTR(venue,',') > 0
                     THEN INSTR(VENUE,',') - 1
                     ELSE LENGTH(VENUE)
                END)),
            'M.Chinnaswamy','M Chinnaswamy') AS venue_clean
FROM matches;                
