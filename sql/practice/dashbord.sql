-- ============================================================
-- TEAM B — BOWLERS DASHBOARD
-- ============================================================
--
-- The queries themselves are the ones used inside q() in app.py.
-- One query per box / visual on the approved dashboard.
--
-- Filters:
--   Season
--   Bowling Style
--   Minimum Balls
--   Team
--
-- ============================================================


-- ============================================================
-- CARD 1: TOTAL BOWLERS
-- ============================================================
--
-- Number of unique bowlers after applying the dashboard filters.
--

SELECT
    COUNT(DISTINCT bowler) AS total_bowlers

FROM v_ball

WHERE
    (? IS NULL OR season_id = ?)
    AND
    (? IS NULL OR bowling_team = ?);


-- ============================================================
-- CARD 2: QUALIFIED BOWLERS
-- ============================================================
--
-- Number of bowlers who have bowled at least the selected
-- minimum number of legal balls.
--

SELECT
    COUNT(*) AS qualified_bowlers

FROM
(
    SELECT
        bowler,
        SUM(is_legal) AS balls

    FROM v_ball

    WHERE
        (? IS NULL OR season_id = ?)
        AND
        (? IS NULL OR bowling_team = ?)

    GROUP BY
        bowler

    HAVING
        SUM(is_legal) >= ?
);


-- ============================================================
-- CARD 3: TOTAL WICKETS
-- ============================================================
--
-- Total wickets credited to bowlers after applying filters.
--

SELECT
    SUM(bowler_wicket) AS total_wickets

FROM v_ball

WHERE
    (? IS NULL OR season_id = ?)
    AND
    (? IS NULL OR bowling_team = ?);


-- ============================================================
-- VISUAL 1: ECONOMY BY INNINGS PHASE
-- ============================================================
--
-- Compares Spin and Pace economy across:
--
--   Powerplay
--   Middle Overs
--   Death Overs
--
-- This is the main / hero visual.
--

SELECT

    CASE
        WHEN phase = 'Powerplay'
            THEN 'Powerplay (1-6)'

        WHEN phase = 'Middle'
            THEN 'Middle Overs (7-15)'

        WHEN phase = 'Death'
            THEN 'Death Overs (16-20)'

        ELSE phase
    END AS phase,

    CASE
        WHEN bowler_type LIKE '%Legbreak%'
          OR bowler_type LIKE '%Offbreak%'
          OR bowler_type LIKE '%Orthodox%'
          OR bowler_type LIKE '%Googly%'
          OR bowler_type LIKE '%Wrist spin%'
            THEN 'Spin'

        ELSE 'Pace'
    END AS bowling_group,

    ROUND(
        6.0 * SUM(bowler_runs)
        / NULLIF(SUM(is_legal), 0),
        2
    ) AS economy,

    SUM(is_legal) AS balls

FROM v_ball

WHERE
    (? IS NULL OR season_id = ?)
    AND
    (? IS NULL OR bowling_team = ?)

GROUP BY
    phase,
    bowling_group

ORDER BY
    CASE phase
        WHEN 'Powerplay' THEN 1
        WHEN 'Middle' THEN 2
        WHEN 'Death' THEN 3
        ELSE 4
    END,
    bowling_group;


-- ============================================================
-- VISUAL 2: ECONOMY BY BOWLING STYLE
-- ============================================================
--
-- Economy rate for each bowling style.
--

SELECT

    CASE

        WHEN bowler_type LIKE '%Legbreak%'
          OR bowler_type LIKE '%Googly%'
          OR bowler_type LIKE '%Wrist spin%'
            THEN 'Leg spin'

        WHEN bowler_type LIKE '%Offbreak%'
            THEN 'Right-arm off spin'

        WHEN bowler_type LIKE '%Orthodox%'
            THEN 'Left-arm orthodox'

        WHEN bowler_type LIKE '%Left arm%'
         AND (
                bowler_type LIKE '%Fast%'
                OR bowler_type LIKE '%Medium%'
             )
            THEN 'Left-arm pace'

        WHEN bowler_type LIKE '%Right arm%'
         AND (
                bowler_type LIKE '%Fast%'
                OR bowler_type LIKE '%Medium%'
             )
            THEN 'Right-arm pace'

        ELSE 'Others'

    END AS bowling_style,

    ROUND(
        6.0 * SUM(bowler_runs)
        / NULLIF(SUM(is_legal), 0),
        2
    ) AS economy,

    COUNT(DISTINCT bowler) AS bowlers

FROM v_ball

WHERE
    (? IS NULL OR season_id = ?)
    AND
    (? IS NULL OR bowling_team = ?)

GROUP BY
    bowling_style

HAVING
    bowling_style <> 'Others'

ORDER BY
    economy;


-- ============================================================
-- VISUAL 3: WICKETS BY INNINGS PHASE
-- ============================================================
--
-- Total wickets taken in each innings phase.
--

SELECT

    CASE
        WHEN phase = 'Powerplay'
            THEN 'Powerplay (1-6)'

        WHEN phase = 'Middle'
            THEN 'Middle Overs (7-15)'

        WHEN phase = 'Death'
            THEN 'Death Overs (16-20)'

        ELSE phase
    END AS phase,

    SUM(bowler_wicket) AS wickets

FROM v_ball

WHERE
    (? IS NULL OR season_id = ?)
    AND
    (? IS NULL OR bowling_team = ?)

GROUP BY
    phase

ORDER BY

    CASE phase
        WHEN 'Powerplay' THEN 1
        WHEN 'Middle' THEN 2
        WHEN 'Death' THEN 3
        ELSE 4
    END;


-- ============================================================
-- VISUAL 4: DOT-BALL SHARE BY BOWLING STYLE
-- ============================================================
--
-- Percentage of legal deliveries that were dot balls.
--

SELECT

    CASE

        WHEN bowler_type LIKE '%Legbreak%'
          OR bowler_type LIKE '%Googly%'
          OR bowler_type LIKE '%Wrist spin%'
            THEN 'Leg spin'

        WHEN bowler_type LIKE '%Offbreak%'
            THEN 'Right-arm off spin'

        WHEN bowler_type LIKE '%Orthodox%'
            THEN 'Left-arm orthodox'

        WHEN bowler_type LIKE '%Left arm%'
         AND (
                bowler_type LIKE '%Fast%'
                OR bowler_type LIKE '%Medium%'
             )
            THEN 'Left-arm pace'

        WHEN bowler_type LIKE '%Right arm%'
         AND (
                bowler_type LIKE '%Fast%'
                OR bowler_type LIKE '%Medium%'
             )
            THEN 'Right-arm pace'

        ELSE 'Others'

    END AS bowling_style,

    COUNT(*) AS legal_balls,

    SUM(
        CASE
            WHEN bowler_runs = 0
                THEN 1
            ELSE 0
        END
    ) AS dot_balls,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN bowler_runs = 0
                    THEN 1
                ELSE 0
            END
        )
        / NULLIF(SUM(is_legal), 0),
        1
    ) AS dot_ball_share

FROM v_ball

WHERE
    (? IS NULL OR season_id = ?)
    AND
    (? IS NULL OR bowling_team = ?)

GROUP BY
    bowling_style

HAVING
    bowling_style <> 'Others'

ORDER BY
    dot_ball_share DESC;


-- ============================================================
-- VISUAL 5: ECONOMY TREND BY SEASON
-- ============================================================
--
-- Shows how bowling economy changed from season to season.
--

SELECT

    season_id AS season,

    ROUND(
        6.0 * SUM(bowler_runs)
        / NULLIF(SUM(is_legal), 0),
        2
    ) AS economy,

    SUM(is_legal) AS balls,

    SUM(bowler_wicket) AS wickets

FROM v_ball

WHERE
    (? IS NULL OR bowling_team = ?)

GROUP BY
    season_id

ORDER BY
    season_id;


-- ============================================================
-- VISUAL 6: BOWLING STYLE DISTRIBUTION
-- ============================================================
--
-- Number of bowlers belonging to each bowling style.
--

SELECT

    CASE

        WHEN bowler_type LIKE '%Legbreak%'
          OR bowler_type LIKE '%Googly%'
          OR bowler_type LIKE '%Wrist spin%'
            THEN 'Leg spin'

        WHEN bowler_type LIKE '%Offbreak%'
            THEN 'Right-arm off spin'

        WHEN bowler_type LIKE '%Orthodox%'
            THEN 'Left-arm orthodox'

        WHEN bowler_type LIKE '%Left arm%'
         AND (
                bowler_type LIKE '%Fast%'
                OR bowler_type LIKE '%Medium%'
             )
            THEN 'Left-arm pace'

        WHEN bowler_type LIKE '%Right arm%'
         AND (
                bowler_type LIKE '%Fast%'
                OR bowler_type LIKE '%Medium%'
             )
            THEN 'Right-arm pace'

        ELSE 'Others'

    END AS bowling_style,

    COUNT(DISTINCT bowler) AS bowlers

FROM v_ball

WHERE
    (? IS NULL OR season_id = ?)
    AND
    (? IS NULL OR bowling_team = ?)

GROUP BY
    bowling_style

HAVING
    bowling_style <> 'Others'

ORDER BY
    bowlers DESC;


-- ============================================================
-- INDIVIDUAL BOWLER
-- ============================================================


-- ============================================================
-- CARD 4: SELECTED BOWLER — WICKETS
-- ============================================================

SELECT

    SUM(bowler_wicket) AS wickets

FROM v_ball

WHERE
    bowler = ?
    AND
    (? IS NULL OR season_id = ?);


-- ============================================================
-- CARD 5: SELECTED BOWLER — ECONOMY
-- ============================================================

SELECT

    ROUND(
        6.0 * SUM(bowler_runs)
        / NULLIF(SUM(is_legal), 0),
        2
    ) AS economy

FROM v_ball

WHERE
    bowler = ?
    AND
    (? IS NULL OR season_id = ?);


-- ============================================================
-- CARD 6: SELECTED BOWLER — DOT-BALL SHARE
-- ============================================================

SELECT

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN bowler_runs = 0
                    THEN 1
                ELSE 0
            END
        )
        / NULLIF(SUM(is_legal), 0),
        1
    ) AS dot_ball_share

FROM v_ball

WHERE
    bowler = ?
    AND
    (? IS NULL OR season_id = ?);


-- ============================================================
-- INDIVIDUAL VISUAL 1: ECONOMY BY SEASON
-- ============================================================

SELECT

    season_id AS season,

    ROUND(
        6.0 * SUM(bowler_runs)
        / NULLIF(SUM(is_legal), 0),
        2
    ) AS economy,

    SUM(bowler_wicket) AS wickets,

    SUM(is_legal) AS balls

FROM v_ball

WHERE
    bowler = ?

GROUP BY
    season_id

ORDER BY
    season_id;


-- ============================================================
-- INDIVIDUAL VISUAL 2: WICKETS & ECONOMY BY PHASE
-- ============================================================

SELECT

    CASE
        WHEN phase = 'Powerplay'
            THEN 'Powerplay (1-6)'

        WHEN phase = 'Middle'
            THEN 'Middle Overs (7-15)'

        WHEN phase = 'Death'
            THEN 'Death Overs (16-20)'

        ELSE phase
    END AS phase,

    SUM(bowler_wicket) AS wickets,

    ROUND(
        6.0 * SUM(bowler_runs)
        / NULLIF(SUM(is_legal), 0),
        2
    ) AS economy

FROM v_ball

WHERE
    bowler = ?

GROUP BY
    phase

ORDER BY

    CASE phase
        WHEN 'Powerplay' THEN 1
        WHEN 'Middle' THEN 2
        WHEN 'Death' THEN 3
        ELSE 4
    END;


-- ============================================================
-- INDIVIDUAL VISUAL 3: ECONOMY VS OPPONENT
-- ============================================================

SELECT

    batting_team AS opponent,

    ROUND(
        6.0 * SUM(bowler_runs)
        / NULLIF(SUM(is_legal), 0),
        2
    ) AS economy,

    SUM(bowler_wicket) AS wickets

FROM v_ball

WHERE
    bowler = ?

GROUP BY
    batting_team

HAVING
    SUM(is_legal) >= 12

ORDER BY
    economy

LIMIT 8;


-- ============================================================
-- INDIVIDUAL VISUAL 4: ECONOMY BY GROUND
-- ============================================================

SELECT

    m.venue_clean AS ground,

    ROUND(
        6.0 * SUM(v.bowler_runs)
        / NULLIF(SUM(v.is_legal), 0),
        2
    ) AS economy,

    SUM(v.bowler_wicket) AS wickets

FROM v_ball v

JOIN matches_clean m
    ON v.match_id = m.match_id

WHERE
    v.bowler = ?

GROUP BY
    m.venue_clean























































HAVING
    SUM(v.is_legal) >= 24

ORDER BY
    economy

LIMIT 5;


-- ============================================================
-- INDIVIDUAL VISUAL 5: DISMISSAL TYPES
-- ============================================================

SELECT

    wicket_kind AS dismissal_type,

    COUNT(*) AS dismissals

FROM v_ball

WHERE
    bowler = ?

    AND
    bowler_wicket = 1

GROUP BY
    wicket_kind

ORDER BY
    dismissals DESC;