-- Users
CREATE TABLE users (
  Id INTEGER NOT NULL PRIMARY KEY,
  Reputation INTEGER NOT NULL,
  CreationDate TIMESTAMP NOT NULL,
  DisplayName VARCHAR(100),
  LastAccessDate TIMESTAMP NOT NULL,
  WebsiteUrl VARCHAR(200),
  Location VARCHAR(300),
  AboutMe TEXT,
  Views INTEGER,
  UpVotes INTEGER,
  DownVotes INTEGER,
  ProfileImageUrl VARCHAR(200),
  AccountId BIGINT
);

-- Posts
CREATE TABLE posts (
  Id INTEGER NOT NULL PRIMARY KEY,
  PostTypeId SMALLINT,
  AcceptedAnswerId INTEGER,
  ParentId INTEGER,
  CreationDate TIMESTAMP,
  Score INTEGER,
  ViewCount INTEGER,
  Body TEXT,
  OwnerUserId INTEGER,
  OwnerDisplayName VARCHAR(100),
  LastEditorUserId INTEGER,
  LastEditorDisplayName VARCHAR(100),
  LastEditDate TIMESTAMP,
  LastActivityDate TIMESTAMP,
  Title VARCHAR(300),
  Tags VARCHAR(4000),
  AnswerCount INTEGER,
  CommentCount INTEGER,
  FavoriteCount INTEGER,
  ClosedDate TIMESTAMP,
  CommunityOwnedDate TIMESTAMP,
  ContentLicense VARCHAR(30)
);

-- PostLinks
CREATE TABLE postLinks (
  Id BIGINT NOT NULL PRIMARY KEY,
  CreationDate TIMESTAMP NOT NULL,
  PostId INTEGER NOT NULL,
  RelatedPostId INTEGER NOT NULL,
  LinkTypeId SMALLINT NOT NULL
);

-- PostHistory
CREATE TABLE postHistory (
  Id INTEGER NOT NULL PRIMARY KEY,
  PostHistoryTypeId SMALLINT,
  PostId INTEGER,
  RevisionGUID VARCHAR(36),
  CreationDate TIMESTAMP,
  UserId INTEGER,
  UserDisplayName VARCHAR(100),
  Comment VARCHAR(800),
  Text TEXT,
  ContentLicense VARCHAR(30)
);

-- Comments
CREATE TABLE comments (
  Id INTEGER NOT NULL PRIMARY KEY,
  PostId INTEGER NOT NULL,
  Score INTEGER,
  Text VARCHAR(2000) NOT NULL,
  CreationDate TIMESTAMP NOT NULL,
  UserDisplayName VARCHAR(100),
  UserId INTEGER,
  ContentLicense VARCHAR(30)
);

-- Votes
CREATE TABLE votes (
  Id INTEGER NOT NULL PRIMARY KEY,
  PostId INTEGER NOT NULL,
  VoteTypeId SMALLINT NOT NULL,
  UserId INTEGER,
  CreationDate TIMESTAMP,
  BountyAmount INTEGER
);

-- Badges
CREATE TABLE badges (
  Id INTEGER NOT NULL PRIMARY KEY,
  UserId INTEGER NOT NULL,
  Name VARCHAR(50) NOT NULL,
  Date TIMESTAMP NOT NULL,
  Class SMALLINT NOT NULL,
  TagBased BOOL NOT NULL
);

-- Tags
CREATE TABLE tags (
  Id INTEGER NOT NULL PRIMARY KEY,
  TagName VARCHAR(35),
  Count INTEGER NOT NULL,
  ExcerptPostId INTEGER,
  WikiPostId INTEGER,
  IsModeratorOnly BOOL,
  IsRequired BOOL
);