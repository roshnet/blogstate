-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 07, 2019 at 09:42 PM
-- Server version: 5.7.26-0ubuntu0.18.04.1
-- PHP Version: 7.2.17-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `blogstate`
--

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `comment_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `author_uid` int(11) NOT NULL,
  `message` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `credentials`
--

CREATE TABLE `credentials` (
  `user_id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `hash` varchar(256) NOT NULL,
  `email` varchar(100) NOT NULL,
  `name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `credentials`
--

INSERT INTO `credentials` (`user_id`, `username`, `hash`, `email`, `name`) VALUES
(1, 'roshnet', 'sha1$dAwGuBM9$9c1460f47199fd7ccf448fe52c89a9a01493cb48', 'roshan@gmail.com', 'Roshan Sharma'),
(2, 'saksham12', 'sha1$a4yaMvMu$8368f15deb303e099b23f29301ad69fdb9830ccf', 'saksham12@gmail.com', 'Saksham Singh'),
(3, 'authcoder', 'sha1$uYRaVz3e$13da2742387dd7f03eaf6b02299a56d07ca7b1ca', 'sig@gmail.com', 'Siddhartha'),
(4, 'userone', 'sha1$sbdPcE4V$87937667502f8d5979669b4b7571fc58d2c2559d', 'userone@gmail.com', 'User one'),
(5, 'usertwo', 'sha1$yWSQRnwI$03499a8a95828345eccd608b326b3602baa7d1e5', 'usertwo@gmail.com', 'User Two'),
(6, 'pnijhara', 'sha1$WtQ2fOfC$f1415f8cd8b26faf0d411f0f3c0b359e1d340d92', 'prajjwalnijhara@gmail.com', 'Prajjwal Nijhara');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `post_id` int(11) NOT NULL,
  `author_uid` int(11) NOT NULL,
  `title` varchar(100) NOT NULL DEFAULT 'New Article',
  `body` text NOT NULL,
  `likes` int(11) NOT NULL DEFAULT '0',
  `time` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`post_id`, `author_uid`, `title`, `body`, `likes`, `time`) VALUES
(1, 3, 'Boring Sunday', 'This Sunday is the <b>most</b> boring I\'ve ever seen.', 0, ''),
(2, 6, 'New Article', 'This is a new article meant for testing.', 0, ''),
(3, 1, 'Test Article', 'This is an amazing article!', 5, NULL),
(4, 6, 'My second article', 'Hi, this is my second article.', 8, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`comment_id`),
  ADD KEY `post_id` (`post_id`),
  ADD KEY `author_uid` (`author_uid`);

--
-- Indexes for table `credentials`
--
ALTER TABLE `credentials`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username_2` (`username`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_id`),
  ADD KEY `title` (`title`),
  ADD KEY `author_uid` (`author_uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `comment_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `credentials`
--
ALTER TABLE `credentials`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `post_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`post_id`),
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`author_uid`) REFERENCES `credentials` (`user_id`);

--
-- Constraints for table `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`author_uid`) REFERENCES `credentials` (`user_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
