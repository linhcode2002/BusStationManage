/*
 Navicat Premium Data Transfer

 Source Server         : busapp
 Source Server Type    : MySQL
 Source Server Version : 80200
 Source Host           : localhost:3307
 Source Schema         : bus_manage

 Target Server Type    : MySQL
 Target Server Version : 80200
 File Encoding         : 65001

 Date: 06/10/2024 20:49:32
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 101 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO `auth_permission` VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO `auth_permission` VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO `auth_permission` VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO `auth_permission` VALUES (21, 'Can add bus', 6, 'add_bus');
INSERT INTO `auth_permission` VALUES (22, 'Can change bus', 6, 'change_bus');
INSERT INTO `auth_permission` VALUES (23, 'Can delete bus', 6, 'delete_bus');
INSERT INTO `auth_permission` VALUES (24, 'Can view bus', 6, 'view_bus');
INSERT INTO `auth_permission` VALUES (25, 'Can add revenue statistics', 7, 'add_revenuestatistics');
INSERT INTO `auth_permission` VALUES (26, 'Can change revenue statistics', 7, 'change_revenuestatistics');
INSERT INTO `auth_permission` VALUES (27, 'Can delete revenue statistics', 7, 'delete_revenuestatistics');
INSERT INTO `auth_permission` VALUES (28, 'Can view revenue statistics', 7, 'view_revenuestatistics');
INSERT INTO `auth_permission` VALUES (29, 'Can add review', 8, 'add_review');
INSERT INTO `auth_permission` VALUES (30, 'Can change review', 8, 'change_review');
INSERT INTO `auth_permission` VALUES (31, 'Can delete review', 8, 'delete_review');
INSERT INTO `auth_permission` VALUES (32, 'Can view review', 8, 'view_review');
INSERT INTO `auth_permission` VALUES (33, 'Can add bus route', 9, 'add_busroute');
INSERT INTO `auth_permission` VALUES (34, 'Can change bus route', 9, 'change_busroute');
INSERT INTO `auth_permission` VALUES (35, 'Can delete bus route', 9, 'delete_busroute');
INSERT INTO `auth_permission` VALUES (36, 'Can view bus route', 9, 'view_busroute');
INSERT INTO `auth_permission` VALUES (37, 'Can add seat', 10, 'add_seat');
INSERT INTO `auth_permission` VALUES (38, 'Can change seat', 10, 'change_seat');
INSERT INTO `auth_permission` VALUES (39, 'Can delete seat', 10, 'delete_seat');
INSERT INTO `auth_permission` VALUES (40, 'Can view seat', 10, 'view_seat');
INSERT INTO `auth_permission` VALUES (41, 'Can add trip', 11, 'add_trip');
INSERT INTO `auth_permission` VALUES (42, 'Can change trip', 11, 'change_trip');
INSERT INTO `auth_permission` VALUES (43, 'Can delete trip', 11, 'delete_trip');
INSERT INTO `auth_permission` VALUES (44, 'Can view trip', 11, 'view_trip');
INSERT INTO `auth_permission` VALUES (45, 'Can add booking', 12, 'add_booking');
INSERT INTO `auth_permission` VALUES (46, 'Can change booking', 12, 'change_booking');
INSERT INTO `auth_permission` VALUES (47, 'Can delete booking', 12, 'delete_booking');
INSERT INTO `auth_permission` VALUES (48, 'Can view booking', 12, 'view_booking');
INSERT INTO `auth_permission` VALUES (49, 'Can add trip statistics', 13, 'add_tripstatistics');
INSERT INTO `auth_permission` VALUES (50, 'Can change trip statistics', 13, 'change_tripstatistics');
INSERT INTO `auth_permission` VALUES (51, 'Can delete trip statistics', 13, 'delete_tripstatistics');
INSERT INTO `auth_permission` VALUES (52, 'Can view trip statistics', 13, 'view_tripstatistics');
INSERT INTO `auth_permission` VALUES (53, 'Can add user', 14, 'add_user');
INSERT INTO `auth_permission` VALUES (54, 'Can change user', 14, 'change_user');
INSERT INTO `auth_permission` VALUES (55, 'Can delete user', 14, 'delete_user');
INSERT INTO `auth_permission` VALUES (56, 'Can view user', 14, 'view_user');
INSERT INTO `auth_permission` VALUES (57, 'Can add customer', 15, 'add_customer');
INSERT INTO `auth_permission` VALUES (58, 'Can change customer', 15, 'change_customer');
INSERT INTO `auth_permission` VALUES (59, 'Can delete customer', 15, 'delete_customer');
INSERT INTO `auth_permission` VALUES (60, 'Can view customer', 15, 'view_customer');
INSERT INTO `auth_permission` VALUES (61, 'Can add application', 16, 'add_application');
INSERT INTO `auth_permission` VALUES (62, 'Can change application', 16, 'change_application');
INSERT INTO `auth_permission` VALUES (63, 'Can delete application', 16, 'delete_application');
INSERT INTO `auth_permission` VALUES (64, 'Can view application', 16, 'view_application');
INSERT INTO `auth_permission` VALUES (65, 'Can add access token', 17, 'add_accesstoken');
INSERT INTO `auth_permission` VALUES (66, 'Can change access token', 17, 'change_accesstoken');
INSERT INTO `auth_permission` VALUES (67, 'Can delete access token', 17, 'delete_accesstoken');
INSERT INTO `auth_permission` VALUES (68, 'Can view access token', 17, 'view_accesstoken');
INSERT INTO `auth_permission` VALUES (69, 'Can add grant', 18, 'add_grant');
INSERT INTO `auth_permission` VALUES (70, 'Can change grant', 18, 'change_grant');
INSERT INTO `auth_permission` VALUES (71, 'Can delete grant', 18, 'delete_grant');
INSERT INTO `auth_permission` VALUES (72, 'Can view grant', 18, 'view_grant');
INSERT INTO `auth_permission` VALUES (73, 'Can add refresh token', 19, 'add_refreshtoken');
INSERT INTO `auth_permission` VALUES (74, 'Can change refresh token', 19, 'change_refreshtoken');
INSERT INTO `auth_permission` VALUES (75, 'Can delete refresh token', 19, 'delete_refreshtoken');
INSERT INTO `auth_permission` VALUES (76, 'Can view refresh token', 19, 'view_refreshtoken');
INSERT INTO `auth_permission` VALUES (77, 'Can add id token', 20, 'add_idtoken');
INSERT INTO `auth_permission` VALUES (78, 'Can change id token', 20, 'change_idtoken');
INSERT INTO `auth_permission` VALUES (79, 'Can delete id token', 20, 'delete_idtoken');
INSERT INTO `auth_permission` VALUES (80, 'Can view id token', 20, 'view_idtoken');
INSERT INTO `auth_permission` VALUES (81, 'Can add association', 21, 'add_association');
INSERT INTO `auth_permission` VALUES (82, 'Can change association', 21, 'change_association');
INSERT INTO `auth_permission` VALUES (83, 'Can delete association', 21, 'delete_association');
INSERT INTO `auth_permission` VALUES (84, 'Can view association', 21, 'view_association');
INSERT INTO `auth_permission` VALUES (85, 'Can add code', 22, 'add_code');
INSERT INTO `auth_permission` VALUES (86, 'Can change code', 22, 'change_code');
INSERT INTO `auth_permission` VALUES (87, 'Can delete code', 22, 'delete_code');
INSERT INTO `auth_permission` VALUES (88, 'Can view code', 22, 'view_code');
INSERT INTO `auth_permission` VALUES (89, 'Can add nonce', 23, 'add_nonce');
INSERT INTO `auth_permission` VALUES (90, 'Can change nonce', 23, 'change_nonce');
INSERT INTO `auth_permission` VALUES (91, 'Can delete nonce', 23, 'delete_nonce');
INSERT INTO `auth_permission` VALUES (92, 'Can view nonce', 23, 'view_nonce');
INSERT INTO `auth_permission` VALUES (93, 'Can add user social auth', 24, 'add_usersocialauth');
INSERT INTO `auth_permission` VALUES (94, 'Can change user social auth', 24, 'change_usersocialauth');
INSERT INTO `auth_permission` VALUES (95, 'Can delete user social auth', 24, 'delete_usersocialauth');
INSERT INTO `auth_permission` VALUES (96, 'Can view user social auth', 24, 'view_usersocialauth');
INSERT INTO `auth_permission` VALUES (97, 'Can add partial', 25, 'add_partial');
INSERT INTO `auth_permission` VALUES (98, 'Can change partial', 25, 'change_partial');
INSERT INTO `auth_permission` VALUES (99, 'Can delete partial', 25, 'delete_partial');
INSERT INTO `auth_permission` VALUES (100, 'Can view partial', 25, 'view_partial');

-- ----------------------------
-- Table structure for busmanage_booking
-- ----------------------------
DROP TABLE IF EXISTS `busmanage_booking`;
CREATE TABLE `busmanage_booking`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `created_date` datetime(6) NULL DEFAULT NULL,
  `updated_date` datetime(6) NULL DEFAULT NULL,
  `customer_email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `customer_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `customer_phone` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `booking_time` datetime(6) NULL DEFAULT NULL,
  `seat_id` bigint NOT NULL,
  `trip_id` bigint NOT NULL,
  `ticket_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_trip_seat_email`(`trip_id` ASC, `seat_id` ASC, `customer_email` ASC) USING BTREE,
  UNIQUE INDEX `ticket_code`(`ticket_code` ASC) USING BTREE,
  INDEX `BusManage_booking_seat_id_ca43b02a_fk_BusManage_seat_id`(`seat_id` ASC) USING BTREE,
  CONSTRAINT `BusManage_booking_seat_id_ca43b02a_fk_BusManage_seat_id` FOREIGN KEY (`seat_id`) REFERENCES `busmanage_seat` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `BusManage_booking_trip_id_55fd5808_fk_BusManage_trip_id` FOREIGN KEY (`trip_id`) REFERENCES `busmanage_trip` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of busmanage_booking
-- ----------------------------
INSERT INTO `busmanage_booking` VALUES (7, 1, '2024-10-02 15:39:53.585722', '2024-10-02 15:39:53.585722', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-02 15:39:53.585722', 36, 1, '7V8461');
INSERT INTO `busmanage_booking` VALUES (8, 1, '2024-10-02 15:55:58.488007', '2024-10-02 15:55:58.488007', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-02 15:55:58.488007', 29, 1, 'OB552M');
INSERT INTO `busmanage_booking` VALUES (9, 1, '2024-10-02 15:55:58.495872', '2024-10-02 15:55:58.495872', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-02 15:55:58.495872', 30, 1, 'EXKC3T');
INSERT INTO `busmanage_booking` VALUES (10, 1, '2024-10-02 16:08:21.317960', '2024-10-02 16:08:21.317960', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-02 16:08:21.317960', 34, 1, '84K9SH');
INSERT INTO `busmanage_booking` VALUES (11, 1, '2024-10-02 16:15:12.958430', '2024-10-02 16:15:12.958430', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-02 16:15:12.958430', 33, 1, 'H3K1HP');
INSERT INTO `busmanage_booking` VALUES (12, 1, '2024-10-02 16:15:12.975053', '2024-10-02 16:15:12.975053', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-02 16:15:12.975053', 32, 1, 'EDEDYX');
INSERT INTO `busmanage_booking` VALUES (13, 1, '2024-10-02 16:24:48.833516', '2024-10-02 16:24:48.833516', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-02 16:24:48.833516', 14, 1, 'XFIXSB');
INSERT INTO `busmanage_booking` VALUES (14, 1, '2024-10-02 16:29:17.605737', '2024-10-02 16:29:17.605737', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-02 16:29:17.605737', 35, 1, 'C0E7R3');
INSERT INTO `busmanage_booking` VALUES (15, 1, '2024-10-02 16:30:56.524336', '2024-10-02 16:30:56.524336', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-02 16:30:56.524336', 31, 1, 'LOB796');
INSERT INTO `busmanage_booking` VALUES (16, 1, '2024-10-05 16:09:26.427294', '2024-10-05 16:09:26.427294', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-05 16:09:26.427294', 8, 3, 'GQZ56E');
INSERT INTO `busmanage_booking` VALUES (17, 1, '2024-10-05 16:09:26.443822', '2024-10-05 16:09:26.443822', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-05 16:09:26.443822', 9, 3, 'VJL62F');
INSERT INTO `busmanage_booking` VALUES (18, 1, '2024-10-05 16:15:34.007890', '2024-10-05 16:15:34.007890', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-05 16:15:34.007890', 28, 3, 'F2EULH');
INSERT INTO `busmanage_booking` VALUES (19, 1, '2024-10-05 16:15:34.023659', '2024-10-05 16:15:34.023659', 'linhho.linhcangfc@gmail.com', 'Hồ Văn Lĩnh', '0974376442', '2024-10-05 16:15:34.023659', 34, 3, 'AEUW90');

-- ----------------------------
-- Table structure for busmanage_bus
-- ----------------------------
DROP TABLE IF EXISTS `busmanage_bus`;
CREATE TABLE `busmanage_bus`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `created_date` datetime(6) NULL DEFAULT NULL,
  `updated_date` datetime(6) NULL DEFAULT NULL,
  `license_plate` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_seats` int NOT NULL,
  `driver` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of busmanage_bus
-- ----------------------------
INSERT INTO `busmanage_bus` VALUES (1, 1, '2024-10-02 11:29:29.499356', '2024-10-02 11:29:29.499356', '92H1 - 00805', 36, 'Hồ Văn Lĩnh');

-- ----------------------------
-- Table structure for busmanage_busroute
-- ----------------------------
DROP TABLE IF EXISTS `busmanage_busroute`;
CREATE TABLE `busmanage_busroute`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `created_date` datetime(6) NULL DEFAULT NULL,
  `updated_date` datetime(6) NULL DEFAULT NULL,
  `route_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `end_location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `distance` decimal(5, 0) NOT NULL,
  `bus_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `BusManage_busroute_bus_id_65625540_fk_BusManage_bus_id`(`bus_id` ASC) USING BTREE,
  CONSTRAINT `BusManage_busroute_bus_id_65625540_fk_BusManage_bus_id` FOREIGN KEY (`bus_id`) REFERENCES `busmanage_bus` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of busmanage_busroute
-- ----------------------------
INSERT INTO `busmanage_busroute` VALUES (1, 1, '2024-10-02 11:29:31.049263', '2024-10-02 11:29:31.049263', 'Quảng Nam - Quãng Ngãi', 'Quảng Nam', 'Quãng Ngãi', 80, 1);
INSERT INTO `busmanage_busroute` VALUES (2, 1, '2024-10-05 16:36:33.049029', '2024-10-05 16:36:33.049029', 'Đà Nẵng - Hà Nội', 'Đà Nẵng', 'Hà Nội', 900, 1);

-- ----------------------------
-- Table structure for busmanage_customer
-- ----------------------------
DROP TABLE IF EXISTS `busmanage_customer`;
CREATE TABLE `busmanage_customer`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `created_date` datetime(6) NULL DEFAULT NULL,
  `updated_date` datetime(6) NULL DEFAULT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `phone_number` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of busmanage_customer
-- ----------------------------
INSERT INTO `busmanage_customer` VALUES (1, 1, '2024-10-05 16:42:22.905143', '2024-10-05 16:43:00.684045', 'Hồ Văn Lĩnh', '0974376442', 'linhho.linhcangfc@gmail.com', 'Quảng Nam', 'image/upload/v1728146583/CustomerAvatars/llzgkqhzczvnkqxyp381.jpg', 'pbkdf2_sha256$720000$w5h2ipaK4rPxCnMOXEobo9$msSjG+ySHBpzr65Y5otquhoch0FjTIYTVoPeMEd+RLs=');

-- ----------------------------
-- Table structure for busmanage_revenuestatistics
-- ----------------------------
DROP TABLE IF EXISTS `busmanage_revenuestatistics`;
CREATE TABLE `busmanage_revenuestatistics`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `created_date` datetime(6) NULL DEFAULT NULL,
  `updated_date` datetime(6) NULL DEFAULT NULL,
  `month` int NOT NULL,
  `year` int NOT NULL,
  `revenue` decimal(15, 2) NOT NULL,
  `frequency` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of busmanage_revenuestatistics
-- ----------------------------

-- ----------------------------
-- Table structure for busmanage_review
-- ----------------------------
DROP TABLE IF EXISTS `busmanage_review`;
CREATE TABLE `busmanage_review`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `created_date` datetime(6) NULL DEFAULT NULL,
  `updated_date` datetime(6) NULL DEFAULT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `customer_email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_number` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of busmanage_review
-- ----------------------------

-- ----------------------------
-- Table structure for busmanage_seat
-- ----------------------------
DROP TABLE IF EXISTS `busmanage_seat`;
CREATE TABLE `busmanage_seat`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `created_date` datetime(6) NULL DEFAULT NULL,
  `updated_date` datetime(6) NULL DEFAULT NULL,
  `name` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `bus_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE,
  INDEX `BusManage_seat_bus_id_f04da555_fk_BusManage_bus_id`(`bus_id` ASC) USING BTREE,
  CONSTRAINT `BusManage_seat_bus_id_f04da555_fk_BusManage_bus_id` FOREIGN KEY (`bus_id`) REFERENCES `busmanage_bus` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 37 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of busmanage_seat
-- ----------------------------
INSERT INTO `busmanage_seat` VALUES (1, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A01', 1);
INSERT INTO `busmanage_seat` VALUES (2, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A02', 1);
INSERT INTO `busmanage_seat` VALUES (3, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A03', 1);
INSERT INTO `busmanage_seat` VALUES (4, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B01', 1);
INSERT INTO `busmanage_seat` VALUES (5, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B02', 1);
INSERT INTO `busmanage_seat` VALUES (6, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B03', 1);
INSERT INTO `busmanage_seat` VALUES (7, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A04', 1);
INSERT INTO `busmanage_seat` VALUES (8, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A05', 1);
INSERT INTO `busmanage_seat` VALUES (9, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A06', 1);
INSERT INTO `busmanage_seat` VALUES (10, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B04', 1);
INSERT INTO `busmanage_seat` VALUES (11, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B05', 1);
INSERT INTO `busmanage_seat` VALUES (12, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B06', 1);
INSERT INTO `busmanage_seat` VALUES (13, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A07', 1);
INSERT INTO `busmanage_seat` VALUES (14, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A08', 1);
INSERT INTO `busmanage_seat` VALUES (15, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B07', 1);
INSERT INTO `busmanage_seat` VALUES (16, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B08', 1);
INSERT INTO `busmanage_seat` VALUES (17, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B09', 1);
INSERT INTO `busmanage_seat` VALUES (18, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A09', 1);
INSERT INTO `busmanage_seat` VALUES (19, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A10', 1);
INSERT INTO `busmanage_seat` VALUES (20, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A11', 1);
INSERT INTO `busmanage_seat` VALUES (21, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A12', 1);
INSERT INTO `busmanage_seat` VALUES (22, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B10', 1);
INSERT INTO `busmanage_seat` VALUES (23, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B11', 1);
INSERT INTO `busmanage_seat` VALUES (24, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B12', 1);
INSERT INTO `busmanage_seat` VALUES (25, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A13', 1);
INSERT INTO `busmanage_seat` VALUES (26, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A14', 1);
INSERT INTO `busmanage_seat` VALUES (27, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B13', 1);
INSERT INTO `busmanage_seat` VALUES (28, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B14', 1);
INSERT INTO `busmanage_seat` VALUES (29, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B15', 1);
INSERT INTO `busmanage_seat` VALUES (30, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A15', 1);
INSERT INTO `busmanage_seat` VALUES (31, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A16', 1);
INSERT INTO `busmanage_seat` VALUES (32, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A17', 1);
INSERT INTO `busmanage_seat` VALUES (33, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'A18', 1);
INSERT INTO `busmanage_seat` VALUES (34, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B16', 1);
INSERT INTO `busmanage_seat` VALUES (35, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B17', 1);
INSERT INTO `busmanage_seat` VALUES (36, 1, '2024-10-02 18:32:42.000000', '2024-10-02 18:32:42.000000', 'B18', 1);

-- ----------------------------
-- Table structure for busmanage_trip
-- ----------------------------
DROP TABLE IF EXISTS `busmanage_trip`;
CREATE TABLE `busmanage_trip`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `created_date` datetime(6) NULL DEFAULT NULL,
  `updated_date` datetime(6) NULL DEFAULT NULL,
  `departure_time` datetime(6) NOT NULL,
  `arrival_time` datetime(6) NOT NULL,
  `ticket_price` decimal(10, 0) NOT NULL,
  `bus_route_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `BusManage_trip_bus_route_id_5a62ba9b_fk_BusManage_busroute_id`(`bus_route_id` ASC) USING BTREE,
  CONSTRAINT `BusManage_trip_bus_route_id_5a62ba9b_fk_BusManage_busroute_id` FOREIGN KEY (`bus_route_id`) REFERENCES `busmanage_busroute` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of busmanage_trip
-- ----------------------------
INSERT INTO `busmanage_trip` VALUES (1, 1, '2024-10-02 11:30:13.822833', '2024-10-02 11:30:13.822833', '2024-10-05 01:30:00.000000', '2024-10-05 08:30:00.000000', 100000, 1);
INSERT INTO `busmanage_trip` VALUES (2, 1, '2024-10-05 16:02:53.474955', '2024-10-05 16:02:53.474955', '2024-10-09 16:02:14.000000', '2024-10-09 18:02:32.000000', 100000, 1);
INSERT INTO `busmanage_trip` VALUES (3, 1, '2024-10-05 16:04:13.075784', '2024-10-05 16:36:45.802133', '2024-10-09 09:03:41.000000', '2024-10-09 16:04:04.000000', 100000, 2);

-- ----------------------------
-- Table structure for busmanage_tripstatistics
-- ----------------------------
DROP TABLE IF EXISTS `busmanage_tripstatistics`;
CREATE TABLE `busmanage_tripstatistics`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `created_date` datetime(6) NULL DEFAULT NULL,
  `updated_date` datetime(6) NULL DEFAULT NULL,
  `total_tickets` int NOT NULL,
  `booked_tickets` int NOT NULL,
  `total_payment` decimal(12, 0) NOT NULL,
  `trip_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `trip_id`(`trip_id` ASC) USING BTREE,
  CONSTRAINT `BusManage_tripstatistics_trip_id_ee2f8a14_fk_BusManage_trip_id` FOREIGN KEY (`trip_id`) REFERENCES `busmanage_trip` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of busmanage_tripstatistics
-- ----------------------------
INSERT INTO `busmanage_tripstatistics` VALUES (1, 1, '2024-10-02 11:33:08.677006', '2024-10-02 16:30:56.532466', 0, 15, 1500000, 1);
INSERT INTO `busmanage_tripstatistics` VALUES (2, 1, '2024-10-05 16:09:26.435093', '2024-10-05 16:15:34.031962', 0, 4, 400000, 3);

-- ----------------------------
-- Table structure for busmanage_user
-- ----------------------------
DROP TABLE IF EXISTS `busmanage_user`;
CREATE TABLE `busmanage_user`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of busmanage_user
-- ----------------------------
INSERT INTO `busmanage_user` VALUES (1, 'pbkdf2_sha256$720000$2VGCbY1CyqR45hXRUz62VR$SrbzQBTxAme+zBLnX67TXu8o1c0e7IuU95Y0OSauLMc=', '2024-10-02 11:29:04.000000', 1, 'admin', '', '', 'abc@gmail.com', 1, 1, '2024-10-02 11:28:54.000000', 'image/upload/v1728146829/avatars/tg5x5knkecjqvx743evx.jpg');

-- ----------------------------
-- Table structure for busmanage_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `busmanage_user_groups`;
CREATE TABLE `busmanage_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `BusManage_user_groups_user_id_group_id_8bb972d4_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `BusManage_user_groups_group_id_f8fe3e24_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `BusManage_user_groups_group_id_f8fe3e24_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `BusManage_user_groups_user_id_45301892_fk_BusManage_user_id` FOREIGN KEY (`user_id`) REFERENCES `busmanage_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of busmanage_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for busmanage_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `busmanage_user_user_permissions`;
CREATE TABLE `busmanage_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `BusManage_user_user_perm_user_id_permission_id_7dba85f1_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `BusManage_user_user__permission_id_251e9535_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `BusManage_user_user__permission_id_251e9535_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `BusManage_user_user__user_id_c86d6e8f_fk_BusManage` FOREIGN KEY (`user_id`) REFERENCES `busmanage_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of busmanage_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_BusManage_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_BusManage_user_id` FOREIGN KEY (`user_id`) REFERENCES `busmanage_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
INSERT INTO `django_admin_log` VALUES (1, '2024-10-02 11:29:29.499356', '1', '92H1 - 00805', 1, '[{\"added\": {}}]', 6, 1);
INSERT INTO `django_admin_log` VALUES (2, '2024-10-02 11:29:31.049263', '1', 'Quảng Nam - Quãng Ngãi', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (3, '2024-10-02 11:30:13.822833', '1', 'Quảng Nam - Quãng Ngãi - 2024-10-05 08:30:00+07:00', 1, '[{\"added\": {}}]', 11, 1);
INSERT INTO `django_admin_log` VALUES (4, '2024-10-02 15:56:39.337069', '6', 'Booking for Hồ Văn Lĩnh - Seat B09 (Quảng Nam - Quãng Ngãi)', 3, '', 12, 1);
INSERT INTO `django_admin_log` VALUES (5, '2024-10-02 15:56:39.354891', '5', 'Booking for Hồ Văn Lĩnh - Seat B08 (Quảng Nam - Quãng Ngãi)', 3, '', 12, 1);
INSERT INTO `django_admin_log` VALUES (6, '2024-10-02 15:56:39.354891', '4', 'Booking for Hồ Văn Lĩnh - Seat B17 (Quảng Nam - Quãng Ngãi)', 3, '', 12, 1);
INSERT INTO `django_admin_log` VALUES (7, '2024-10-02 15:56:39.354891', '3', 'Booking for Hồ Văn Lĩnh - Seat B16 (Quảng Nam - Quãng Ngãi)', 3, '', 12, 1);
INSERT INTO `django_admin_log` VALUES (8, '2024-10-02 15:56:39.363050', '2', 'Booking for Hồ Văn Lĩnh - Seat A18 (Quảng Nam - Quãng Ngãi)', 3, '', 12, 1);
INSERT INTO `django_admin_log` VALUES (9, '2024-10-02 15:56:39.363050', '1', 'Booking for Hồ Văn Lĩnh - Seat A17 (Quảng Nam - Quãng Ngãi)', 3, '', 12, 1);
INSERT INTO `django_admin_log` VALUES (10, '2024-10-05 16:02:53.491964', '2', 'Quảng Nam - Quãng Ngãi - 2024-10-09 23:02:14+07:00', 1, '[{\"added\": {}}]', 11, 1);
INSERT INTO `django_admin_log` VALUES (11, '2024-10-05 16:04:13.083027', '3', 'Quảng Nam - Quãng Ngãi - 2024-10-09 16:03:41+07:00', 1, '[{\"added\": {}}]', 11, 1);
INSERT INTO `django_admin_log` VALUES (12, '2024-10-05 16:36:33.049029', '2', 'Đà Nẵng - Hà Nội', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (13, '2024-10-05 16:36:45.802133', '3', 'Đà Nẵng - Hà Nội - 2024-10-09 16:03:41+07:00', 2, '[{\"changed\": {\"fields\": [\"Bus route\"]}}]', 11, 1);
INSERT INTO `django_admin_log` VALUES (14, '2024-10-05 16:47:11.562914', '1', 'admin', 2, '[{\"changed\": {\"fields\": [\"Avatar\"]}}]', 14, 1);

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (12, 'BusManage', 'booking');
INSERT INTO `django_content_type` VALUES (6, 'BusManage', 'bus');
INSERT INTO `django_content_type` VALUES (9, 'BusManage', 'busroute');
INSERT INTO `django_content_type` VALUES (15, 'BusManage', 'customer');
INSERT INTO `django_content_type` VALUES (7, 'BusManage', 'revenuestatistics');
INSERT INTO `django_content_type` VALUES (8, 'BusManage', 'review');
INSERT INTO `django_content_type` VALUES (10, 'BusManage', 'seat');
INSERT INTO `django_content_type` VALUES (11, 'BusManage', 'trip');
INSERT INTO `django_content_type` VALUES (13, 'BusManage', 'tripstatistics');
INSERT INTO `django_content_type` VALUES (14, 'BusManage', 'user');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (17, 'oauth2_provider', 'accesstoken');
INSERT INTO `django_content_type` VALUES (16, 'oauth2_provider', 'application');
INSERT INTO `django_content_type` VALUES (18, 'oauth2_provider', 'grant');
INSERT INTO `django_content_type` VALUES (20, 'oauth2_provider', 'idtoken');
INSERT INTO `django_content_type` VALUES (19, 'oauth2_provider', 'refreshtoken');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (21, 'social_django', 'association');
INSERT INTO `django_content_type` VALUES (22, 'social_django', 'code');
INSERT INTO `django_content_type` VALUES (23, 'social_django', 'nonce');
INSERT INTO `django_content_type` VALUES (25, 'social_django', 'partial');
INSERT INTO `django_content_type` VALUES (24, 'social_django', 'usersocialauth');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 57 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2024-10-02 11:07:04.184331');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2024-10-02 11:07:04.244908');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2024-10-02 11:07:04.475937');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2024-10-02 11:07:04.523515');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0003_alter_user_email_max_length', '2024-10-02 11:07:04.529744');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0004_alter_user_username_opts', '2024-10-02 11:07:04.534909');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0005_alter_user_last_login_null', '2024-10-02 11:07:04.540253');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0006_require_contenttypes_0002', '2024-10-02 11:07:04.543437');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2024-10-02 11:07:04.547661');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0008_alter_user_username_max_length', '2024-10-02 11:07:04.554972');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2024-10-02 11:07:04.560341');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0010_alter_group_name_max_length', '2024-10-02 11:07:04.572933');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0011_update_proxy_permissions', '2024-10-02 11:07:04.578193');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2024-10-02 11:07:04.583386');
INSERT INTO `django_migrations` VALUES (15, 'BusManage', '0001_initial', '2024-10-02 11:07:05.383152');
INSERT INTO `django_migrations` VALUES (16, 'BusManage', '0002_customer_user', '2024-10-02 11:07:05.451224');
INSERT INTO `django_migrations` VALUES (17, 'BusManage', '0003_remove_customer_user', '2024-10-02 11:07:05.515518');
INSERT INTO `django_migrations` VALUES (18, 'BusManage', '0004_delete_customer_user_address_user_phone_number', '2024-10-02 11:07:05.566325');
INSERT INTO `django_migrations` VALUES (19, 'BusManage', '0005_customer_remove_user_address_and_more', '2024-10-02 11:07:05.636940');
INSERT INTO `django_migrations` VALUES (20, 'BusManage', '0006_booking_ticket_code', '2024-10-02 11:07:05.690865');
INSERT INTO `django_migrations` VALUES (21, 'admin', '0001_initial', '2024-10-02 11:07:05.829150');
INSERT INTO `django_migrations` VALUES (22, 'admin', '0002_logentry_remove_auto_add', '2024-10-02 11:07:05.836490');
INSERT INTO `django_migrations` VALUES (23, 'admin', '0003_logentry_add_action_flag_choices', '2024-10-02 11:07:05.843760');
INSERT INTO `django_migrations` VALUES (24, 'oauth2_provider', '0001_initial', '2024-10-02 11:07:06.502828');
INSERT INTO `django_migrations` VALUES (25, 'oauth2_provider', '0002_auto_20190406_1805', '2024-10-02 11:07:06.561696');
INSERT INTO `django_migrations` VALUES (26, 'oauth2_provider', '0003_auto_20201211_1314', '2024-10-02 11:07:06.621034');
INSERT INTO `django_migrations` VALUES (27, 'oauth2_provider', '0004_auto_20200902_2022', '2024-10-02 11:07:06.985371');
INSERT INTO `django_migrations` VALUES (28, 'oauth2_provider', '0005_auto_20211222_2352', '2024-10-02 11:07:07.030192');
INSERT INTO `django_migrations` VALUES (29, 'oauth2_provider', '0006_alter_application_client_secret', '2024-10-02 11:07:07.058770');
INSERT INTO `django_migrations` VALUES (30, 'oauth2_provider', '0007_application_post_logout_redirect_uris', '2024-10-02 11:07:07.151379');
INSERT INTO `django_migrations` VALUES (31, 'sessions', '0001_initial', '2024-10-02 11:07:07.180876');
INSERT INTO `django_migrations` VALUES (32, 'default', '0001_initial', '2024-10-02 11:07:07.357364');
INSERT INTO `django_migrations` VALUES (33, 'social_auth', '0001_initial', '2024-10-02 11:07:07.359492');
INSERT INTO `django_migrations` VALUES (34, 'default', '0002_add_related_name', '2024-10-02 11:07:07.370502');
INSERT INTO `django_migrations` VALUES (35, 'social_auth', '0002_add_related_name', '2024-10-02 11:07:07.372740');
INSERT INTO `django_migrations` VALUES (36, 'default', '0003_alter_email_max_length', '2024-10-02 11:07:07.383551');
INSERT INTO `django_migrations` VALUES (37, 'social_auth', '0003_alter_email_max_length', '2024-10-02 11:07:07.384637');
INSERT INTO `django_migrations` VALUES (38, 'default', '0004_auto_20160423_0400', '2024-10-02 11:07:07.398213');
INSERT INTO `django_migrations` VALUES (39, 'social_auth', '0004_auto_20160423_0400', '2024-10-02 11:07:07.400291');
INSERT INTO `django_migrations` VALUES (40, 'social_auth', '0005_auto_20160727_2333', '2024-10-02 11:07:07.417404');
INSERT INTO `django_migrations` VALUES (41, 'social_django', '0006_partial', '2024-10-02 11:07:07.450356');
INSERT INTO `django_migrations` VALUES (42, 'social_django', '0007_code_timestamp', '2024-10-02 11:07:07.487337');
INSERT INTO `django_migrations` VALUES (43, 'social_django', '0008_partial_timestamp', '2024-10-02 11:07:07.519019');
INSERT INTO `django_migrations` VALUES (44, 'social_django', '0009_auto_20191118_0520', '2024-10-02 11:07:07.580017');
INSERT INTO `django_migrations` VALUES (45, 'social_django', '0010_uid_db_index', '2024-10-02 11:07:07.603166');
INSERT INTO `django_migrations` VALUES (46, 'social_django', '0011_alter_id_fields', '2024-10-02 11:07:07.860206');
INSERT INTO `django_migrations` VALUES (47, 'social_django', '0012_usersocialauth_extra_data_new', '2024-10-02 11:07:07.983673');
INSERT INTO `django_migrations` VALUES (48, 'social_django', '0013_migrate_extra_data', '2024-10-02 11:07:08.006253');
INSERT INTO `django_migrations` VALUES (49, 'social_django', '0014_remove_usersocialauth_extra_data', '2024-10-02 11:07:08.042672');
INSERT INTO `django_migrations` VALUES (50, 'social_django', '0015_rename_extra_data_new_usersocialauth_extra_data', '2024-10-02 11:07:08.079829');
INSERT INTO `django_migrations` VALUES (51, 'social_django', '0016_alter_usersocialauth_extra_data', '2024-10-02 11:07:08.091237');
INSERT INTO `django_migrations` VALUES (52, 'social_django', '0004_auto_20160423_0400', '2024-10-02 11:07:08.094593');
INSERT INTO `django_migrations` VALUES (53, 'social_django', '0002_add_related_name', '2024-10-02 11:07:08.096643');
INSERT INTO `django_migrations` VALUES (54, 'social_django', '0005_auto_20160727_2333', '2024-10-02 11:07:08.099846');
INSERT INTO `django_migrations` VALUES (55, 'social_django', '0001_initial', '2024-10-02 11:07:08.100951');
INSERT INTO `django_migrations` VALUES (56, 'social_django', '0003_alter_email_max_length', '2024-10-02 11:07:08.103085');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('28hccxauryfd04h30ehh5zfexv1jhhds', '.eJyNkEtPxCAUhf_KhHVtoI_pMCujRmviY6UTX2kuj7ZMW9ACG43_XTATrTvZAPec-3EPH6gB7_rGWzk3SqAtIihZ1hjwQeooiD3ozqTcaDcrlkZLelBtem2EHE8O3j-AHmwfsTkAlrkoi4pk60ridVm1BSl5UdCMs5YBLRmWJSUZCIIhx6KSnFSwoRUIygOUGTMo3X2PmS2vFm2fyCYh9CVBzjgYm9dZcRlcOK5fq5xAjWGYUem-N2nceAjV8uMuKiHbtHhHwxQYqH72RIp8df_sMcG5Xl3FQ0Z1H7ydMd0oj0zMmzXWgYstpw-XUO_e9-zMX5i2hnmAob55s3ebXf94fpuHRu6tM9Ph00mClG1-ShEmtVM80ILqZi8XDf8J8fkFs-CfVA:1sx7rR:0TFM5QVozFxFQZMi4q88M097g58Sya0E5cHabf1TWJY', '2024-10-19 16:42:29.830547');

-- ----------------------------
-- Table structure for oauth2_provider_accesstoken
-- ----------------------------
DROP TABLE IF EXISTS `oauth2_provider_accesstoken`;
CREATE TABLE `oauth2_provider_accesstoken`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires` datetime(6) NOT NULL,
  `scope` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `application_id` bigint NULL DEFAULT NULL,
  `user_id` bigint NULL DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `source_refresh_token_id` bigint NULL DEFAULT NULL,
  `id_token_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `token`(`token` ASC) USING BTREE,
  UNIQUE INDEX `source_refresh_token_id`(`source_refresh_token_id` ASC) USING BTREE,
  UNIQUE INDEX `id_token_id`(`id_token_id` ASC) USING BTREE,
  INDEX `oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr`(`application_id` ASC) USING BTREE,
  INDEX `oauth2_provider_acce_user_id_6e4c9a65_fk_BusManage`(`user_id` ASC) USING BTREE,
  CONSTRAINT `oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `oauth2_provider_acce_id_token_id_85db651b_fk_oauth2_pr` FOREIGN KEY (`id_token_id`) REFERENCES `oauth2_provider_idtoken` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `oauth2_provider_acce_source_refresh_token_e66fbc72_fk_oauth2_pr` FOREIGN KEY (`source_refresh_token_id`) REFERENCES `oauth2_provider_refreshtoken` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `oauth2_provider_acce_user_id_6e4c9a65_fk_BusManage` FOREIGN KEY (`user_id`) REFERENCES `busmanage_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of oauth2_provider_accesstoken
-- ----------------------------

-- ----------------------------
-- Table structure for oauth2_provider_application
-- ----------------------------
DROP TABLE IF EXISTS `oauth2_provider_application`;
CREATE TABLE `oauth2_provider_application`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `client_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `redirect_uris` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `authorization_grant_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_secret` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint NULL DEFAULT NULL,
  `skip_authorization` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `algorithm` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_logout_redirect_uris` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `client_id`(`client_id` ASC) USING BTREE,
  INDEX `oauth2_provider_appl_user_id_79829054_fk_BusManage`(`user_id` ASC) USING BTREE,
  INDEX `oauth2_provider_application_client_secret_53133678`(`client_secret` ASC) USING BTREE,
  CONSTRAINT `oauth2_provider_appl_user_id_79829054_fk_BusManage` FOREIGN KEY (`user_id`) REFERENCES `busmanage_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of oauth2_provider_application
-- ----------------------------

-- ----------------------------
-- Table structure for oauth2_provider_grant
-- ----------------------------
DROP TABLE IF EXISTS `oauth2_provider_grant`;
CREATE TABLE `oauth2_provider_grant`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires` datetime(6) NOT NULL,
  `redirect_uri` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `scope` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `application_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `code_challenge` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `code_challenge_method` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `nonce` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `claims` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `code`(`code` ASC) USING BTREE,
  INDEX `oauth2_provider_gran_application_id_81923564_fk_oauth2_pr`(`application_id` ASC) USING BTREE,
  INDEX `oauth2_provider_grant_user_id_e8f62af8_fk_BusManage_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `oauth2_provider_gran_application_id_81923564_fk_oauth2_pr` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `oauth2_provider_grant_user_id_e8f62af8_fk_BusManage_user_id` FOREIGN KEY (`user_id`) REFERENCES `busmanage_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of oauth2_provider_grant
-- ----------------------------

-- ----------------------------
-- Table structure for oauth2_provider_idtoken
-- ----------------------------
DROP TABLE IF EXISTS `oauth2_provider_idtoken`;
CREATE TABLE `oauth2_provider_idtoken`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `jti` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires` datetime(6) NOT NULL,
  `scope` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `application_id` bigint NULL DEFAULT NULL,
  `user_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `jti`(`jti` ASC) USING BTREE,
  INDEX `oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr`(`application_id` ASC) USING BTREE,
  INDEX `oauth2_provider_idtoken_user_id_dd512b59_fk_BusManage_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `oauth2_provider_idtoken_user_id_dd512b59_fk_BusManage_user_id` FOREIGN KEY (`user_id`) REFERENCES `busmanage_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of oauth2_provider_idtoken
-- ----------------------------

-- ----------------------------
-- Table structure for oauth2_provider_refreshtoken
-- ----------------------------
DROP TABLE IF EXISTS `oauth2_provider_refreshtoken`;
CREATE TABLE `oauth2_provider_refreshtoken`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `access_token_id` bigint NULL DEFAULT NULL,
  `application_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `revoked` datetime(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `access_token_id`(`access_token_id` ASC) USING BTREE,
  UNIQUE INDEX `oauth2_provider_refreshtoken_token_revoked_af8a5134_uniq`(`token` ASC, `revoked` ASC) USING BTREE,
  INDEX `oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr`(`application_id` ASC) USING BTREE,
  INDEX `oauth2_provider_refr_user_id_da837fce_fk_BusManage`(`user_id` ASC) USING BTREE,
  CONSTRAINT `oauth2_provider_refr_access_token_id_775e84e8_fk_oauth2_pr` FOREIGN KEY (`access_token_id`) REFERENCES `oauth2_provider_accesstoken` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `oauth2_provider_refr_user_id_da837fce_fk_BusManage` FOREIGN KEY (`user_id`) REFERENCES `busmanage_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of oauth2_provider_refreshtoken
-- ----------------------------

-- ----------------------------
-- Table structure for social_auth_association
-- ----------------------------
DROP TABLE IF EXISTS `social_auth_association`;
CREATE TABLE `social_auth_association`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `handle` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `secret` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `issued` int NOT NULL,
  `lifetime` int NOT NULL,
  `assoc_type` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `social_auth_association_server_url_handle_078befa2_uniq`(`server_url` ASC, `handle` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of social_auth_association
-- ----------------------------

-- ----------------------------
-- Table structure for social_auth_code
-- ----------------------------
DROP TABLE IF EXISTS `social_auth_code`;
CREATE TABLE `social_auth_code`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `social_auth_code_email_code_801b2d02_uniq`(`email` ASC, `code` ASC) USING BTREE,
  INDEX `social_auth_code_code_a2393167`(`code` ASC) USING BTREE,
  INDEX `social_auth_code_timestamp_176b341f`(`timestamp` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of social_auth_code
-- ----------------------------

-- ----------------------------
-- Table structure for social_auth_nonce
-- ----------------------------
DROP TABLE IF EXISTS `social_auth_nonce`;
CREATE TABLE `social_auth_nonce`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` int NOT NULL,
  `salt` varchar(65) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `social_auth_nonce_server_url_timestamp_salt_f6284463_uniq`(`server_url` ASC, `timestamp` ASC, `salt` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of social_auth_nonce
-- ----------------------------

-- ----------------------------
-- Table structure for social_auth_partial
-- ----------------------------
DROP TABLE IF EXISTS `social_auth_partial`;
CREATE TABLE `social_auth_partial`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `next_step` smallint UNSIGNED NOT NULL,
  `backend` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `data` json NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `social_auth_partial_token_3017fea3`(`token` ASC) USING BTREE,
  INDEX `social_auth_partial_timestamp_50f2119f`(`timestamp` ASC) USING BTREE,
  CONSTRAINT `social_auth_partial_chk_1` CHECK (`next_step` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of social_auth_partial
-- ----------------------------

-- ----------------------------
-- Table structure for social_auth_usersocialauth
-- ----------------------------
DROP TABLE IF EXISTS `social_auth_usersocialauth`;
CREATE TABLE `social_auth_usersocialauth`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `provider` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `uid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint NOT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `extra_data` json NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `social_auth_usersocialauth_provider_uid_e6b5e668_uniq`(`provider` ASC, `uid` ASC) USING BTREE,
  INDEX `social_auth_usersocialauth_user_id_17d28448_fk_BusManage_user_id`(`user_id` ASC) USING BTREE,
  INDEX `social_auth_usersocialauth_uid_796e51dc`(`uid` ASC) USING BTREE,
  CONSTRAINT `social_auth_usersocialauth_user_id_17d28448_fk_BusManage_user_id` FOREIGN KEY (`user_id`) REFERENCES `busmanage_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of social_auth_usersocialauth
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
