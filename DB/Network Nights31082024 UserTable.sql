USE NetworkNights

CREATE TABLE Users.USERS
(
    UserID INT IDENTITY(1,1) PRIMARY KEY  ,
    FullName VARCHAR(70),
    UserName VARCHAR(70) UNIQUE NOT NULL ,
    Email VARCHAR(50) UNIQUE NOT NULL ,
    UserPassword VARCHAR(60) NOT NULL,
    UserRole BIT DEFAULT 0 ,  -- BIT column for role (0 = user, 1 = admin)
    CreatedDate DATETIME2 DEFAULT GETDATE() ,
    EmailVerified BIT DEFAULT 0  ,  -- 0 means not verified, 1 means verified
    UpdatedDate DATETIME DEFAULT GETDATE() ,
    IsActive BIT DEFAULT 0 ,
    CanLogin BIT DEFAULT 1 
);

-- Table Password reset
CREATE TABLE Users.PasswordResets(
ResetID Int identity(1,1) primary key,
UserID INT CONSTRAINT FK_USERS_UserID foreign key references users.users(UserID) on DELETE CASCADE, -- USERTABLE IF ANY ROW DELETE IT WILL AUTOMATICALYY DELETE FROM HERE 
ResetToken varchar(70) NOT NULL,
CreadtedDate Datetime Default GetDate(),
expireDate DateTime Not NUll
);


-- LOGIN ATTEMPTS
CREATE TABLE Users.LoginAttempts(

AttemptID Int Identity(1,1) primary key,
UserID Int Constraint FK_USERS_USERID_loginattempts FOREIGN KEY REFERENCES USERS.USERS(UserID) ON DELETE CASCADE,
AttemptTime DateTime Default Getdate(),
Succesfull Bit NOT NULL,
IpAddress Varchar(20)
);

-- SESSIONS
CREATE TABLE users.UserSession (
SessionID int identity(1,1) primary key,
UserID int Constraint FK_USER_USERID_UserSession foreign key references Users.Users(UserId) on Delete Cascade,
SessionToken varchar(255) Unique NOT NULL,
createdDate Datetime Default GetDate(),
ExpireDate datetime Not NUll,
IpAddress varchar(45),
UserAgent Text Not NULL
)





