-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 31, 2025 at 01:11 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wifi`
--

-- --------------------------------------------------------

--
-- Table structure for table `area_layanan`
--

CREATE TABLE `area_layanan` (
  `id_area_layanan` int(11) NOT NULL,
  `nama_area` varchar(100) NOT NULL,
  `kode_pos` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `area_layanan`
--

INSERT INTO `area_layanan` (`id_area_layanan`, `nama_area`, `kode_pos`) VALUES
(1, 'Jakarta Selatan', '12110'),
(2, 'Surabaya Pusat', '60171'),
(3, 'Bandung Kota', '40111');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add area layanan', 7, 'add_arealayanan'),
(26, 'Can change area layanan', 7, 'change_arealayanan'),
(27, 'Can delete area layanan', 7, 'delete_arealayanan'),
(28, 'Can view area layanan', 7, 'view_arealayanan'),
(29, 'Can add jenis jasa', 8, 'add_jenisjasa'),
(30, 'Can change jenis jasa', 8, 'change_jenisjasa'),
(31, 'Can delete jenis jasa', 8, 'delete_jenisjasa'),
(32, 'Can view jenis jasa', 8, 'view_jenisjasa'),
(33, 'Can add jenis perangkat', 9, 'add_jenisperangkat'),
(34, 'Can change jenis perangkat', 9, 'change_jenisperangkat'),
(35, 'Can delete jenis perangkat', 9, 'delete_jenisperangkat'),
(36, 'Can view jenis perangkat', 9, 'view_jenisperangkat'),
(37, 'Can add langganan', 10, 'add_langganan'),
(38, 'Can change langganan', 10, 'change_langganan'),
(39, 'Can delete langganan', 10, 'delete_langganan'),
(40, 'Can view langganan', 10, 'view_langganan'),
(41, 'Can add metode pembayaran', 11, 'add_metodepembayaran'),
(42, 'Can change metode pembayaran', 11, 'change_metodepembayaran'),
(43, 'Can delete metode pembayaran', 11, 'delete_metodepembayaran'),
(44, 'Can view metode pembayaran', 11, 'view_metodepembayaran'),
(45, 'Can add paket layanan', 12, 'add_paketlayanan'),
(46, 'Can change paket layanan', 12, 'change_paketlayanan'),
(47, 'Can delete paket layanan', 12, 'delete_paketlayanan'),
(48, 'Can view paket layanan', 12, 'view_paketlayanan'),
(49, 'Can add pelanggan', 13, 'add_pelanggan'),
(50, 'Can change pelanggan', 13, 'change_pelanggan'),
(51, 'Can delete pelanggan', 13, 'delete_pelanggan'),
(52, 'Can view pelanggan', 13, 'view_pelanggan'),
(53, 'Can add pembayaran', 14, 'add_pembayaran'),
(54, 'Can change pembayaran', 14, 'change_pembayaran'),
(55, 'Can delete pembayaran', 14, 'delete_pembayaran'),
(56, 'Can view pembayaran', 14, 'view_pembayaran'),
(57, 'Can add pemesanan jasa', 15, 'add_pemesananjasa'),
(58, 'Can change pemesanan jasa', 15, 'change_pemesananjasa'),
(59, 'Can delete pemesanan jasa', 15, 'delete_pemesananjasa'),
(60, 'Can view pemesanan jasa', 15, 'view_pemesananjasa'),
(61, 'Can add penempatan perangkat', 16, 'add_penempatanperangkat'),
(62, 'Can change penempatan perangkat', 16, 'change_penempatanperangkat'),
(63, 'Can delete penempatan perangkat', 16, 'delete_penempatanperangkat'),
(64, 'Can view penempatan perangkat', 16, 'view_penempatanperangkat'),
(65, 'Can add perangkat', 17, 'add_perangkat'),
(66, 'Can change perangkat', 17, 'change_perangkat'),
(67, 'Can delete perangkat', 17, 'delete_perangkat'),
(68, 'Can view perangkat', 17, 'view_perangkat'),
(69, 'Can add riwayat testing wifi', 18, 'add_riwayattestingwifi'),
(70, 'Can change riwayat testing wifi', 18, 'change_riwayattestingwifi'),
(71, 'Can delete riwayat testing wifi', 18, 'delete_riwayattestingwifi'),
(72, 'Can view riwayat testing wifi', 18, 'view_riwayattestingwifi'),
(73, 'Can add teknisi', 19, 'add_teknisi'),
(74, 'Can change teknisi', 19, 'change_teknisi'),
(75, 'Can delete teknisi', 19, 'delete_teknisi'),
(76, 'Can view teknisi', 19, 'view_teknisi'),
(77, 'Can add area layanan', 20, 'add_arealayanan'),
(78, 'Can change area layanan', 20, 'change_arealayanan'),
(79, 'Can delete area layanan', 20, 'delete_arealayanan'),
(80, 'Can view area layanan', 20, 'view_arealayanan'),
(81, 'Can add jenis jasa', 21, 'add_jenisjasa'),
(82, 'Can change jenis jasa', 21, 'change_jenisjasa'),
(83, 'Can delete jenis jasa', 21, 'delete_jenisjasa'),
(84, 'Can view jenis jasa', 21, 'view_jenisjasa'),
(85, 'Can add jenis perangkat', 22, 'add_jenisperangkat'),
(86, 'Can change jenis perangkat', 22, 'change_jenisperangkat'),
(87, 'Can delete jenis perangkat', 22, 'delete_jenisperangkat'),
(88, 'Can view jenis perangkat', 22, 'view_jenisperangkat'),
(89, 'Can add langganan', 23, 'add_langganan'),
(90, 'Can change langganan', 23, 'change_langganan'),
(91, 'Can delete langganan', 23, 'delete_langganan'),
(92, 'Can view langganan', 23, 'view_langganan'),
(93, 'Can add metode pembayaran', 24, 'add_metodepembayaran'),
(94, 'Can change metode pembayaran', 24, 'change_metodepembayaran'),
(95, 'Can delete metode pembayaran', 24, 'delete_metodepembayaran'),
(96, 'Can view metode pembayaran', 24, 'view_metodepembayaran'),
(97, 'Can add paket layanan', 25, 'add_paketlayanan'),
(98, 'Can change paket layanan', 25, 'change_paketlayanan'),
(99, 'Can delete paket layanan', 25, 'delete_paketlayanan'),
(100, 'Can view paket layanan', 25, 'view_paketlayanan'),
(101, 'Can add pelanggan', 26, 'add_pelanggan'),
(102, 'Can change pelanggan', 26, 'change_pelanggan'),
(103, 'Can delete pelanggan', 26, 'delete_pelanggan'),
(104, 'Can view pelanggan', 26, 'view_pelanggan'),
(105, 'Can add pembayaran', 27, 'add_pembayaran'),
(106, 'Can change pembayaran', 27, 'change_pembayaran'),
(107, 'Can delete pembayaran', 27, 'delete_pembayaran'),
(108, 'Can view pembayaran', 27, 'view_pembayaran'),
(109, 'Can add pemesanan jasa', 28, 'add_pemesananjasa'),
(110, 'Can change pemesanan jasa', 28, 'change_pemesananjasa'),
(111, 'Can delete pemesanan jasa', 28, 'delete_pemesananjasa'),
(112, 'Can view pemesanan jasa', 28, 'view_pemesananjasa'),
(113, 'Can add penempatan perangkat', 29, 'add_penempatanperangkat'),
(114, 'Can change penempatan perangkat', 29, 'change_penempatanperangkat'),
(115, 'Can delete penempatan perangkat', 29, 'delete_penempatanperangkat'),
(116, 'Can view penempatan perangkat', 29, 'view_penempatanperangkat'),
(117, 'Can add perangkat', 30, 'add_perangkat'),
(118, 'Can change perangkat', 30, 'change_perangkat'),
(119, 'Can delete perangkat', 30, 'delete_perangkat'),
(120, 'Can view perangkat', 30, 'view_perangkat'),
(121, 'Can add riwayat testing wifi', 31, 'add_riwayattestingwifi'),
(122, 'Can change riwayat testing wifi', 31, 'change_riwayattestingwifi'),
(123, 'Can delete riwayat testing wifi', 31, 'delete_riwayattestingwifi'),
(124, 'Can view riwayat testing wifi', 31, 'view_riwayattestingwifi'),
(125, 'Can add teknisi', 32, 'add_teknisi'),
(126, 'Can change teknisi', 32, 'change_teknisi'),
(127, 'Can delete teknisi', 32, 'delete_teknisi'),
(128, 'Can view teknisi', 32, 'view_teknisi');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(20, 'layanan_wifi', 'arealayanan'),
(21, 'layanan_wifi', 'jenisjasa'),
(22, 'layanan_wifi', 'jenisperangkat'),
(23, 'layanan_wifi', 'langganan'),
(24, 'layanan_wifi', 'metodepembayaran'),
(25, 'layanan_wifi', 'paketlayanan'),
(26, 'layanan_wifi', 'pelanggan'),
(27, 'layanan_wifi', 'pembayaran'),
(28, 'layanan_wifi', 'pemesananjasa'),
(29, 'layanan_wifi', 'penempatanperangkat'),
(30, 'layanan_wifi', 'perangkat'),
(31, 'layanan_wifi', 'riwayattestingwifi'),
(32, 'layanan_wifi', 'teknisi'),
(6, 'sessions', 'session'),
(7, 'wifi_service', 'arealayanan'),
(8, 'wifi_service', 'jenisjasa'),
(9, 'wifi_service', 'jenisperangkat'),
(10, 'wifi_service', 'langganan'),
(11, 'wifi_service', 'metodepembayaran'),
(12, 'wifi_service', 'paketlayanan'),
(13, 'wifi_service', 'pelanggan'),
(14, 'wifi_service', 'pembayaran'),
(15, 'wifi_service', 'pemesananjasa'),
(16, 'wifi_service', 'penempatanperangkat'),
(17, 'wifi_service', 'perangkat'),
(18, 'wifi_service', 'riwayattestingwifi'),
(19, 'wifi_service', 'teknisi');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-10-30 16:55:34.453152'),
(2, 'auth', '0001_initial', '2025-10-30 16:55:35.058759'),
(3, 'admin', '0001_initial', '2025-10-30 16:55:35.200294'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-10-30 16:55:35.213288'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-10-30 16:55:35.227642'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-10-30 16:55:35.320315'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-10-30 16:55:35.402956'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-10-30 16:55:35.419486'),
(9, 'auth', '0004_alter_user_username_opts', '2025-10-30 16:55:35.428864'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-10-30 16:55:35.489623'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-10-30 16:55:35.493761'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-10-30 16:55:35.503101'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-10-30 16:55:35.520482'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-10-30 16:55:35.538497'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-10-30 16:55:35.561526'),
(16, 'auth', '0011_update_proxy_permissions', '2025-10-30 16:55:35.570526'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-10-30 16:55:35.590773'),
(18, 'sessions', '0001_initial', '2025-10-30 16:55:35.650616'),
(19, 'wifi_service', '0001_initial', '2025-10-30 16:55:35.664616'),
(20, 'layanan_wifi', '0001_initial', '2025-10-31 05:59:43.810068');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('nj4fvg4vanvlzknyhwksbbvz2ad6zj57', 'eyJwZWxhbmdnYW5faWQiOjQsInVzZXJfcm9sZSI6InBlbGFuZ2dhbiJ9:1vEmOC:T1DN-fG3NTJbLcfZlnEiLjO5d_2K0rTjxGdN906KHrY', '2025-11-14 10:29:48.980080');

-- --------------------------------------------------------

--
-- Table structure for table `jenis_jasa`
--

CREATE TABLE `jenis_jasa` (
  `id_jenis_jasa` int(11) NOT NULL,
  `nama_jasa` varchar(100) NOT NULL,
  `biaya` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jenis_jasa`
--

INSERT INTO `jenis_jasa` (`id_jenis_jasa`, `nama_jasa`, `biaya`) VALUES
(1, 'Instalasi Baru', 150000.00),
(2, 'Perbaikan Gangguan Koneksi', 75000.00),
(3, 'Pemasangan Perangkat Tambahan', 100000.00);

-- --------------------------------------------------------

--
-- Table structure for table `jenis_perangkat`
--

CREATE TABLE `jenis_perangkat` (
  `id_jenis_perangkat` int(11) NOT NULL,
  `nama_jenis` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jenis_perangkat`
--

INSERT INTO `jenis_perangkat` (`id_jenis_perangkat`, `nama_jenis`) VALUES
(3, 'Access Point Repeater'),
(2, 'Modem Fiber Optik'),
(1, 'Router WiFi (ONT)');

-- --------------------------------------------------------

--
-- Table structure for table `langganan`
--

CREATE TABLE `langganan` (
  `id_langganan` int(11) NOT NULL,
  `id_pelanggan` int(11) NOT NULL,
  `id_paket` int(11) NOT NULL,
  `tanggal_mulai` date NOT NULL,
  `tanggal_akhir` date DEFAULT NULL,
  `status_langganan` enum('Aktif','Ditangguhkan','Nonaktif') NOT NULL DEFAULT 'Aktif'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `langganan`
--

INSERT INTO `langganan` (`id_langganan`, `id_pelanggan`, `id_paket`, `tanggal_mulai`, `tanggal_akhir`, `status_langganan`) VALUES
(1, 1, 1, '2025-01-20', NULL, 'Aktif'),
(2, 2, 2, '2025-02-25', NULL, 'Aktif'),
(3, 3, 3, '2025-03-30', '2025-09-30', 'Nonaktif');

-- --------------------------------------------------------

--
-- Table structure for table `metode_pembayaran`
--

CREATE TABLE `metode_pembayaran` (
  `id_metode_bayar` int(11) NOT NULL,
  `nama_metode` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `metode_pembayaran`
--

INSERT INTO `metode_pembayaran` (`id_metode_bayar`, `nama_metode`) VALUES
(3, 'Alfamart / Indomaret'),
(2, 'GoPay / OVO'),
(1, 'Virtual Account BCA');

-- --------------------------------------------------------

--
-- Table structure for table `paket_layanan`
--

CREATE TABLE `paket_layanan` (
  `id_paket` int(11) NOT NULL,
  `nama_paket` varchar(100) NOT NULL,
  `kecepatan_mbps` int(11) NOT NULL,
  `harga` decimal(10,2) NOT NULL,
  `deskripsi` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `paket_layanan`
--

INSERT INTO `paket_layanan` (`id_paket`, `nama_paket`, `kecepatan_mbps`, `harga`, `deskripsi`) VALUES
(1, 'Home Basic 20 Mbps', 20, 250000.00, 'Paket dasar untuk browsing dan streaming ringan.'),
(2, 'Home Standard 50 Mbps', 50, 350000.00, 'Paket standar untuk streaming HD dan WFH.'),
(3, 'Home Pro 100 Mbps', 100, 500000.00, 'Paket profesional untuk gaming dan multi-perangkat.');

-- --------------------------------------------------------

--
-- Table structure for table `pelanggan`
--

CREATE TABLE `pelanggan` (
  `id_pelanggan` int(11) NOT NULL,
  `nama_lengkap` varchar(150) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `alamat_pemasangan` text NOT NULL,
  `no_telepon` varchar(15) DEFAULT NULL,
  `tanggal_daftar` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pelanggan`
--

INSERT INTO `pelanggan` (`id_pelanggan`, `nama_lengkap`, `email`, `password_hash`, `alamat_pemasangan`, `no_telepon`, `tanggal_daftar`) VALUES
(1, 'Andi Wijaya', 'andi@example.com', 'hash_pw_andi123', 'Jl. Merdeka No. 10, Jakarta Selatan', '081234567890', '2025-01-15'),
(2, 'Bunga Citra', 'bunga@example.com', 'hash_pw_bunga456', 'Jl. Diponegoro No. 20, Surabaya Pusat', '081234567891', '2025-02-20'),
(3, 'Cahyo Purnomo', 'cahyo@example.com', 'hash_pw_cahyo789', 'Jl. Asia Afrika No. 30, Bandung Kota', '081234567892', '2025-03-25'),
(4, 'jenar', 'jenar122@gmail.com', 'pbkdf2_sha256$600000$fFurgs7izRanXBFJsPq3rn$lZ54dpOGKmqgtkLom5ldtIsbNL4NlKw/iveWZ++ui40=', 'panekan', '085755323427', '2025-10-31');

-- --------------------------------------------------------

--
-- Table structure for table `pembayaran`
--

CREATE TABLE `pembayaran` (
  `id_pembayaran` int(11) NOT NULL,
  `id_langganan` int(11) NOT NULL,
  `id_metode_bayar` int(11) NOT NULL,
  `jumlah_bayar` decimal(10,2) NOT NULL,
  `tanggal_bayar` datetime NOT NULL,
  `periode_tagihan` date DEFAULT NULL,
  `status_pembayaran` enum('Lunas','Menunggu','Gagal') NOT NULL DEFAULT 'Lunas'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pembayaran`
--

INSERT INTO `pembayaran` (`id_pembayaran`, `id_langganan`, `id_metode_bayar`, `jumlah_bayar`, `tanggal_bayar`, `periode_tagihan`, `status_pembayaran`) VALUES
(1, 1, 1, 250000.00, '2025-02-05 10:30:00', '2025-02-01', 'Lunas'),
(2, 2, 2, 350000.00, '2025-03-04 15:00:00', '2025-03-01', 'Lunas'),
(3, 1, 3, 250000.00, '2025-03-06 08:00:00', '2025-03-01', 'Lunas');

-- --------------------------------------------------------

--
-- Table structure for table `pemesanan_jasa`
--

CREATE TABLE `pemesanan_jasa` (
  `id_pemesanan` int(11) NOT NULL,
  `id_pelanggan` int(11) NOT NULL,
  `id_jenis_jasa` int(11) NOT NULL,
  `id_teknisi` int(11) DEFAULT NULL,
  `tanggal_pemesanan` datetime NOT NULL,
  `tanggal_jadwal` date DEFAULT NULL,
  `status_pemesanan` enum('Baru','Menunggu Penugasan','Ditugaskan','Dikerjakan','Selesai','Batal') NOT NULL DEFAULT 'Menunggu Penugasan',
  `catatan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pemesanan_jasa`
--

INSERT INTO `pemesanan_jasa` (`id_pemesanan`, `id_pelanggan`, `id_jenis_jasa`, `id_teknisi`, `tanggal_pemesanan`, `tanggal_jadwal`, `status_pemesanan`, `catatan`) VALUES
(1, 1, 1, 1, '2025-01-16 09:00:00', '2025-01-20', 'Selesai', 'Instalasi awal pelanggan baru.'),
(2, 2, 2, 2, '2025-05-10 14:30:00', '2025-05-11', 'Selesai', 'Kabel fiber optik putus di area tiang.'),
(3, 1, 3, 1, '2025-06-01 11:00:00', '2025-06-02', 'Dikerjakan', 'Pelanggan minta pasang repeater di lantai 2.');

-- --------------------------------------------------------

--
-- Table structure for table `penempatan_perangkat`
--

CREATE TABLE `penempatan_perangkat` (
  `id_penempatan` int(11) NOT NULL,
  `id_langganan` int(11) NOT NULL,
  `id_perangkat` int(11) NOT NULL,
  `tanggal_pasang` date DEFAULT NULL,
  `status_perangkat` enum('Terpasang','Dicabut','Rusak') DEFAULT 'Terpasang'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `penempatan_perangkat`
--

INSERT INTO `penempatan_perangkat` (`id_penempatan`, `id_langganan`, `id_perangkat`, `tanggal_pasang`, `status_perangkat`) VALUES
(1, 1, 1, '2025-01-20', 'Terpasang'),
(2, 2, 2, '2025-02-25', 'Terpasang'),
(3, 3, 3, '2025-03-30', 'Dicabut');

-- --------------------------------------------------------

--
-- Table structure for table `perangkat`
--

CREATE TABLE `perangkat` (
  `id_perangkat` int(11) NOT NULL,
  `id_jenis_perangkat` int(11) NOT NULL,
  `serial_number` varchar(100) NOT NULL,
  `merk_model` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `perangkat`
--

INSERT INTO `perangkat` (`id_perangkat`, `id_jenis_perangkat`, `serial_number`, `merk_model`) VALUES
(1, 1, 'SN_ROUTER_HW_001', 'Huawei EchoLife HG8245H5'),
(2, 1, 'SN_ROUTER_ZTE_002', 'ZTE F609'),
(3, 2, 'SN_MODEM_TP_003', 'TP-Link TX-6610');

-- --------------------------------------------------------

--
-- Table structure for table `riwayat_testing_wifi`
--

CREATE TABLE `riwayat_testing_wifi` (
  `id_testing` int(11) NOT NULL,
  `id_langganan` int(11) NOT NULL,
  `waktu_testing` datetime NOT NULL,
  `download_speed_mbps` decimal(5,2) DEFAULT NULL,
  `upload_speed_mbps` decimal(5,2) DEFAULT NULL,
  `ping_ms` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `riwayat_testing_wifi`
--

INSERT INTO `riwayat_testing_wifi` (`id_testing`, `id_langganan`, `waktu_testing`, `download_speed_mbps`, `upload_speed_mbps`, `ping_ms`) VALUES
(1, 1, '2025-04-01 08:00:00', 19.80, 4.50, 15),
(2, 2, '2025-04-02 09:00:00', 48.50, 9.20, 8),
(3, 1, '2025-05-01 10:00:00', 20.10, 4.80, 12);

-- --------------------------------------------------------

--
-- Table structure for table `teknisi`
--

CREATE TABLE `teknisi` (
  `id_teknisi` int(11) NOT NULL,
  `nama_teknisi` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role_akses` enum('Teknisi','Admin') NOT NULL DEFAULT 'Teknisi',
  `no_telepon` varchar(15) DEFAULT NULL,
  `id_area_layanan` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teknisi`
--

INSERT INTO `teknisi` (`id_teknisi`, `nama_teknisi`, `username`, `password_hash`, `role_akses`, `no_telepon`, `id_area_layanan`) VALUES
(1, 'Rudi Hartono', 'rudi_teknisi', 'hash_pw_rudi', 'Teknisi', '085111222333', 1),
(2, 'Siti Aminah', 'siti_teknisi', 'hash_pw_siti', 'Teknisi', '085111222444', 2),
(3, 'Doni Saputra', 'doni_admin', 'hash_pw_doni', 'Admin', '085111222555', 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `area_layanan`
--
ALTER TABLE `area_layanan`
  ADD PRIMARY KEY (`id_area_layanan`),
  ADD UNIQUE KEY `nama_area` (`nama_area`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `jenis_jasa`
--
ALTER TABLE `jenis_jasa`
  ADD PRIMARY KEY (`id_jenis_jasa`),
  ADD UNIQUE KEY `nama_jasa` (`nama_jasa`);

--
-- Indexes for table `jenis_perangkat`
--
ALTER TABLE `jenis_perangkat`
  ADD PRIMARY KEY (`id_jenis_perangkat`),
  ADD UNIQUE KEY `nama_jenis` (`nama_jenis`);

--
-- Indexes for table `langganan`
--
ALTER TABLE `langganan`
  ADD PRIMARY KEY (`id_langganan`),
  ADD KEY `id_pelanggan` (`id_pelanggan`),
  ADD KEY `id_paket` (`id_paket`);

--
-- Indexes for table `metode_pembayaran`
--
ALTER TABLE `metode_pembayaran`
  ADD PRIMARY KEY (`id_metode_bayar`),
  ADD UNIQUE KEY `nama_metode` (`nama_metode`);

--
-- Indexes for table `paket_layanan`
--
ALTER TABLE `paket_layanan`
  ADD PRIMARY KEY (`id_paket`),
  ADD UNIQUE KEY `nama_paket` (`nama_paket`);

--
-- Indexes for table `pelanggan`
--
ALTER TABLE `pelanggan`
  ADD PRIMARY KEY (`id_pelanggan`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `pembayaran`
--
ALTER TABLE `pembayaran`
  ADD PRIMARY KEY (`id_pembayaran`),
  ADD KEY `id_langganan` (`id_langganan`),
  ADD KEY `id_metode_bayar` (`id_metode_bayar`);

--
-- Indexes for table `pemesanan_jasa`
--
ALTER TABLE `pemesanan_jasa`
  ADD PRIMARY KEY (`id_pemesanan`),
  ADD KEY `id_pelanggan` (`id_pelanggan`),
  ADD KEY `id_jenis_jasa` (`id_jenis_jasa`),
  ADD KEY `id_teknisi` (`id_teknisi`);

--
-- Indexes for table `penempatan_perangkat`
--
ALTER TABLE `penempatan_perangkat`
  ADD PRIMARY KEY (`id_penempatan`),
  ADD UNIQUE KEY `uk_perangkat_langganan` (`id_perangkat`,`id_langganan`),
  ADD KEY `id_langganan` (`id_langganan`);

--
-- Indexes for table `perangkat`
--
ALTER TABLE `perangkat`
  ADD PRIMARY KEY (`id_perangkat`),
  ADD UNIQUE KEY `serial_number` (`serial_number`),
  ADD KEY `id_jenis_perangkat` (`id_jenis_perangkat`);

--
-- Indexes for table `riwayat_testing_wifi`
--
ALTER TABLE `riwayat_testing_wifi`
  ADD PRIMARY KEY (`id_testing`),
  ADD KEY `id_langganan` (`id_langganan`);

--
-- Indexes for table `teknisi`
--
ALTER TABLE `teknisi`
  ADD PRIMARY KEY (`id_teknisi`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `id_area_layanan` (`id_area_layanan`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `area_layanan`
--
ALTER TABLE `area_layanan`
  MODIFY `id_area_layanan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=129;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `jenis_jasa`
--
ALTER TABLE `jenis_jasa`
  MODIFY `id_jenis_jasa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `jenis_perangkat`
--
ALTER TABLE `jenis_perangkat`
  MODIFY `id_jenis_perangkat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `langganan`
--
ALTER TABLE `langganan`
  MODIFY `id_langganan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `metode_pembayaran`
--
ALTER TABLE `metode_pembayaran`
  MODIFY `id_metode_bayar` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `paket_layanan`
--
ALTER TABLE `paket_layanan`
  MODIFY `id_paket` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `pelanggan`
--
ALTER TABLE `pelanggan`
  MODIFY `id_pelanggan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `pembayaran`
--
ALTER TABLE `pembayaran`
  MODIFY `id_pembayaran` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `pemesanan_jasa`
--
ALTER TABLE `pemesanan_jasa`
  MODIFY `id_pemesanan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `penempatan_perangkat`
--
ALTER TABLE `penempatan_perangkat`
  MODIFY `id_penempatan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `perangkat`
--
ALTER TABLE `perangkat`
  MODIFY `id_perangkat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `riwayat_testing_wifi`
--
ALTER TABLE `riwayat_testing_wifi`
  MODIFY `id_testing` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `teknisi`
--
ALTER TABLE `teknisi`
  MODIFY `id_teknisi` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `langganan`
--
ALTER TABLE `langganan`
  ADD CONSTRAINT `langganan_ibfk_1` FOREIGN KEY (`id_pelanggan`) REFERENCES `pelanggan` (`id_pelanggan`),
  ADD CONSTRAINT `langganan_ibfk_2` FOREIGN KEY (`id_paket`) REFERENCES `paket_layanan` (`id_paket`);

--
-- Constraints for table `pembayaran`
--
ALTER TABLE `pembayaran`
  ADD CONSTRAINT `pembayaran_ibfk_1` FOREIGN KEY (`id_langganan`) REFERENCES `langganan` (`id_langganan`),
  ADD CONSTRAINT `pembayaran_ibfk_2` FOREIGN KEY (`id_metode_bayar`) REFERENCES `metode_pembayaran` (`id_metode_bayar`);

--
-- Constraints for table `pemesanan_jasa`
--
ALTER TABLE `pemesanan_jasa`
  ADD CONSTRAINT `pemesanan_jasa_ibfk_1` FOREIGN KEY (`id_pelanggan`) REFERENCES `pelanggan` (`id_pelanggan`),
  ADD CONSTRAINT `pemesanan_jasa_ibfk_2` FOREIGN KEY (`id_jenis_jasa`) REFERENCES `jenis_jasa` (`id_jenis_jasa`),
  ADD CONSTRAINT `pemesanan_jasa_ibfk_3` FOREIGN KEY (`id_teknisi`) REFERENCES `teknisi` (`id_teknisi`);

--
-- Constraints for table `penempatan_perangkat`
--
ALTER TABLE `penempatan_perangkat`
  ADD CONSTRAINT `penempatan_perangkat_ibfk_1` FOREIGN KEY (`id_langganan`) REFERENCES `langganan` (`id_langganan`),
  ADD CONSTRAINT `penempatan_perangkat_ibfk_2` FOREIGN KEY (`id_perangkat`) REFERENCES `perangkat` (`id_perangkat`);

--
-- Constraints for table `perangkat`
--
ALTER TABLE `perangkat`
  ADD CONSTRAINT `perangkat_ibfk_1` FOREIGN KEY (`id_jenis_perangkat`) REFERENCES `jenis_perangkat` (`id_jenis_perangkat`);

--
-- Constraints for table `riwayat_testing_wifi`
--
ALTER TABLE `riwayat_testing_wifi`
  ADD CONSTRAINT `riwayat_testing_wifi_ibfk_1` FOREIGN KEY (`id_langganan`) REFERENCES `langganan` (`id_langganan`);

--
-- Constraints for table `teknisi`
--
ALTER TABLE `teknisi`
  ADD CONSTRAINT `teknisi_ibfk_1` FOREIGN KEY (`id_area_layanan`) REFERENCES `area_layanan` (`id_area_layanan`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
