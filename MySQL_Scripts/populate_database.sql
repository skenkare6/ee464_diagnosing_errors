CREATE DATABASE IF NOT EXISTS TestingDatabase;
USE TestingDatabase;

CREATE TABLE IF NOT EXISTS `Repositories` (
  `repositoryID` int(11) NOT NULL AUTO_INCREMENT,
  `path` text NOT NULL,
  PRIMARY KEY (`repositoryID`)
);
CREATE TABLE IF NOT EXISTS `RFiles` (
  `fileID` int(11) NOT NULL AUTO_INCREMENT,
  `repositoryID` int(11) NOT NULL,
  `filePath` text NOT NULL,
  `fileType` int(11) NOT NULL,
  PRIMARY KEY (`fileID`),
  KEY `repositoryID` (`repositoryID`),
  CONSTRAINT `RFiles_ibfk_1` FOREIGN KEY (`repositoryID`) REFERENCES `Repositories` (`repositoryID`)
);
CREATE TABLE IF NOT EXISTS `RFunctions` (
  `functionID` int(11) NOT NULL AUTO_INCREMENT,
  `fileID` int(11) NOT NULL,
  `functionName` text NOT NULL,
  PRIMARY KEY (`functionID`),
  KEY `fileID` (`fileID`),
  CONSTRAINT `RFunctions_ibfk_1` FOREIGN KEY (`fileID`) REFERENCES `RFiles` (`fileID`)
);
CREATE TABLE IF NOT EXISTS `RTestCases` (
  `testCaseID` int(11) NOT NULL AUTO_INCREMENT,
  `fileID` int(11) NOT NULL,
  `testCaseName` text NOT NULL,
  PRIMARY KEY (`testCaseID`),
  KEY `fileID` (`fileID`),
  CONSTRAINT `RTestCases_ibfk_1` FOREIGN KEY (`fileID`) REFERENCES `RFiles` (`fileID`)
);
CREATE TABLE IF NOT EXISTS `RCodeToTestCases` (
  `linkID` int(11) NOT NULL AUTO_INCREMENT,
  `functionID` int(11) NOT NULL,
  `testCaseID` int(11) NOT NULL,
  PRIMARY KEY (`linkID`),
  KEY `functionID` (`functionID`),
  KEY `testCaseID` (`testCaseID`),
  CONSTRAINT `RCodeToTestCases_ibfk_1` FOREIGN KEY (`functionID`) REFERENCES `RFunctions` (`functionID`),
  CONSTRAINT `RCodeToTestCases_ibfk_2` FOREIGN KEY (`testCaseID`) REFERENCES `RTestCases` (`testCaseID`)
);

