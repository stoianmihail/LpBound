COPY posthistory FROM '../../LpBound/data/datasets/math/PostHistory.csv'
(
  DELIMITER ',',
  QUOTE '"',
  ESCAPE '"',
  NULL '',
  HEADER FALSE,
  STRICT_MODE FALSE,
  PARALLEL FALSE,
  MAX_LINE_SIZE 10000000
);

COPY badges FROM '../../LpBound/data/datasets/math/Badges.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY comments FROM '../../LpBound/data/datasets/math/Comments.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY users FROM '../../LpBound/data/datasets/math/Users.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY tags FROM '../../LpBound/data/datasets/math/Tags.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY posts FROM '../../LpBound/data/datasets/math/Posts.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY votes FROM '../../LpBound/data/datasets/math/Votes.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');
COPY postlinks FROM '../../LpBound/data/datasets/math/PostLinks.csv' (DELIMITER ',', NULL '', QUOTE '"', ESCAPE '"');