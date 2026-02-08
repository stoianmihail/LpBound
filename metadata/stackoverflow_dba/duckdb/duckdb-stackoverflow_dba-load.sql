COPY badges FROM '../../LpBound/data/datasets/stackoverflow_dba/Badges.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY comments FROM '../../LpBound/data/datasets/stackoverflow_dba/Comments.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY users FROM '../../LpBound/data/datasets/stackoverflow_dba/Users.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY tags FROM '../../LpBound/data/datasets/stackoverflow_dba/Tags.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY posts FROM '../../LpBound/data/datasets/stackoverflow_dba/Posts.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY votes FROM '../../LpBound/data/datasets/stackoverflow_dba/Votes.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY posthistory FROM '../../LpBound/data/datasets/stackoverflow_dba/PostHistory.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY postlinks FROM '../../LpBound/data/datasets/stackoverflow_dba/PostLinks.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');