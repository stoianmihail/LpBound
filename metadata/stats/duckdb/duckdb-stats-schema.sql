-- Users
CREATE TABLE users (
  Id INTEGER NOT NULL PRIMARY KEY,
  Reputation INTEGER ,
  CreationDate TIMESTAMP ,
  Views INTEGER ,
  UpVotes INTEGER ,
  DownVotes INTEGER
);

-- Posts
CREATE TABLE posts (
	Id INTEGER NOT NULL PRIMARY KEY,
	PostTypeId SMALLINT ,
	CreationDate TIMESTAMP ,
	Score INTEGER ,
	ViewCount INTEGER,
	OwnerUserId INTEGER,
  AnswerCount INTEGER ,
  CommentCount INTEGER ,
  FavoriteCount INTEGER,
  LastEditorUserId INTEGER
);

-- PostLinks
CREATE TABLE postLinks (
	Id INTEGER NOT NULL PRIMARY KEY,
	CreationDate TIMESTAMP ,
	PostId INTEGER ,
	RelatedPostId INTEGER ,
	LinkTypeId SMALLINT
);

-- PostHistory
CREATE TABLE postHistory (
	Id INTEGER NOT NULL PRIMARY KEY,
	PostHistoryTypeId SMALLINT ,
	PostId INTEGER ,
	CreationDate TIMESTAMP ,
	UserId INTEGER
);

-- Comments
CREATE TABLE comments (
	Id INTEGER NOT NULL PRIMARY KEY,
	PostId INTEGER ,
	Score SMALLINT ,
  CreationDate TIMESTAMP ,
	UserId INTEGER
);

-- Votes
CREATE TABLE votes (
	Id INTEGER NOT NULL PRIMARY KEY,
	PostId INTEGER,
	VoteTypeId SMALLINT ,
	CreationDate TIMESTAMP ,
	UserId INTEGER,
	BountyAmount SMALLINT
);

-- Badges
CREATE TABLE badges (
	Id INTEGER NOT NULL PRIMARY KEY,
	UserId INTEGER ,
	Date TIMESTAMP
);

-- Tags
CREATE TABLE tags (
	Id INTEGER NOT NULL PRIMARY KEY,
	Count INTEGER ,
	ExcerptPostId INTEGER
);
