-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Waktu pembuatan: 02 Sep 2023 pada 17.23
-- Versi server: 8.0.33-0ubuntu0.22.04.4
-- Versi PHP: 8.1.2-1ubuntu2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sic-biona`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_payment`
--

CREATE TABLE `tb_payment` (
  `id_payment` int NOT NULL,
  `method` varchar(200) NOT NULL,
  `logo` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `tb_payment`
--

INSERT INTO `tb_payment` (`id_payment`, `method`, `logo`) VALUES
(1, 'GOPAY', 'gopay.png'),
(2, 'BCA', 'bca.png'),
(3, 'MANDIRI', 'MANDIRI.png\r\n');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_transaksi`
--

CREATE TABLE `tb_transaksi` (
  `id_transaksi` int NOT NULL,
  `email` varchar(200) NOT NULL,
  `payment` varchar(200) NOT NULL,
  `no_payment` int NOT NULL,
  `nominal` int NOT NULL,
  `tanggal_transaksi` datetime DEFAULT NULL,
  `status` varchar(200) NOT NULL,
  `bukti_pembayaran` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `tb_transaksi`
--

INSERT INTO `tb_transaksi` (`id_transaksi`, `email`, `payment`, `no_payment`, `nominal`, `tanggal_transaksi`, `status`, `bukti_pembayaran`) VALUES
(23, 'cahyosaputrorahmadi@gmail.com', 'GOPAY', 817718181, 12883, '2023-09-01 11:15:00', 'PAID', '<FileStorage: \'MANDIRI.png\' (\'image/png\')>'),
(24, 'cahyosaputrorahmadi@gmail.com', 'GOPAY', 817718181, 829237, '2023-09-02 11:58:52', 'PAID', '<FileStorage: \'gopay.png\' (\'image/png\')>');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_users`
--

CREATE TABLE `tb_users` (
  `id` int NOT NULL,
  `email` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `role` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `saldo` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tb_users`
--

INSERT INTO `tb_users` (`id`, `email`, `username`, `password`, `role`, `saldo`) VALUES
(8, 'biona226@gmail.com', 'Admin\r\n', '$2b$12$n2677u1Uy7mFKneho/BF6uvCDtSAsugUG3rgKd8oMKw6zvenjiDPK', 'ADMIN', 0),
(9, 'cahyosaputrorahmadi@gmail.com', 'Rahmadi', '$2b$12$RMMfP/Fmx0ygZvY.11Y7KuCgZSnAFZ87OyRs6SjnLS3IDu05RXJcS', 'user', 0),
(10, 'biona@gmail.com', 'Biona ', '$2b$12$Ny9wmBKzVhBA4HTUEELQ5uwjfycnjIke8NF.Z4cHz1feAWIurL2VC', 'user', 0),
(11, 'raihan@gmail.com', 'raihani1', '$2b$12$Xm/7yTgAFizH/Hxm7ht.MOnu43I9LxwCaDRjeQr9ursyQ3.LcbqgC', 'user', 0);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tb_payment`
--
ALTER TABLE `tb_payment`
  ADD PRIMARY KEY (`id_payment`);

--
-- Indeks untuk tabel `tb_transaksi`
--
ALTER TABLE `tb_transaksi`
  ADD PRIMARY KEY (`id_transaksi`);

--
-- Indeks untuk tabel `tb_users`
--
ALTER TABLE `tb_users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `tb_payment`
--
ALTER TABLE `tb_payment`
  MODIFY `id_payment` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `tb_transaksi`
--
ALTER TABLE `tb_transaksi`
  MODIFY `id_transaksi` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT untuk tabel `tb_users`
--
ALTER TABLE `tb_users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
