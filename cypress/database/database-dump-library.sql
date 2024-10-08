-- MariaDB dump 10.19-11.3.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: library
-- ------------------------------------------------------
-- Server version	11.3.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES
('a0cb5c19c077');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `article`
--

DROP TABLE IF EXISTS `article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `content` varchar(15000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `category` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `note` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `thumbnail` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article`
--

LOCK TABLES `article` WRITE;
/*!40000 ALTER TABLE `article` DISABLE KEYS */;
INSERT INTO `article` VALUES
(1,'Introduction to Meditation','- Tuesdays at 10 a.m.\r\n- Location: Regional Branch Library\r\n- Type: Online\r\n- Audience:Adults\r\n- Category: Health & Wellness\r\n- Language: English\r\n\r\nRSVP:\r\n\r\nPlease email abc@easylib.com for the Zoom meeting link.\r\nDescription:\r\n\r\nJoin us via Zoom to experience a variety of calming meditation techniques presented by instructor Staci Mintz.\r\n \r\n\r\nFor ADA accommodations, call (213) 228-7430 at least 72 hours prior to the event.\r\n\r\nPara ajustes razonables según la ley de ADA, llama al (213) 228-7430 al menos 72 horas antes del evento.\r\n','2024-07-16 11:23:24','Event','Tuesdays at 10 a.m. - Location: Regional Branch Library',NULL),
(2,'New UI','This is the new UI for EasyLib 1.0.1, with a more modern UI.\r\n\r\nHowever, one of the regressions is dark mode can no longer work well.','2024-08-20 14:45:23','Library Update',NULL,'https://easylib.jesse-tong.work/uploaded-image/10'),
(7,'Kaleidoscope Play & Learn @ Columbia Branch','![DgDmZqnI9BRWvNdBMGJ28LYN.jpg](https://easylib.jesse-tong.work/uploaded-image/9 \"DgDmZqnI9BRWvNdBMGJ28LYN.jpg\")\r\n\r\nChildren listen to multilingual stories, sing songs and do simple crafts with their caregivers during the group time.\r\n\r\nThis program will be co-facilitated in English and አማርኛ (Amharic).\r\n------------------------------------------------------------------------------------------------------\r\n\r\nበዚህ ጊዜ ልጆች በቡድን የተለያዩ ታሪኮችን ይሰማሉ፣ ሙዚቃ ይዘፍናሉ እንዲሁም ከቤተሰቦቻቸዉ ወይም ከአሳዳጊዎቻቸዉ ጋር ቀላል እደ-ጥበብ ወይም ስእል ይስላሉ።\r\n\r\nይህ ፕሮግራም በእንግሊዘኛ እና በአማርኛ በጋራ የሚዘጋጅ ይሆናል።\r\n\r\nለመሳተፍ ወይም ለመምጣት ምዝገባ አያስፈልግም።\r\n\r\nColumbia Branch\r\nRegistration is not required.\r\nabout-AM-EN\r\nKaleidoscope play and learn offers a chance for children and their families to come play and have a good time. \r\n\r\nThere is also a play time for children to explore various toys and play activities.\r\n\r\nChildren learn and explore the use of art, music, toys and more. Families learn about their child\'s development and community resources available to them.\r\n\r\nThanks to our partner Denise Louie Education Center.\r\n\r\n-----------------------------------------------------\r\n\r\nየካሊዶስኮፕ ጨዋታ እና ትምህርት ክፍለ ጊዜ ልጆች እና ቤተሰቦቻቸው መጥተዉ በቡድን\r\n\r\nእንዲጫወቱ እና ጥሩ ጊዜ እንዲያሳልፉ እድል ይሰጣል።\r\n\r\nበተጨማሪም ልጆች በተለያዩ አሻንጉሊቶች እና የጨዋታ አይነቶች የሚጫወቱበት ሰዓት ተካቷል።\r\n\r\nልጆች ጥበብን፣ ሙዚቃን፣ መጫወቻዎችን ወይም አሻንጉሊቶችን እና የመሳሰሉትን ጠቀሜታቸዉን ይማራሉ በተጨማሪም ይመራመራሉ። ቤተሰቦች ስለልጆቻቸው እድገት እና ለእነሱ ስላሉ የህዝብ ሀብቶች ይማራሉ ያዉቃሉ ።\r\n\r\nየዚህ ፕሮግራም አዘጋጅ  ባልደረባችን Denise Louie Education Center/ ዴኒዝ ሉዊ የትምህርት ማእከል/  እናመሰግናለን።\r\ninformation-AM-EN\r\nThis group is open to children of all abilities, ages 0 to 5 years old.\r\n\r\n-----------------------------------------------------\r\n\r\nይህ ፕሮግራም እድሜያቸው ከ0ወር እስከ 5 አመት ለሆኑ ህጻናት ለሁሉም ክፍት ነው።\r\ncontact-AM-EN\r\nIf you have questions about this event, Ask Us or call 206-386-4636.\r\n\r\n-----------------------------------------------------\r\n\r\nበፕሮግራሙ ላይ አስተያየቶች እና ጥያቄዎች ካሉዎት ይጠይቁን ወይም በስልክ ቁጥር  206-386-4636 ይደውሉልን።\r\naccessibility-AM-EN\r\nWe can provide accommodations for people with disabilities at Library events. Please contact LEAP at least seven days before the event to request accommodations.\r\n\r\n-----------------------------------------------------\r\n\r\nበቤተ መጽሐፍ ዝግጅቶች ላይ ለአካል ጉዳተኞች ማረፊያ ቦታ እንሰጣለን። እባክዎ ከፈለጉ ዝግጅቱ ከመድረሱ ከሰባት ቀናት በፊት   LEAPን ያግኙ ። በስልክ ቁጥር  206-615-1380 ወይም በኢሜይል leap@spl.org ማግኘት ይችላሉ።','2024-08-25 20:07:43','Event','Monday, August 26, 2024, 10:30 a.m. – 12 p.m.','https://easylib.jesse-tong.work/uploaded-image/9'),
(8,'Back to School 2024 with NYPL','Getting ready to head back to school? The Library can help you brush up on your skills, prepare for college or a career, find new books to read, and more. Plus, don’t miss our many resources for educators from NYPL’s Center for Educators and Schools.\r\n\r\nJump to resources for:\r\n\r\nKids\r\nTeens\r\nBabies & Toddlers\r\nAdults\r\nEducators\r\n','2024-08-28 22:17:44','Event','','');
/*!40000 ALTER TABLE `article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `place` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `author`
--

LOCK TABLES `author` WRITE;
/*!40000 ALTER TABLE `author` DISABLE KEYS */;
INSERT INTO `author` VALUES
(1,'Miguel de Cervantes',NULL),
(2,'Mary Shelley',NULL),
(5,'Dustin Stevens',NULL),
(52,'Sarah J. Maas',NULL),
(54,'Test author',NULL);
/*!40000 ALTER TABLE `author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stock` int(11) DEFAULT NULL,
  `title` varchar(300) DEFAULT NULL,
  `publish_year` int(11) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `isbn` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES
(1,4,'Don Quixote',1605,'Don Quixote, novel published in two parts (part 1, 1605, and part 2, 1615) by Spanish writer Miguel de Cervantes, one of the most widely read classics of Western literature. Originally conceived as a parody of the chivalric romances that had long been in literary vogue, it describes realistically what befalls an aging knight who, his head bemused by reading such romances, sets out on his old horse Rocinante, with his pragmatic squire, Sancho Panza, to seek adventure. Widely and immediately translated (first English translation 1612), the novel was a great and continuing success and is considered a prototype of the modern novel. ','1716619041010'),
(4,0,'Frankenstein',1818,'Shelley\'s novel, Frankenstein: or, the Modern Prometheus (1818), is a combination of Gothic horror story and science fiction. \r\nThe book tells the story of Victor Frankenstein, a Swiss student of natural science who creates an artificial man from pieces of corpses and brings his creature to life.','13, 978-0486282114'),
(15,0,'Frankenstein',1818,'Shelley\'s novel, Frankenstein: or, the Modern Prometheus (1818), is a combination of Gothic horror story and science fiction. \r\nThe book tells the story of Victor Frankenstein, a Swiss student of natural science who creates an artificial man from pieces of corpses and brings his creature to life.','13-0486282114'),
(17,4,'A Court of Thorns and Roses',2015,' The sexy, action-packed first book in the #1 New York Times bestselling Court of Thorns and Roses series from Sarah J. Maas.\r\n\r\nWhen nineteen-year-old huntress Feyre kills a wolf in the woods, a terrifying creature arrives to demand retribution. Dragged to a treacherous magical land she knows about only from legends, Feyre discovers that her captor is not truly a beast, but one of the lethal, immortal faeries who once ruled her world.\r\n','1526605392'),
(20,0,'Cold Fire',2015,'As a DEA agent, Jeremiah “Hawk” Tate was one of the best at taking down drug traffickers. Then the cartels struck back—and destroyed everything he held dear.\r\n\r\nFive years later, Hawk has retreated from society and is living a quiet life as a Montana wilderness guide. He’s done with the DEA, done with the criminals, and done with the pain left over from his past. But his past isn’t done with him.',' ‎B00QKUW8UO'),
(24,0,'Cold Fire',2015,'','1222131414141'),
(61,99990,'Test book 2',2024,'Test description','1111111111111'),
(74,0,'Test book 1',2024,'Test description','1111111'),
(96,1,'Test book 11',2021,NULL,'TESTbook11');
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookauthor`
--

DROP TABLE IF EXISTS `bookauthor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bookauthor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookId` int(11) DEFAULT NULL,
  `authorId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bookId` (`bookId`),
  KEY `authorId` (`authorId`),
  CONSTRAINT `bookauthor_ibfk_1` FOREIGN KEY (`bookId`) REFERENCES `book` (`id`),
  CONSTRAINT `bookauthor_ibfk_2` FOREIGN KEY (`authorId`) REFERENCES `author` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookauthor`
--

LOCK TABLES `bookauthor` WRITE;
/*!40000 ALTER TABLE `bookauthor` DISABLE KEYS */;
INSERT INTO `bookauthor` VALUES
(49,24,5),
(100,17,52),
(103,74,54),
(108,4,2),
(150,96,54),
(153,1,1);
/*!40000 ALTER TABLE `bookauthor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookborrow`
--

DROP TABLE IF EXISTS `bookborrow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bookborrow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookId` int(11) DEFAULT NULL,
  `userId` int(11) DEFAULT NULL,
  `startBorrow` datetime DEFAULT NULL,
  `endBorrow` datetime DEFAULT NULL,
  `hasReturned` tinyint(1) DEFAULT NULL,
  `returnDate` datetime DEFAULT NULL,
  `isDamagedOrLost` tinyint(1) DEFAULT NULL,
  `isApproved` tinyint(1) DEFAULT NULL,
  `hasResolved` tinyint(1) DEFAULT NULL,
  `renewPending` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `bookId` (`bookId`),
  KEY `userId` (`userId`),
  CONSTRAINT `bookborrow_ibfk_1` FOREIGN KEY (`bookId`) REFERENCES `book` (`id`),
  CONSTRAINT `bookborrow_ibfk_2` FOREIGN KEY (`userId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookborrow`
--

LOCK TABLES `bookborrow` WRITE;
/*!40000 ALTER TABLE `bookborrow` DISABLE KEYS */;
INSERT INTO `bookborrow` VALUES
(18,4,1,'2024-04-04 03:00:00','2024-06-06 03:00:00',1,'2024-07-09 03:00:00',0,1,0,0),
(19,17,1,'2024-04-04 04:11:00','2024-06-06 04:11:00',1,'2024-05-24 04:11:00',0,1,0,0),
(20,1,1,'2024-05-06 03:00:00','2024-06-06 03:00:00',1,'2024-05-24 02:00:00',0,1,0,0),
(21,1,1,'2024-04-26 11:07:20','2024-04-30 12:00:00',1,'2024-05-29 00:00:00',0,1,0,0),
(22,17,1,'2024-05-01 12:33:15','2024-05-07 16:59:59',1,'2024-06-17 04:10:00',0,1,0,0),
(27,61,2,'2024-05-15 03:00:00','2024-06-15 16:59:59',1,'2024-06-16 03:00:00',0,1,0,0),
(28,61,2,'2024-05-15 03:00:00','2024-06-15 16:59:59',1,'2024-07-18 04:12:00',0,1,0,0),
(29,61,2,'2024-05-15 03:00:00','2024-06-15 16:59:59',0,NULL,0,0,0,0),
(31,17,22,'2024-06-09 14:51:50','2024-06-23 16:59:59',1,'2024-06-10 02:15:00',0,1,0,0),
(32,1,21,'2024-06-10 03:00:00','2024-06-18 15:00:00',1,'2024-06-16 04:01:00',0,1,0,0),
(34,61,1,'2024-05-15 03:00:00','2024-06-15 16:59:59',0,NULL,0,0,0,0),
(35,61,1,'2024-05-15 03:00:00','2024-06-15 16:59:59',0,NULL,0,0,0,0),
(36,61,1,'2024-05-15 03:00:00','2024-06-15 16:59:59',0,NULL,0,0,0,0),
(37,61,1,'2024-05-15 03:00:00','2024-06-15 16:59:59',0,NULL,0,0,0,0),
(38,61,1,'2024-05-15 03:00:00','2024-06-15 16:59:59',0,NULL,0,0,0,0),
(39,61,1,'2024-05-15 03:00:00','2024-06-15 16:59:59',0,NULL,0,0,0,0),
(40,61,1,'2024-05-15 03:00:00','2024-06-15 16:59:59',0,NULL,0,0,0,0),
(41,61,1,'2024-05-15 03:00:00','2024-06-15 16:59:59',0,NULL,0,0,0,0),
(42,61,1,'2024-05-15 03:00:00','2024-06-15 16:59:59',0,NULL,0,0,0,0),
(43,61,1,'2024-05-15 03:00:00','2024-06-15 16:59:59',0,NULL,0,0,0,0),
(46,4,27,'2024-07-02 07:39:42','2024-07-16 16:59:59',1,'2024-07-18 02:04:00',0,1,0,0),
(47,61,4,'2024-07-17 18:01:56','2024-08-01 16:59:59',1,'2024-07-18 12:20:00',1,1,1,0),
(49,61,4,'2024-06-06 03:00:00','2024-07-07 03:00:00',1,'2024-07-17 10:30:00',0,1,1,0),
(50,61,4,'2024-06-06 03:00:00','2024-07-07 03:00:00',1,'2024-07-17 03:00:00',0,1,0,0),
(51,61,4,'2024-06-06 03:00:00','2024-06-07 03:00:00',1,'2024-08-23 09:04:53',0,1,1,0),
(54,61,4,'2024-07-10 07:00:00','2024-07-21 13:00:00',1,'2024-08-21 03:00:00',0,1,1,0),
(55,61,4,'2024-07-10 07:00:00','2024-08-04 13:00:00',0,NULL,0,0,0,1),
(56,61,1,'2024-07-07 03:00:00','2024-07-21 03:00:00',0,NULL,0,0,0,0),
(57,61,1,'2024-07-02 03:00:00','2024-07-30 03:00:00',0,NULL,0,0,1,0),
(58,61,1,'2024-07-22 04:11:00','2024-07-31 03:00:00',0,NULL,0,0,0,0);
/*!40000 ALTER TABLE `bookborrow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookfavorite`
--

DROP TABLE IF EXISTS `bookfavorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bookfavorite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookId` int(11) DEFAULT NULL,
  `userId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bookId` (`bookId`),
  KEY `userId` (`userId`),
  CONSTRAINT `bookfavorite_ibfk_1` FOREIGN KEY (`bookId`) REFERENCES `book` (`id`),
  CONSTRAINT `bookfavorite_ibfk_2` FOREIGN KEY (`userId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookfavorite`
--

LOCK TABLES `bookfavorite` WRITE;
/*!40000 ALTER TABLE `bookfavorite` DISABLE KEYS */;
INSERT INTO `bookfavorite` VALUES
(7,61,4),
(11,4,4),
(13,17,4),
(14,1,4);
/*!40000 ALTER TABLE `bookfavorite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookfile`
--

DROP TABLE IF EXISTS `bookfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bookfile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookId` int(11) DEFAULT NULL,
  `fileSrc` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bookId` (`bookId`),
  CONSTRAINT `bookfile_ibfk_1` FOREIGN KEY (`bookId`) REFERENCES `book` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookfile`
--

LOCK TABLES `bookfile` WRITE;
/*!40000 ALTER TABLE `bookfile` DISABLE KEYS */;
INSERT INTO `bookfile` VALUES
(1,4,'shelley-frankenstein-1818.pdf'),
(3,1,'book0530.pdf'),
(5,61,'final_semester_project-4.pdf');
/*!40000 ALTER TABLE `bookfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookgenre`
--

DROP TABLE IF EXISTS `bookgenre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bookgenre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookId` int(11) DEFAULT NULL,
  `genreId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bookId` (`bookId`),
  KEY `genreId` (`genreId`),
  CONSTRAINT `bookgenre_ibfk_1` FOREIGN KEY (`bookId`) REFERENCES `book` (`id`),
  CONSTRAINT `bookgenre_ibfk_2` FOREIGN KEY (`genreId`) REFERENCES `genre` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=203 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookgenre`
--

LOCK TABLES `bookgenre` WRITE;
/*!40000 ALTER TABLE `bookgenre` DISABLE KEYS */;
INSERT INTO `bookgenre` VALUES
(79,24,10),
(80,24,11),
(143,17,30),
(144,17,31),
(147,74,33),
(151,4,4),
(152,4,5),
(153,4,6),
(154,4,7),
(196,96,62),
(199,1,1),
(200,1,2),
(201,1,3),
(202,1,4);
/*!40000 ALTER TABLE `bookgenre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookimage`
--

DROP TABLE IF EXISTS `bookimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bookimage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookId` int(11) DEFAULT NULL,
  `image` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bookId` (`bookId`),
  CONSTRAINT `bookimage_ibfk_1` FOREIGN KEY (`bookId`) REFERENCES `book` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookimage`
--

LOCK TABLES `bookimage` WRITE;
/*!40000 ALTER TABLE `bookimage` DISABLE KEYS */;
/*!40000 ALTER TABLE `bookimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booklanguage`
--

DROP TABLE IF EXISTS `booklanguage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `booklanguage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookId` int(11) DEFAULT NULL,
  `language` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bookId` (`bookId`),
  CONSTRAINT `booklanguage_ibfk_1` FOREIGN KEY (`bookId`) REFERENCES `book` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booklanguage`
--

LOCK TABLES `booklanguage` WRITE;
/*!40000 ALTER TABLE `booklanguage` DISABLE KEYS */;
INSERT INTO `booklanguage` VALUES
(61,74,'English'),
(65,4,'English'),
(88,61,'English'),
(105,96,'English');
/*!40000 ALTER TABLE `booklanguage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booklocation`
--

DROP TABLE IF EXISTS `booklocation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `booklocation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookId` int(11) DEFAULT NULL,
  `roomId` varchar(30) DEFAULT NULL,
  `shelfId` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bookId` (`bookId`),
  CONSTRAINT `booklocation_ibfk_1` FOREIGN KEY (`bookId`) REFERENCES `book` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booklocation`
--

LOCK TABLES `booklocation` WRITE;
/*!40000 ALTER TABLE `booklocation` DISABLE KEYS */;
INSERT INTO `booklocation` VALUES
(2,4,'G3','A14');
/*!40000 ALTER TABLE `booklocation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) DEFAULT NULL,
  `comment` varchar(3000) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `bookId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `userId` (`userId`),
  KEY `bookId` (`bookId`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`bookId`) REFERENCES `book` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES
(1,1,'This book is great!',10,4),
(3,1,'Test comment 2',10,4),
(5,4,'Test comment',9,1),
(6,4,'This looks good!',9,17),
(7,4,'test comment',9,24),
(9,4,'Testing if Vue static files can work on Flask!',9,4),
(10,4,'Test comment',9,1),
(13,4,'test',9,1),
(14,4,'Test content',9,1),
(15,4,'Test content',8,1),
(16,16,'Test comment',7,1),
(22,4,'Test comment',10,4),
(24,4,'',1,17),
(25,4,'',9,61),
(26,4,'Test comment',8,4);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment_like`
--

DROP TABLE IF EXISTS `comment_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment_like` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `commentId` int(11) DEFAULT NULL,
  `userId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `commentId` (`commentId`),
  KEY `userId` (`userId`),
  CONSTRAINT `comment_like_ibfk_1` FOREIGN KEY (`commentId`) REFERENCES `comment` (`id`),
  CONSTRAINT `comment_like_ibfk_2` FOREIGN KEY (`userId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_like`
--

LOCK TABLES `comment_like` WRITE;
/*!40000 ALTER TABLE `comment_like` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genre`
--

DROP TABLE IF EXISTS `genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `genre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genre`
--

LOCK TABLES `genre` WRITE;
/*!40000 ALTER TABLE `genre` DISABLE KEYS */;
INSERT INTO `genre` VALUES
(1,'Epic'),
(2,'Parody'),
(3,'Satire'),
(4,'Novel'),
(5,'Horror'),
(6,'Science Fiction'),
(7,'Gothic Novel'),
(10,'Conspiracy Thriller'),
(11,'War & Millitary Fiction'),
(30,'Romance'),
(31,'Fantasy'),
(33,'Test genre'),
(62,'');
/*!40000 ALTER TABLE `genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `library_place`
--

DROP TABLE IF EXISTS `library_place`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `library_place` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `haveComputer` tinyint(1) DEFAULT NULL,
  `room` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `library_place`
--

LOCK TABLES `library_place` WRITE;
/*!40000 ALTER TABLE `library_place` DISABLE KEYS */;
INSERT INTO `library_place` VALUES
(1,1,'E2'),
(3,1,'E2'),
(4,1,'E2'),
(5,1,'E2'),
(6,1,'E3'),
(7,1,'E1'),
(8,1,'E1'),
(9,1,'E1'),
(10,1,'E1'),
(11,1,'E1'),
(12,0,'E1'),
(13,0,'E1'),
(14,1,'E1'),
(15,1,'E3'),
(21,1,'103');
/*!40000 ALTER TABLE `library_place` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `library_session`
--

DROP TABLE IF EXISTS `library_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `library_session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `placeId` int(11) DEFAULT NULL,
  `inUse` tinyint(1) DEFAULT NULL,
  `startDate` datetime DEFAULT NULL,
  `userId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `placeId` (`placeId`),
  KEY `userId` (`userId`),
  CONSTRAINT `library_session_ibfk_1` FOREIGN KEY (`placeId`) REFERENCES `library_place` (`id`),
  CONSTRAINT `library_session_ibfk_2` FOREIGN KEY (`userId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `library_session`
--

LOCK TABLES `library_session` WRITE;
/*!40000 ALTER TABLE `library_session` DISABLE KEYS */;
INSERT INTO `library_session` VALUES
(1,3,0,'2024-09-12 10:00:00',4),
(3,3,0,'2024-09-21 10:00:00',4);
/*!40000 ALTER TABLE `library_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `library_session_book`
--

DROP TABLE IF EXISTS `library_session_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `library_session_book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sessionId` int(11) DEFAULT NULL,
  `bookId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sessionId` (`sessionId`),
  KEY `bookId` (`bookId`),
  CONSTRAINT `library_session_book_ibfk_1` FOREIGN KEY (`sessionId`) REFERENCES `library_session` (`id`),
  CONSTRAINT `library_session_book_ibfk_2` FOREIGN KEY (`bookId`) REFERENCES `book` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `library_session_book`
--

LOCK TABLES `library_session_book` WRITE;
/*!40000 ALTER TABLE `library_session_book` DISABLE KEYS */;
INSERT INTO `library_session_book` VALUES
(1,1,15),
(2,1,15),
(3,1,1);
/*!40000 ALTER TABLE `library_session_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monthly_sessioncount`
--

DROP TABLE IF EXISTS `monthly_sessioncount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monthly_sessioncount` (
  `browserOrOs` varchar(60) NOT NULL,
  `type` varchar(30) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `lastUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`browserOrOs`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monthly_sessioncount`
--

LOCK TABLES `monthly_sessioncount` WRITE;
/*!40000 ALTER TABLE `monthly_sessioncount` DISABLE KEYS */;
INSERT INTO `monthly_sessioncount` VALUES
('704','country',36,'2024-09-13 14:16:03'),
('840','country',0,'2024-07-19 13:15:04'),
('Android','os',5,'2024-09-13 10:46:24'),
('Chrome','browser',1,'2024-07-19 00:56:36'),
('Firefox','browser',31,'2024-09-13 14:16:03'),
('Firefox Mobile','browser',5,'2024-09-13 10:46:24'),
('iOS','os',2,'2024-07-19 18:24:56'),
('Linux','os',2,'2024-07-19 02:26:31'),
('Mac OS X','os',1,'2024-07-19 00:56:19'),
('Mobile Safari','browser',2,'2024-07-19 18:24:56'),
('Safari','browser',1,'2024-07-19 00:56:19'),
('Windows','os',31,'2024-09-13 14:16:03');
/*!40000 ALTER TABLE `monthly_sessioncount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) DEFAULT NULL,
  `os` varchar(50) DEFAULT NULL,
  `browser` varchar(50) DEFAULT NULL,
  `referer` varchar(500) DEFAULT NULL,
  `ipAddress` varchar(500) DEFAULT NULL,
  `sessionTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `userId` (`userId`),
  CONSTRAINT `session_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
INSERT INTO `session` VALUES
(3,4,'Linux','Firefox',NULL,'::1','2024-07-19 02:26:31'),
(4,4,'Windows','Firefox',NULL,'::1','2024-07-19 02:31:26'),
(5,4,'Android','Firefox Mobile',NULL,'::1','2024-07-19 12:52:30'),
(6,4,'Android','Firefox Mobile','https://easylib.jesse-tong.work/login','113.185.74.24','2024-07-19 13:15:04'),
(7,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','14.169.33.144','2024-07-19 16:30:40'),
(8,4,'Windows','Firefox','https://easylib.jesse-tong.work/admin/reports','14.169.31.144','2024-07-19 18:23:27'),
(9,4,'iOS','Mobile Safari','https://easylib.jesse-tong.work/','14.169.31.144','2024-07-19 18:24:56'),
(10,4,'Windows','Firefox','http://localhost/login','127.0.0.1','2024-07-20 08:53:55'),
(11,31,'Windows','Firefox','https://easylib.jesse-tong.work/login','14.169.31.144','2024-07-21 12:10:10'),
(12,4,'Windows','Firefox','http://localhost:5173/','2405:4802:a451:4eb0:5835:61f8:1f:7858','2024-08-15 12:50:22'),
(13,4,'Windows','Firefox','http://localhost:5173/','2405:4802:a451:4eb0:7c93:abf0:e109:9bba','2024-08-20 09:48:50'),
(14,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a451:4eb0:697b:2007:d096:27de','2024-08-21 21:40:29'),
(15,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a470:f760:a50d:13e5:55a9:eb55','2024-08-22 14:12:28'),
(16,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a470:f760:64e3:4906:f40d:a0c3','2024-08-23 08:35:09'),
(17,4,'Windows','Firefox','https://intro-se21-22group1-production.up.railway.app/','2405:4802:a470:f760:8d55:3bae:32d:4dfa','2024-08-24 17:40:51'),
(18,35,'Windows','Firefox','http://localhost:5000/?userId=35&name=Khang%20T%E1%BB%91ng%20Nguy%E1%BB%85n%20Minh%20(21120263)&role=user','127.0.0.1','2024-08-24 18:29:43'),
(19,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a470:f760:b4cc:f9b5:bd20:72d9','2024-08-25 10:29:06'),
(20,4,'Android','Firefox Mobile','https://easylib.jesse-tong.work/login','113.185.77.114','2024-08-25 18:30:09'),
(21,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a470:f760:a15b:68a5:7b0f:6442','2024-08-25 19:02:44'),
(22,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a470:f760:68f0:90ea:1ddd:d268','2024-08-26 17:28:30'),
(23,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a470:f760:c05c:898e:b5f3:855c','2024-08-27 10:00:42'),
(24,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a470:f760:38fd:c0df:713a:b9f0','2024-08-27 16:51:28'),
(25,1,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a470:f760:38fd:c0df:713a:b9f0','2024-08-27 17:10:09'),
(26,4,'Android','Firefox Mobile','https://easylib.jesse-tong.work/login?error=You+must+log+in+first+before+update+password!','113.185.75.151','2024-08-28 10:13:53'),
(27,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a470:f760:355f:db3c:a940:c5ff','2024-08-28 11:43:33'),
(28,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a41a:e740:d983:81ba:b788:d763','2024-09-03 15:35:33'),
(29,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a41a:e740:4d06:355e:a3f9:bd93','2024-09-04 15:00:58'),
(30,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a41a:e740:8da9:dce2:f79d:d311','2024-09-05 08:40:12'),
(31,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a41a:e740:3c58:387a:4d3e:e83c','2024-09-05 13:33:06'),
(32,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a41a:e740:a9b8:8ffd:939a:428e','2024-09-07 11:35:22'),
(33,4,'Android','Firefox Mobile','https://easylib.jesse-tong.work/login','113.185.76.99','2024-09-07 11:42:48'),
(34,35,'Android','Firefox Mobile','https://easylib.jesse-tong.work/?userId=35&name=Khang%20T%E1%BB%91ng%20Nguy%E1%BB%85n%20Minh%20(21120263)&role=user','113.185.76.99','2024-09-07 11:50:38'),
(35,35,'Windows','Firefox','https://easylib.jesse-tong.work/?userId=35&name=Khang%20T%E1%BB%91ng%20Nguy%E1%BB%85n%20Minh%20(21120263)&role=user','2405:4802:a41a:e740:a9b8:8ffd:939a:428e','2024-09-07 11:53:30'),
(36,31,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a41a:e740:a9b8:8ffd:939a:428e','2024-09-07 11:55:20'),
(37,4,'Windows','Firefox','http://localhost:5173/','2405:4802:a3f1:aaf0:d80e:e26d:75fb:d806','2024-09-11 15:14:42'),
(38,4,'Windows','Firefox','https://easylib.jesse-tong.work/login','2405:4802:a47b:1c50:e49c:270a:ed53:6879','2024-09-13 08:32:04'),
(39,4,'Android','Firefox Mobile','https://easylib.jesse-tong.work/login','113.185.78.56','2024-09-13 10:46:24');
/*!40000 ALTER TABLE `session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(530) DEFAULT NULL,
  `name` varchar(300) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `isRestricted` tinyint(1) DEFAULT NULL,
  `isVerified` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES
(1,'jesse-tong@gmail.com','scrypt:32768:8:1$Np75qqYJfk5Dw5Tn$7084996e23ccc3350118ad41e5c9028325e48ceaf0586ef65549704c36b8b003dd86630dde514368bbe51cc1ef83b97c2fcd612bbc7c75e4ba2e95638a70a160','Jesse Tong','user',1,0),
(2,'jesse-tong2@gmail.com','scrypt:32768:8:1$9JYSQ9qYvuCys34h$384ef4e9afee3dd63989b090478acdc34b334629e102b855f3fa5cc83017b725a7530745b2a898989d25767bd89376a2971cf9e5901ff06fec7af4ff7993b00f','Jesse Tong','user',0,0),
(3,'some-email@gmail.com','scrypt:32768:8:1$PGeJpOZxpeeu61HB$9a6fcd91ed9ce51bb018c181165770aece093ad9c3b74e9ac33d1955e49518c306b0fe7d57a732d93f15bdee95ce95bbe83cbada30861464a05f2514ac58cb48','Test user','admin',0,0),
(4,'jesse-tong3@gmail.com','scrypt:32768:8:1$nVLNRwXNYrezmgtw$05c8aab4745cae0a114288d5c19c9ca129d7c4c695bd7c4d5161cbbb205fcafe8b11249a550514031e13f4ae6e9ffc37f8e1c1ed425a2a92512f9c50a102f8eb','Test account 3','admin',0,0),
(5,'jesse-tong7@gmail.com','scrypt:32768:8:1$LjNdixV1kT1X2seZ$6f03758756a8c57e0d51d65e7c0623133571e7ebedbe3fb21212870a414cde6ca086825197572a8a4ce37144d6c51a99ab9e726d54325c17c9a2d5b83f869b97','Jesse Tong','user',0,0),
(6,'jesse-tong3gmail.com','scrypt:32768:8:1$JdtgzqZB1wClEBCZ$85791dcae07181c7ff1e679e258f32dd662098b1758204babbe05f9079d6a093afa5f36965d61bdbc678d037c1bc0dd23b57ce32e38ea619bb7848a9ba4775c0','some name','user',0,0),
(15,'Laurine_Hand45','scrypt:32768:8:1$YlyT2bd6V41FhIFm$3035d2833ad81efb9e0a29ad0c93ce39944dd3fb20b28b3b1a8c36bb4606036c21a73b85c194e3ad3b6f4b7eef1850a9307ca5c2c5a343cf8262797ec8432b95','Crystal87','user',0,0),
(16,'jesse-tong4@gmail.com','scrypt:32768:8:1$6Y586WSlXl0pA7rV$d6db2c2d26fd95d93fb6a75c217550760a8b056c0d4be7427b1579510d1d1dc556a34dea92740e9eaecfb8d04251334e1cca372a696339b5f3df789f9db80422','User 4','user',0,0),
(17,'\'a@gmail.com\' or 1 = 1','scrypt:32768:8:1$cZXq5PK6aPgZ0fzg$75f4792617c540128f9e77cda9eb19441a2bf1b696a4047a8c8d04e3d3a9b7f3cf81096517167072b4de3b6efb0f53c9a95ad2feaebbe360314e96ef70bd532e','User 7','user',0,0),
(18,'\"abc@gmail.com\" or user.email = user.email','scrypt:32768:8:1$ucCBl3r9y5qHR3WG$bb1e8e075e16f79147fbc8495d199bd5b63bc28c60cb117ffd98cf871a465ca48de2e1b56ebfac5abb6d4f0fb8786e21d1c7d32437dfcb48c17eb58c037f3a63','jesse-tong3@gmail.com','user',0,0),
(19,'ttttt@gmail.com','scrypt:32768:8:1$XZO0l1jJGguH3xIp$b6d908f2f97e181308319935f541d2488a56ab557b8c9e398266a1aa167aad06d91b136bb363764a20a6d83e33e68919fb248559a83c16f3febca7752b583651','ttttttt','user',0,0),
(20,'t@gmail.com','scrypt:32768:8:1$HR6BjSGDkW1eacUc$b89586bd3e6a6e6b6239ab1cb1106a44fd58b60b0e68185c9c379761b4deb04f511f4240d34610211dfa473eb06f8def9922b44e520ba6663858aeade0538e61','ttttt','user',0,0),
(21,'test2@gmail.com','scrypt:32768:8:1$j0Zx3eChNifCiYd3$cddacb25cb04645d2d9b460f7f385830062bcbf903266c4fcbf8044411df9782e2f232a739abd820efa0c1b77f0ec46846ca4d85a05d3ffc3947826a6726ba43','Test user','user',0,0),
(22,'test3@gmail.com','scrypt:32768:8:1$A3bLMuLgJ1MNRRk0$c30ef771c8cbd649e442129566531d3f1c56957b3c7987179a127cca7b7e57258825c1ff761b145b4877e6dc49b868cc2631eef1a287ab34914a02bee48da0c9','Test user 3','admin',0,0),
(23,'Jerald55@hotmail.com','scrypt:32768:8:1$6PjabneNjI0Dkcak$14369e40e1c5a8f2349ea5ea1d2c3d9a27ae82bb43fb671b1f067644bcaf9340be74e4b294783bf97f5269a0d36e4d34faedb0b166ba21f6f06aa3c9a763d991','Leonie43','user',0,0),
(24,'Tierra44@gmail.com','scrypt:32768:8:1$itNq4HcgCjRDmGsq$123b1062276b46f29e3678655a0151e5dfc1b1d2f17a6311a6ea0dfd16a1c663de95f3dd99033b2bb790be48382c557f2ac33ff0950f7b9eb530a10b115c7fd1','Karina44','user',0,0),
(25,'Bertram.Mills@yahoo.com','scrypt:32768:8:1$samtTcvbwq8dSBVn$c8b0c835d520e263394890ee8953de622dfb0ae56e548ac2c38a49a8f33cd44ccb1814bbd989ea5afb980518b4a23674d3c560cfc3a06d2218f66b764bba27f1','Napoleon_Russel','admin',0,0),
(26,'test@gmail.com','scrypt:32768:8:1$gmhXb5e0xSyhHax6$e2a57d9a04c0fd6b6a593555abf036ec169d7af5e64dadbda11db1213c659e8a716a53f2f9c0d8554dbd5129f1cf4de4010c681eb37864b0a5747dcc7f44125e','User 2','admin',0,0),
(27,'test4@gmail.com','scrypt:32768:8:1$j8FPsciMVQvp0sRH$58507b49c4cdf600400242bda170c941a7d70f892c4a8fef2931fd216d8821331a0c0dc08b394b2ecf0843eee857a62e6a325a74a1c73c0fe6a83de1703895e2','Demo user','user',0,0),
(29,'voquocbao124@gmail.com',NULL,'Quốc Bảo Võ','user',0,0),
(31,'ledohe7516@tiervio.com','scrypt:32768:8:1$AZw89goSEmI2vTsz$0969599da142421293ffc6f47ee3c728a6ec46c8ff8b9dd9240283b9c9e6a4c236c7649f40a0f74ddb426004618ca9dd24b51410309971c7cb2633877e99c148','jesse-tong3@gmail.com','admin',0,1),
(32,'jehex73381@alientex.com','scrypt:32768:8:1$rIzGPM94798J8jo8$13677680cb3a75fb549411837c6355d07460387fed787096280ea09dcebd340b55259bd6d669e7592d89b07c3efb93fca70b8a42336f035d11eaa841bce757be','test','user',0,0),
(33,'todod11718@biscoine.com','scrypt:32768:8:1$W1DR9iNB6ZuSZJLG$8d66c53f7170a5884384b5deb59e115fb1e7622badb3369abda7ee8076d61801ef5ef7825e586e889681bd910154846498979a14d7388a6341c7f62b0d0bd052','test','user',0,0),
(34,'jabawo1794@alientex.com','scrypt:32768:8:1$jvX6etkuVHR2wzSa$90c1fb61c14a11159d41c7b0ceab34fb1d1a12602e51d90ee41340996af45167e08fcf5a1f47154b66a909dad15977c9c7b109002cae71cce31c305af511d5cf','test','user',0,0),
(35,'tongnguyenminhkhang21012020@gmail.com',NULL,'Khang Tống Nguyễn Minh (21120263)','user',0,0),
(36,'cerako5892@avashost.com','scrypt:32768:8:1$RyEsbUDbjcpkMIrW$18b0692a3668b0ad7c4a6227b04cbaee32c6dae4e1e4d7e58c006886145ab56368f4e635027e4d774ee4377674e8521e0223eff2ac9e6c7e21fa1e5ea564c04e','test','user',0,0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_following`
--

DROP TABLE IF EXISTS `user_following`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_following` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `follower` int(11) DEFAULT NULL,
  `followedUser` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `follower` (`follower`),
  KEY `followedUser` (`followedUser`),
  CONSTRAINT `user_following_ibfk_1` FOREIGN KEY (`follower`) REFERENCES `user` (`id`),
  CONSTRAINT `user_following_ibfk_2` FOREIGN KEY (`followedUser`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_following`
--

LOCK TABLES `user_following` WRITE;
/*!40000 ALTER TABLE `user_following` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_following` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_image`
--

DROP TABLE IF EXISTS `user_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) DEFAULT NULL,
  `imagePath` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `userId` (`userId`),
  CONSTRAINT `user_image_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_image`
--

LOCK TABLES `user_image` WRITE;
/*!40000 ALTER TABLE `user_image` DISABLE KEYS */;
INSERT INTO `user_image` VALUES
(4,4,'EasyLibNotificationClass.PNG'),
(5,4,'Capture3.PNG'),
(9,4,'DgDmZqnI9BRWvNdBMGJ28LYN.jpg'),
(10,4,'Capture.PNG');
/*!40000 ALTER TABLE `user_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_info`
--

DROP TABLE IF EXISTS `user_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `maxBorrow` int(11) DEFAULT NULL,
  `borrowLeft` int(11) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL,
  `imagePath` varchar(300) DEFAULT NULL,
  `alternateEmail` varchar(100) DEFAULT NULL,
  `alternatePhone` varchar(20) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `expires` datetime DEFAULT NULL,
  `zipCode` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `userId` (`userId`),
  CONSTRAINT `user_info_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_info`
--

LOCK TABLES `user_info` WRITE;
/*!40000 ALTER TABLE `user_info` DISABLE KEYS */;
INSERT INTO `user_info` VALUES
(1,1,21,'other',5,5,'0888888888','Some address','1003w-Ah-do4Y91lk-1.webp',NULL,NULL,'user',NULL,NULL),
(2,4,21,'other',5,5,NULL,'Some address','Group 1 - Introduction to SE - EasyLib Register login user .png','tongnguyenminhkhang21012020@gmail.com',NULL,'user',NULL,NULL),
(3,22,21,'male',5,5,'089777777','Some address, HCM City',NULL,NULL,NULL,'user',NULL,NULL),
(5,4,21,'other',5,5,'0878668596','Some address',NULL,'tongnguyenminhkhang21012020@gmail.com',NULL,'library_card','2025-09-15 13:00:00',''),
(6,31,19,NULL,5,5,'0878668596','test',NULL,NULL,NULL,'user',NULL,NULL),
(7,35,21,NULL,5,5,'0987654321','Some address','1f6e29b7f11718cc.jpg',NULL,NULL,'user',NULL,NULL);
/*!40000 ALTER TABLE `user_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_notification`
--

DROP TABLE IF EXISTS `user_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) DEFAULT NULL,
  `notification` varchar(3000) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `userId` (`userId`),
  CONSTRAINT `user_notification_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf32 COLLATE=utf32_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_notification`
--

LOCK TABLES `user_notification` WRITE;
/*!40000 ALTER TABLE `user_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'library'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-13 15:01:58
