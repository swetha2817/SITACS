-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 16, 2022 at 07:41 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ai_cloud`
--

-- --------------------------------------------------------

--
-- Table structure for table `downloadrequest`
--

CREATE TABLE `downloadrequest` (
  `id` int(10) NOT NULL,
  `username` varchar(50) NOT NULL,
  `filename` varchar(50) NOT NULL,
  `fileaccesskey` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `otp` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `downloadrequest`
--

INSERT INTO `downloadrequest` (`id`, `username`, `filename`, `fileaccesskey`, `status`, `otp`) VALUES
(1, 'jas', 'Python Flask upload a file.mp4', '5620c4167dcb34375739b990', 'Downloaded', '');

-- --------------------------------------------------------

--
-- Table structure for table `reg`
--

CREATE TABLE `reg` (
  `id` int(10) NOT NULL,
  `cloudname` varchar(50) NOT NULL,
  `cloudownername` varchar(50) NOT NULL,
  `accesskey` varchar(50) NOT NULL,
  `port` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `uname` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `reg`
--

INSERT INTO `reg` (`id`, `cloudname`, `cloudownername`, `accesskey`, `port`, `phone`, `email`, `uname`, `password`, `status`) VALUES
(4, 'Globus', 'Jeya', '1234', '8080', '8667733206', 'jaslakshu@gmail.com', 'jas', 'jas', '1'),
(5, 'Globus', 'Jas', '1234', '8080', '8667733206', 'jaslakshu@gmail.com', 'jj', 'jj', 'False');

-- --------------------------------------------------------

--
-- Table structure for table `upload`
--

CREATE TABLE `upload` (
  `id` int(10) NOT NULL,
  `username` varchar(50) NOT NULL,
  `filename` varchar(50) NOT NULL,
  `filedec` varchar(50) NOT NULL,
  `filepath` varchar(50) NOT NULL,
  `fileaccesskey` varchar(50) NOT NULL,
  `datetime` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `upload`
--

INSERT INTO `upload` (`id`, `username`, `filename`, `filedec`, `filepath`, `fileaccesskey`, `datetime`) VALUES
(2, 'jas', 'Python Flask upload a file.mp4', 'Video File', 'static/files/Python Flask upload a file.mp4', '5620c4167dcb34375739b990', '2022-04-16 02:37:15.916494'),
(3, 'jas', 'File Uploading with Flask Tamil.mp4', 'Video File', 'static/files/File Uploading with Flask Tamil.mp4', '6b6ff2d7587f38cef5f64724', '2022-04-16 11:07:42.112523');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `downloadrequest`
--
ALTER TABLE `downloadrequest`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reg`
--
ALTER TABLE `reg`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `upload`
--
ALTER TABLE `upload`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `downloadrequest`
--
ALTER TABLE `downloadrequest`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `reg`
--
ALTER TABLE `reg`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `upload`
--
ALTER TABLE `upload`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
